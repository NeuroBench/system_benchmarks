# DWave Tabu search, 100 reads, 50 restarts to find optimal MIS solution

import warnings
warnings.filterwarnings('ignore') # ignore warning from netx

from qubo_mis_generator import MISBenchmark
import csv

from dimod import BinaryQuadraticModel, as_samples
from tabu import TabuSampler

def check_mis(bqm, sample):
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

if __name__ == '__main__':
    benchmark = MISBenchmark('default_config.csv')
    
    for qubo_matrix, num_vertices, density, seed, _ in benchmark.generate_problems():
        print("Problem: ", num_vertices, density, seed)

        bqm = BinaryQuadraticModel(qubo_matrix, "BINARY")

        sampler = TabuSampler()
        sampleset = sampler.sample(bqm, timeout=None, num_reads=100, num_restarts=50)

        # check lowest energy sample
        if check_mis(bqm, sampleset.first.sample):
            print("Valid MIS found, set size = ", sum(sampleset.first.sample.values()))
        else:
            # TODO: should check samples in sampleset sequentially until a valid MIS is found
            print("No valid MIS found")

    # TODO: rewrite the csv with c_optimal values