# DWave Tabu search, 100 reads, 50 restarts to find optimal MIS solution

import warnings
warnings.filterwarnings('ignore') # ignore warning from netx

from qubo_mis_generator import MISBenchmark
import csv

import json

import numba as nb
import numpy as np

from typing import Callable, Dict, Tuple, Union

from dimod import BinaryQuadraticModel, as_samples
from tabu import TabuSampler

def check_mis_np(Q, sample):
    # check for independent set in order to ensure cost is minimized

    assert len(sample) == qubo_matrix.shape[0], "Sample size does not match QUBO size"

    # get the nodes that are part of the MIS
    mis_nodes = [idx for idx in range(len(sample)) if sample[idx] == 1]
    
    # check if the MIS is valid
    for i in range(len(mis_nodes)):
        for j in range(i + 1, len(mis_nodes)):
            # check if dict entry exists
            if qubo_matrix[mis_nodes[i], mis_nodes[j]] != 0:
                return False
    
    return True

def check_mis_bqm(bqm, sample):
    # check for independent set in order to ensure cost is minimized

    assert len(sample) == bqm.num_variables, "Sample size does not match BQM size"

    # get the nodes that are part of the MIS
    mis_nodes = [node for node in sample if sample[node] == 1]
    
    # check if the MIS is valid
    for i in range(len(mis_nodes)):
        for j in range(i + 1, len(mis_nodes)):
            # check if dict entry exists
            if bqm.adj.get(mis_nodes[i]).get(mis_nodes[j]) is not None:
                return False
    
    return True

# Sourced from https://github.com/AlexanderNenninger/QUBOBrute
@nb.njit(fastmath=True)
def bits(n: Union[int, np.intp], nbits: int) -> np.ndarray:
    """Turn n into an array of float32.

    Args:
        n (int)
        nbits (int): length of output array

    Returns:
        The bits of n in an array of float32
    """
    bits = np.zeros(nbits, dtype=np.float32)
    i = 0
    while n > 0:
        n, rem = n // 2, n % 2
        bits[i] = rem
        i += 1
    return bits

# Sourced from https://github.com/AlexanderNenninger/QUBOBrute
@nb.njit(parallel=True, fastmath=True)
def brute_force_solve(Q):
    """Calculate all possible values of the QUBO H(x) = x^T Q x in parallel on the CPU.

    Args:
        Q (np.ndarray)

    Returns:
        np.ndarray: all possible values H can take.
    """
    Q = Q.astype(np.float32)
    nbits = Q.shape[0]
    N = 2**nbits
    out = np.zeros(N, dtype=np.float32)
    for i in nb.prange(N):
        xs = bits(i, nbits)
        out[i] = xs @ Q @ xs

    return out

if __name__ == '__main__':
    benchmark = MISBenchmark('config_no_costs.csv')
    dataset_dir = './data/qubo_mis_dataset'

    costs = {}

    for qubo_matrix, num_vertices, density, seed, _ in benchmark.load_problems(dataset_dir):
        print("Problem: ", num_vertices, density, seed)
        key = f'{num_vertices}_{density}_{seed}'

        if num_vertices < 1000:
            # brute force solve
            bf_costs = brute_force_solve(qubo_matrix)
            c_optimal = np.min(bf_costs)
            idx = np.argmin(bf_costs)
            sample = bits(idx, qubo_matrix.shape[0])

            # sanity check
            assert check_mis_np(qubo_matrix, sample), "Brute force did not find a valid MIS"

            costs[key] = int(c_optimal)

        else:
            bqm = BinaryQuadraticModel(qubo_matrix, "BINARY")

            sampler = TabuSampler()
            # sampleset = sampler.sample(bqm, timeout=None, num_reads=100, num_restarts=50)
            sampleset = sampler.sample(bqm, timeout=None, num_reads=10, num_restarts=5)

            # solver sanity check
            # while not guaranteed, it is highly likely the solver finds independent sets
            assert check_mis_bqm(bqm, sampleset.first.sample), "Solver did not find a valid MIS"

            costs[key] = int(sampleset.first.energy)

        # temporary save costs dict as json
        with open('costs.json', 'w') as f:
            json.dump(costs, f)


    # rewrite csv
    header = ['num_vertices', 'density', 'random_seed', 'c_optimal']
    with open('default_config.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for nv in num_vertices:
            for d in density:
                for rs in random_seed:
                    c_optimal = costs[f'{nv}_{d}_{rs}']
                    writer.writerow([nv, d, rs, c_optimal])
