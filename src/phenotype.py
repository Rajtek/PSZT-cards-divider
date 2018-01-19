#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import random

class Phenotype:
	def __init__(self, **kwargs):
		if "genotype" in kwargs.keys():
			if type(kwargs["genotype"]) != list:
				raise RuntimeError('Bad argument "genotype". Must be list')
			for i in kwargs["genotype"]:
				if not (i == 0 or i == 1):
					raise RuntimeError('Bad "argument" genotype. ' "Not a binary list")
			self.genotype = kwargs["genotype"]
		elif "size" in kwargs.keys():
			if type(kwargs["size"]) != int or kwargs["size"] < 1:
				print kwargs["size"]
				raise RuntimeError('Bad argument "size". Must be int>0')
			self.genotype = [random.randint(0, 1) for x in range(kwargs["size"])]
		else:
			raise RuntimeError("Bad arguments")

		# that ones will be compute later
		self.fitness = 0.0
		self.influence = 0.0


	def __str__(self):
		st = "   Genotype   \n"
		s = "".join([str(x) for x in self.genotype])
		s = (st + "Genotype: " + s + " Fitness: " + str(self.fitness) +
             " Influence: " + str(self.influence))
		self.group_a = []
		self.sum_a = 0
		self.group_b = []
		self.sum_b = 0
		for position, value in enumerate(self.genotype):
			if value == 0:
				self.group_a.append(position + 1)
				self.sum_a += position + 1
			else:
 				self.group_b.append(position + 1)
				self.sum_b += position + 1
		s += "\n"
		s += "Group 1: " + str(self.group_a)
		s += " Sum_a: " + str(self.sum_a) + "\n"
		s += "Group 2: " + str(self.group_b)
		s += " Sum_b: " + str(self.sum_b) + "\n"
		s += "========================="
		return s


	def __repr__(self):
		return self.__str__()


	def calc_influence(self, s, maximum, i):
		self.influence = (float(maximum - self.fitness + 1) / float(i * (maximum + 1) - s))


	def mutate(self, index):
		self.genotype[index] ^= 1


	def crossover(self, other, method="single-point"):

		if method == "single-point":
			position = random.randint(1, len(self.genotype) - 1)
			children_a = []
			children_b = []
			for x in range(len(self.genotype)):
				if x < position:
					children_a.append(self.genotype[x])
					children_b.append(other.genotype[x])
				else:
					children_b.append(self.genotype[x])
					children_a.append(other.genotype[x])
	
			return {'a': Phenotype(genotype=children_a),'b': Phenotype(genotype=children_b)}
		elif method == "two-point":
			position = sorted(random.sample( range( 1, len( self.genotype ) -2 ), 2))
			children_a = []
			children_b = []
			for x in range( len( self.genotype ) ):
				if x < position[0]:
					children_a.append(self.genotype[x])
					children_b.append(other.genotype[x])
				elif x >= position[0] and x < position[1]:
					children_b.append(self.genotype[x])
					children_a.append(other.genotype[x])
				elif x >= position[1]:
					children_a.append(self.genotype[x])
					children_b.append(other.genotype[x])
			return {'a': Phenotype(genotype=children_a),'b': Phenotype(genotype=children_b)}
		elif method == "uniform":
			children_a = []
			children_b = []
			for x in range( len( self.genotype ) ):
				rand = random.randint(0, 1)
				if rand == 0:
					children_a.append(self.genotype[x])
					children_b.append(other.genotype[x])
				else:
					children_b.append(self.genotype[x])
					children_a.append(other.genotype[x])
			return {'a': Phenotype(genotype=children_a),'b': Phenotype(genotype=children_b)}
		else:
			return None
			
			
	def calc_fitness_function(self, A, B):
		s = 0
		i = 0
		for x in range(len(self.genotype)):
			if self.genotype[x] == 0:
				s += (x + 1)
			else:
				i += (x + 1)
		self.fitness = abs(A - s) + abs(B - i)


