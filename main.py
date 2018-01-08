#!/usr/bin/python2.7

import sys
import random
import phenotype
import math

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

<<<<<<< HEAD
	def mutation(self):
		i = 0
		while i < self.number_of_individuals * 0.1:
			self.population[random.randint(0, len(self.population) - 1)].mutation()
			i += 1

=======
>>>>>>> 4d75b3b6b7213289b4f3c055b06091244a777cda
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

<<<<<<< HEAD
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
		
	def RouletteSelection(self, amount):
		self.calc_fitness()
		chosen = []
		self.sort()
		
		for i in range(amount):
		# roll dice
		
			pick = random.uniform(0, 1)
			current=0
			for agent in self.population:
				current += agent.get_influence()

				if current > pick:

					chosen.append(agent)
					break

		return chosen
		
=======
>>>>>>> 4d75b3b6b7213289b4f3c055b06091244a777cda

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
<<<<<<< HEAD
		self.max_iterations = 20
		self.calc_fitness()
		self.selection_method = selection_method
		
=======
		self.max_iterations = 1
		self.calc_fitness()
		self.selection_method = selection_method
		self.crossover_method = crossover_method

>>>>>>> 4d75b3b6b7213289b4f3c055b06091244a777cda
	def step(self):

		print self.num_iterations , ": average fitness" , self.get_avg_fitness()

		self.num_iterations += 1
<<<<<<< HEAD

		
		
		
		
		parents=self.population[:self.lambd] #choose lambda of parents  #actually that works better than
		#parents=self.RouletteSelection(self.lambd)
		
		#make children
		list_of_indices = list(range(self.number_of_individuals))
		children = []
		for pair in range(int(self.number_of_individuals / 2)):
			first = random.randint(0, len(list_of_indices) - 1)
			del list_of_indices[first]
			second = random.randint(0, len(list_of_indices) - 1)
			del list_of_indices[second]

			first_parent = parents[first]
			second_parent = parents[second]
			index = random.randint(0, NUMBER_OF_CARDS-1)
		
			child = first_parent.crossover(second_parent,"single-point")
			child['a'].mutate(index)
			child['b'].mutate(index)
			first_parent.calc_fitness_function(self.expected_sum_A, self.expected_sum_B)
			second_parent.calc_fitness_function(self.expected_sum_A, self.expected_sum_B)
			child['a'].calc_fitness_function(self.expected_sum_A, self.expected_sum_B)
			child['b'].calc_fitness_function(self.expected_sum_A, self.expected_sum_B)

			selector = []
			selector.append(first_parent)
			selector.append(second_parent)
			selector.append(child['a'])
			selector.append(child['b'])
			selector.sort(key=lambda x: x.get_fitness(), reverse=True)

			children.append(selector[0])
			children.append(selector[1])

		
		#add children to population
		for x in children:
			self.population.append(x)
			self.number_of_individuals+=1
		
		#choose next population
		
		
		next_population=self.RouletteSelection(self.mi)
		
		self.number_of_individuals=self.mi
		self.population=next_population
		
=======
		self.calc_fitness()
		self.sort()
		T = []
		if self.selection_method == "RouletteSelection":
			T = self.RouletteSelection(self.crossover_method)

>>>>>>> 4d75b3b6b7213289b4f3c055b06091244a777cda

def main(argv):
	g = OnePlusOneStrategy()
	print "1 + 1 Strategy:\nBefore:"
	print g
	while g.num_iterations < g.max_iterations:

		if g.population[0].fitness == 0:
			break
		g.step()
	print "After:",g.num_iterations, "iterations:\n",g

<<<<<<< HEAD
	print " mi plus lambda strategy:\n"
	h = MiPlusLambdaStrategy(100, 400, "RouletteSelection")
	while h.get_best().fitness == 0:
		h = MiPlusLambdaStrategy(100, 400, "RouletteSelection")
	
=======
	print "\nmi plus lambda Strategy:\nBefone:"
	h = MiPlusLambdaStrategy(8, 10, "RouletteSelection", "single-point")
>>>>>>> 4d75b3b6b7213289b4f3c055b06091244a777cda
	print h
	while h.num_iterations < h.max_iterations:

		if h.get_best().fitness == 0:
			break
		h.step()
<<<<<<< HEAD
	#print h
	print h.num_iterations
	print h.get_best()
=======
	print "After:",h.num_iterations, "iterations:\n", h
>>>>>>> 4d75b3b6b7213289b4f3c055b06091244a777cda

if __name__ == "__main__":
	main(sys.argv[1:])

	
