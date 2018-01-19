#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import phenotype
import random
import solution
import numpy as np

class Generation():
	def __init__(self, number_of_individuals, gen=[0]):
		if gen == [0]:
			self.population = [phenotype.Phenotype(size = solution.NUMBER_OF_CARDS)
								for i in range(number_of_individuals)]
		else:
			self.population = [phenotype.Phenotype(genotype=gen)
								for i in range(number_of_individuals)]
		self.num_iterations = 0
		self.number_of_individuals = number_of_individuals
		self.expected_sum_A = solution.SUM_A
		self.expected_sum_B = solution.SUM_B
		self.max_iterations = solution.MAX_ITERATIONS


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
			s += agent.fitness
			if m < agent.fitness:
				m = agent.fitness

		for x in self.population:
			x.calc_influence(s, m, self.number_of_individuals)

		self.population.sort(key=lambda x: x.influence, reverse=True)


	def sort(self):
		for individual in self.population:
			individual.calc_fitness_function(self.expected_sum_A, self.expected_sum_B)
		self.population.sort(key=lambda x: x.fitness, reverse=False)


	def get_best(self):
		self.sort()
		return self.population[0]


	def get_avg_fitness(self):
		fitness_sum = 0.0
		for individual in self.population:
			individual.calc_fitness_function(self.expected_sum_A, self.expected_sum_B)
			fitness_sum += individual.fitness

		return float(fitness_sum) / float(self.number_of_individuals)

		
	def RouletteSelection(self, amount):
		self.calc_fitness()
		chosen = []
		self.sort()
		
		for i in range(amount):
		# roll dice
			pick = random.uniform(0, 1)
			for agent in self.population:
				pick -= agent.influence

				if pick < 0:
					chosen.append(agent)
					break
		return chosen
	
	
	def TournamentSelection(self, amount):
		self.calc_fitness()
		chosen = []
		q=3
		A = np.array(self.population)
		B = A[0:(len(A)/q)*q]
		random.shuffle(B)
		C = np.reshape(B,(len(A)/q,q))
		i=0
		j=0
		k = C.shape[0]
		while i < amount:
			if j == k:
				random.shuffle(B)
				C = np.reshape(B,(len(A)/q,q))
				j = 0
				
			first_rival  = C[j][0]
			second_rival = C[j][1]
			third_rival  = C[j][2]
			
			if first_rival.fitness < second_rival.fitness:
				if third_rival.fitness < first_rival.fitness:
					chosen.append(third_rival)
				else:
					chosen.append(first_rival)
			else:
				if third_rival.fitness < second_rival.fitness:
					chosen.append(third_rival)
				else:
					chosen.append(second_rival)
			i += 1
			j += 1
		return chosen
		
	def RankingSelection(self, amount):
		self.calc_fitness()
		chosen = []
		
		self.sort()
		a = (-1.0/self.number_of_individuals)
		probability = range(0,self.number_of_individuals)
		probability = [ i*a+6 for i in probability]
		s = sum(probability)
		probability = [i/s for i in probability]
		for i in range(amount):
			p = random.uniform(0, 1)
			for index in range(0,len(probability)):
				p -= probability[index]

				if p < 0:
					chosen.append(self.population[index])
					break

		return chosen
		
	def Selection(self, selection_method="RouletteSelection" ):
		if selection_method == "RouletteSelection":
			return self.RouletteSelection(self.lambd)
			
		elif selection_method == "TournamentSelection":
			return self.TournamentSelection(self.lambd)
			
		elif selection_method == "RankingSelection":
			return self.RankingSelection(self.lambd)
			
		else: return None
		
		
	
class OnePlusOneStrategy(Generation, object):

	def __init__(self, genotype=[0]):
		super(OnePlusOneStrategy, self).__init__(1, genotype)
		self.calc_fitness()		

	def step(self):
		self.num_iterations += 1
		y = phenotype.Phenotype(size=solution.NUMBER_OF_CARDS, genotype=self.population[0].genotype[:])
		index = random.randint(0, solution.NUMBER_OF_CARDS-1)
		y.mutate(index)
		y.calc_fitness_function(self.expected_sum_A, self.expected_sum_B)
		if y.fitness < self.population[0].fitness:
			self.population[0].genotype = y.genotype
			self.population[0].calc_fitness_function(self.expected_sum_A, self.expected_sum_B)
		
		return self.population[0].fitness
			
class OnePlusOneParalleledStrategy(Generation, object):
	def __init__(self, number_of_threads, genotyp=[0]):
		super(OnePlusOneParalleledStrategy, self).__init__(number_of_threads, genotyp)
		if genotyp == [0]:
			phen = phenotype.Phenotype(size = solution.NUMBER_OF_CARDS)
		else:
			phen = phenotype.Phenotype(genotype = genotyp)
		for index in range(0,len(self.population)):
			self.population[index] = phen
		self.calc_fitness()
		self.best = self.population[0]
		
	def step(self):
		self.num_iterations += 1
		
		for i in range(0, self.number_of_individuals-1):
			y = phenotype.Phenotype(size=solution.NUMBER_OF_CARDS, genotype=self.population[i].genotype[:])
			index = random.randint(0, solution.NUMBER_OF_CARDS-1)
			y.mutate(index)
			y.calc_fitness_function(self.expected_sum_A, self.expected_sum_B)
			if y.fitness < self.best.fitness:
				self.best = y
		
		for index in range(0, self.number_of_individuals):
			self.population[index] = self.best
		self.calc_fitness()
		
		return self.best.fitness


class EvolutionaryProgrammingStrategy(Generation, object):
	def __init__(self, mi):
		super(EvolutionaryProgrammingStrategy, self).__init__(mi)
		self.calc_fitness()
		
	def step(self):
		self.num_iterations += 1
		
		for index in range(0, self.number_of_individuals):
			child = (phenotype.Phenotype(size=solution.NUMBER_OF_CARDS, genotype=self.population[index].genotype[:]))
			child.mutate(random.randint(0, solution.NUMBER_OF_CARDS-1))
			child.calc_fitness_function(self.expected_sum_A, self.expected_sum_B)
			
			self.population.append(child)
		
		self.sort()
		self.population = self.RankingSelection(self.number_of_individuals)		
		
		return self.population[0].fitness


class MiPlusLambdaStrategy(Generation, object):

	def __init__(self, mi, lambd, selection_method, crossover_method="single-point"):
		if mi > lambd:
			raise RuntimeError('Bad argument! mi cannot be greater than lambda!')
		super(MiPlusLambdaStrategy, self).__init__(mi)
		self.mi = mi
		self.lambd = lambd

		self.calc_fitness()
		self.selection_method = selection_method
		self.crossover_method = crossover_method


	def step(self):
		self.num_iterations += 1
		parents = []
		
		parents = self.Selection(self.selection_method)
		
		#make children
		list_of_indices = list(range(self.number_of_individuals))
		children = []
		first = -2
		second = -1
		
		for pair in range(int(self.number_of_individuals / 2)):
			first += 2
			second += 2
			first_parent = parents[first]
			second_parent = parents[second]
		
			child={}
			if random.uniform(0,1) < solution.CROSSOVER_PROBABILITY:
				child = first_parent.crossover(second_parent,self.crossover_method)
			else:
				child['a'] = first_parent
				child['b'] = second_parent
				
			if random.uniform(0,1) < solution.MUTATION_PROBABILITY:
				child['a'].mutate(random.randint(0, solution.NUMBER_OF_CARDS-1))
			

			if random.uniform(0,1) < solution.MUTATION_PROBABILITY:
				child['b'].mutate(random.randint(0, solution.NUMBER_OF_CARDS-1))
				
			
			child['a'].calc_fitness_function(self.expected_sum_A, self.expected_sum_B)
			child['b'].calc_fitness_function(self.expected_sum_A, self.expected_sum_B)

			children.append(child['a'])
			children.append(child['b'])
			
		

		#add children to population
		for x in children:
			self.population.append(x)

		self.sort()
		self.population = self.population[0:self.number_of_individuals]
		
		return self.population[0].fitness
		

class MiLambdaStrategy(Generation, object):

	def __init__(self, mi, lambd, selection_method, crossover_method="single-point"):
		if mi > lambd:
			raise RuntimeError('Bad argument! mi cannot be greater than lambda!')
		super(MiLambdaStrategy, self).__init__(mi)
		self.mi = mi
		self.lambd = lambd

		
		self.calc_fitness()
		self.selection_method = selection_method
		self.crossover_method = crossover_method

	def step(self):
		self.num_iterations += 1

		parents = self.Selection(self.selection_method)
		
		#make children
		list_of_indices = list(range(self.number_of_individuals))
		children = []
		first = -2
		second = -1
		
		for pair in range(int(self.number_of_individuals / 2)):
			first += 2
			second += 2
			first_parent = parents[first]
			second_parent = parents[second]
		
			child={}
			if random.uniform(0,1) < solution.CROSSOVER_PROBABILITY:
				child = first_parent.crossover(second_parent,
												self.crossover_method)
			else:
				child['a'] = first_parent
				child['b'] = second_parent
				
			if random.uniform(0,1) < solution.MUTATION_PROBABILITY:
				child['a'].mutate(random.randint(0, solution.NUMBER_OF_CARDS-1))
			

			if random.uniform(0,1) < solution.MUTATION_PROBABILITY:
				child['b'].mutate(random.randint(0, solution.NUMBER_OF_CARDS-1))
				
			
			child['a'].calc_fitness_function(self.expected_sum_A, self.expected_sum_B)
			child['b'].calc_fitness_function(self.expected_sum_A, self.expected_sum_B)

			children.append(child['a'])
			children.append(child['b'])
			
		
		self.population = []
		#add children to population
		for x in children:
			self.population.append(x)

		self.sort()
		self.population = self.population[0:self.number_of_individuals]
		
		return self.population[0].fitness
