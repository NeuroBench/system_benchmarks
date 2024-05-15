# from lava.lib.optimization.utils.generators.mis import MISProblem
from mis import MISProblem

class MISBenchmark:
    '''
    An iterable which generates MIS problem Q-matrices.

    The iterable returns the tuple (graph, c_optimal), where:
    - graph format is an (N x N) symmetric np array with -1 on diagonal and 2 at edges.
    - c_optimal has been found as the global MIS / best found by conventional solver

    The problem parameters should be given as a csv config file with the following format:
    num_vertices,density,random_seed,c_optimal

    By default, the problems allowed for tuning the system are the following:
    - num_vertices: [25, 50, 100, 250, 500, 1000, 2500, 5000]
    - density:      [0.01, 0.05, 0.10, 0.25]
    - random_seed:  [0, 1, 2, 3, 4]

    The benchmark submission will use a withheld set of parameters for evaluation.
    '''

    def __init__(self, config_file):
        if not config_file:
            raise ValueError('Config file must be provided.')
        self.config_file = config_file
        
        with open(self.config_file, 'r') as f:
            num_problems = sum(1 for line in f) - 1
        self.num_problems = num_problems

    def generate_problems(self):
        with open(self.config_file, 'r') as f:
            for line in f:
                if line.startswith('num_vertices'):
                    continue

                num_vertices, density, random_seed, c_optimal = line.split(',')
                mis = MISProblem.from_random_uniform(int(num_vertices), float(density), int(random_seed))
                # qubo_matrix = mis.get_qubo_matrix(w_diag=1, w_off=8)
                qubo_matrix = mis.get_qubo_matrix()
                yield qubo_matrix, int(num_vertices), float(density), int(random_seed), int(c_optimal)

    def __len__(self):
        return self.num_problems

    @staticmethod
    def custom_graph(num_vertices: int, density: float, random_seed: int = 0):
        '''
        Returns a custom MIS problem with the given parameters.

        Should be used to find the maximum supported system workload size, at 100% and 1% density:
        MISBenchmark.custom_graph(size, 1.0)
        MISBenchmark.custom_graph(size, 0.01)
        '''

        mis = MISProblem.from_random_uniform(num_vertices, density, random_seed)
        qubo_matrix = mis.get_qubo_matrix()

        return qubo_matrix


