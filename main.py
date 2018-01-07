#!/usr/bin/python2.7

import sys
import random
import phenotype

NUMBER_OF_CARDS = 10
SUM_A = 20
SUM_B = 100
CROSSOVER_PROPABILITY = 0.7
MUTATION_PROBABILITY = 0.02

class Generation():
	def __init__(self, number_of_individuals):
		self.population = [phenotype.Phenotype(size=NUMBER_OF_CARDS) for i in range(number_of_individuals)]
		self.num_iterations = 0
		self.number_of_individuals = number_of_individuals
		self.expected_sum_A = SUM_A
		self.expected_sum_B = SUM_B

	def __str__(self):
		s = "\n".join([str(x) for x in self.population])
		s = "\n************Population: **************" + s + "\n"
		return s

	def calc_fitness(self):
		for individual in self.population:
			individual.calc_fitness_function(self.expected_sum_A, self.expected_sum_B)

		s = 0
		m = 0

		# Sum all influences and get the biggest one - we will use it
		# in calc_influence
		for agent in self.population:
			s += agent.get_fitness()
			if m < agent.get_fitness():
				m = agent.get_fitness()

		for x in self.population:
			x.calc_influence(s, m, self.number_of_individuals)

		self.population.sort(key=lambda x: x.get_influence(), reverse=True)

	def sort(self):
		for individual in self.population:
			individual.calc_fitness_function(self.expected_sum_A, self.expected_sum_B)
		self.population.sort(key=lambda x: x.get_fitness(), reverse=False)

	def get_best(self):
		self.sort()
		return self.population[0]

	def get_worst(self):
		self.sort()
		return self.population[-1]

	def get_avg_fitness(self):
		fitness_sum = 0.0
		for individual in self.population:
			individual.calc_fitness_function(self.expected_sum_A, self.expected_sum_B)
			fitness_sum += individual.get_fitness()

		return float(fitness_sum) / float(self.number_of_individuals)


	def RouletteSelection(self,crossover_method):
		parents = []
		self.sort()
		for i in range(self.lambd):
		# roll dice
			dice = random.random()
			for agent in self.population:
				dice -= agent.get_influence()
				if dice <= 0:
					parents.append(agent)
					break

		return parents
	
class OnePlusOneStrategy(Generation, object):

	def __init__(self):
		super(OnePlusOneStrategy, self).__init__(1)
		self.max_iterations = 15
		self.calc_fitness()

	def step(self):
		self.num_iterations += 1
		y = phenotype.Phenotype(size=NUMBER_OF_CARDS,genotype=self.population[0].get_genotype()[:])
		index = random.randint(0, NUMBER_OF_CARDS-1)
		y.mutate(index)
		y.calc_fitness_function(self.expected_sum_A, self.expected_sum_B)
		if y.fitness < self.population[0].fitness:
			self.population[0].genotype = y.genotype
			self.population[0].calc_fitness_function(self.expected_sum_A, self.expected_sum_B)


class MiPlusLambdaStrategy(Generation, object):

	def __init__(self, mi, lambd, selection_method, crossover_method):
		if mi > lambd:
			raise RuntimeError('Bad argument! mi cannot be greater than lambda!')
		super(MiPlusLambdaStrategy, self).__init__(mi)
		self.mi = mi
		self.lambd = lambd
		self.max_iterations = 1
		self.calc_fitness()
		self.selection_method = selection_method
		self.crossover_method = crossover_method

	def step(self):
		self.num_iterations += 1
		self.calc_fitness()
		self.sort()
		T = []
		if self.selection_method == "RouletteSelection":
			T = self.RouletteSelection(self.crossover_method)


def main(argv):
	g = OnePlusOneStrategy()
	print "1 + 1 Strategy:\nBefore:"
	print g
	while g.num_iterations < g.max_iterations:
		if g.population[0].fitness == 0:
			break
		g.step()
	print "After:",g.num_iterations, "iterations:\n",g

	print "\nmi plus lambda Strategy:\nBefone:"
	h = MiPlusLambdaStrategy(8, 10, "RouletteSelection", "single-point")
	print h
	while h.num_iterations < h.max_iterations:
		if h.get_best().fitness == 0:
			break
		h.step()
	print "After:",h.num_iterations, "iterations:\n", h

if __name__ == "__main__":
	main(sys.argv[1:])

	
