#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import phenotype
import random
import solution

def int_to_list(iter):
	li=[int(x) for x in bin(iter)[2:]]
	
	while len(li) < solution.NUMBER_OF_CARDS:
		li = [0] + li
	return li
	

last=2**solution.NUMBER_OF_CARDS
best=phenotype.Phenotype(genotype=int_to_list(0))
best.calc_fitness_function(solution.SUM_A, solution.SUM_B)
iter=1
while iter<last:
	y= phenotype.Phenotype(genotype=int_to_list(iter))
	y.calc_fitness_function(solution.SUM_A, solution.SUM_B)
	if y.fitness==0:
		best=y;
		break;
	elif y.fitness < best.fitness:
		best=y
	iter+=1
	

print best