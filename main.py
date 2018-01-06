#!/usr/bin/python2.7

import sys
import random
import phenotype

NUMBER_OF_CARDS = 15
SUM_A = 20
SUM_B = 100

class Generation():
	def __init__(self, number_of_individuals):
		self.population = [phenotype.Phenotype(size=NUMBER_OF_CARDS) for i in range(number_of_individuals)]
		self.num_iterations = 0
		self.number_of_individuals = number_of_individuals
		self.expected_sum_A = SUM_A
		self.expected_sum_B = SUM_B

	def __str__(self):
		s = "\n".join([str(x) for x in self.population])
		s = "\n\n************Population: **************\n" + s + "\n\n"
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

	def mutation(self):
		i = 0
		while i < self.number_of_individuals * 0.1:
			self.population[random.randint(0, len(self.population) - 1)].mutation()
			i += 1

	def get_best(self):
		for individual in self.population:
			individual.calc_fitness_function(self.expected_sum_A, self.expected_sum_B)
		self.population.sort(key=lambda x: x.get_fitness(), reverse=False)
		return self.population[0]

	def get_worst(self):
		self.get_best()
		return self.population[-1]

	def get_avg_fitness(self):
		fitness_sum = 0.0
		for individual in self.population:
			individual.calc_fitness_function(self.expected_sum_A, self.expected_sum_B)
			fitness_sum += individual.get_fitness()

		return float(fitness_sum) / float(self.number_of_individuals)

	def step(self):
		i = 0
		while (i < self.population[0].get_fitness() * self.number_of_individuals * 10 and i < (len(self.population) - 1)):
			#self.population[random.randint(0, self.number_of_individuals - 1)].mutation(0.5, self.bit_probability_table)
			i += 1

		# Crossovers
		i = 0
		while (i < 10 * self.population[0].get_fitness() and i < (len(self.population) - 1)):
			one = self.population[i]
			i += 1
			second = self.population[i]
			i += 1
			r = one.crossover(second)
			#r['a'].mutation(0.01, self.bit_probability_table)
			#r['b'].mutation(0.01, self.bit_probability_table)
			self.population.append(r['a'])
			self.population.append(r['b'])

		self.get_best()
		# Get rid of half of the population
		self.population = self.population[0:self.number_of_individuals]
		self.num_iterations += 1
		assert (len(self.population) == self.number_of_individuals)

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


class NiPlusLambdaStrategy(Generation, object):

	def __init__(self, ni, lambd, selection_method):
		if ni > lambd:
			raise RuntimeError('Bad argument! ni cannot be greater than lambda!')
		super(NiPlusLambdaStrategy, self).__init__(ni)
		self.ni = ni
		self.lambd = lambd
		self.max_iterations = 15
		self.calc_fitness()
		self.selection_method = selection_method

	def step(self):
		self.num_iterations += 1
		self.calc_fitness()
		T = []
		i = 0

def main(argv):
	g = OnePlusOneStrategy()
	print " 1 + 1 Strategy\n:"
	print g
	print g.num_iterations
	while g.num_iterations < g.max_iterations:
		if g.population[0].fitness == 0:
			break
		g.step()
	print g
	print g.num_iterations

	print " ni plus lambda strategy:\n"
	h = NiPlusLambdaStrategy(5, 10, "RouletteSelection")
	print h
	print h.num_iterations
	while h.num_iterations < h.max_iterations:
		if h.get_best().fitness == 0:
			break
		h.step()
	print h
	print h.num_iterations


if __name__ == "__main__":
	main(sys.argv[1:])

	
