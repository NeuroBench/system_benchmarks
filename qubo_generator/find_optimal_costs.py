# DWave Tabu search, 100 reads, 50 restarts to find optimal MIS solution

import warnings
warnings.filterwarnings('ignore') # ignore warning from netx

from qubo_mis_generator import MISBenchmark
import csv
import json
import numpy as np
from brute_solver import solve_cpu, solve_gpu, bits

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

def sample_to_binary_list(sample):
    N = len(sample)
    mis_nodes = [node for node in sample if sample[node] == 1]
    l = [0 if i not in mis_nodes else 1 for i in range(N)]
    return l

if __name__ == '__main__':
    benchmark = MISBenchmark('config_no_costs.csv')
    dataset_dir = './data/qubo_mis_dataset'

    # look for temp costs file
    try:
        with open('costs.json', 'r') as f:
            costs = json.load(f)
    except FileNotFoundError:
        costs = {}

    for qubo_matrix, num_vertices, density, seed, _ in benchmark.load_problems(dataset_dir):
        print("Problem: ", num_vertices, density, seed)
        key = f'{num_vertices}_{density}_{seed}'

        if key in costs:
            continue

        if num_vertices < 50: # the current specification says 1000 nodes, but 50 is already large
            # brute force solve
            bf_costs = solve_gpu(qubo_matrix, 0)
            # bf_costs = solve_cpu(qubo_matrix.astype(np.float32), 0)
            c_optimal = np.min(bf_costs)
            idx = np.argmin(bf_costs)
            sample = bits(idx, qubo_matrix.shape[0])

            # sanity check
            assert check_mis_np(qubo_matrix, sample), "Brute force did not find a valid MIS"

            costs[key] = int(c_optimal)

        else:
            bqm = BinaryQuadraticModel(qubo_matrix, "BINARY")

            sampler = TabuSampler()
            sampleset = sampler.sample(bqm, timeout=None, num_reads=100, num_restarts=50)

            # solver sanity check
            # while not guaranteed, it is highly likely the solver finds independent sets
            assert check_mis_bqm(bqm, sampleset.first.sample), "Solver did not find a valid MIS"

            print("found min cost", int(sampleset.first.energy), "for sample", sample_to_binary_list(sampleset.first.sample), flush=True)

            costs[key] = int(sampleset.first.energy)

        # temporary save costs dict as json
        with open('costs.json', 'w') as f:
            json.dump(costs, f)

    # rewrite csv
    header = ['num_vertices', 'density', 'random_seed', 'c_optimal']
    with open('default_config.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for key, value in costs.items():
            num_vertices, density, random_seed = key.split('_')
            c_optimal = value
            writer.writerow([num_vertices, density, random_seed, c_optimal])
