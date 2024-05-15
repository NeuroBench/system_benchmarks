import csv

header = ['num_vertices', 'density', 'random_seed', 'c_optimal']
num_vertices = [10, 25, 50, 100, 250, 500, 1000, 2500, 5000]
density = [0.01, 0.05, 0.10, 0.25]
random_seed = [0, 1, 2, 3, 4]
c_optimal = -1   # TODO: run DWave Tabu search to find c_optimal

with open('default_config.csv', 'w', newline='') as f:
	writer = csv.writer(f)
	writer.writerow(header)
	for nv in num_vertices:
		for d in density:
			for rs in random_seed:
				writer.writerow([nv, d, rs, c_optimal])