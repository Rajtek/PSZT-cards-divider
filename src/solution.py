#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
'''
TT.AE.4
Masz 10 kart ponumerowanych od 1 do 10. Znajdź przy użyciu algorytmu ewolucyjnego 
sposób na podział kart na dwie kupki w taki sposób, że suma kart na pierwszej kupce jest jak 
najbliższa wartości A, a suma kart na drugiej kupce jest jak najbliższa wartości B.
'''

__author__ = "Rafał Koguciuk and Bartosz Rajkowski and Piotr Frysz"
__version__ = "1.0.0"
__maintainer__ = "Tomasz Trzciński"

import sys
import random
import phenotype
import generation
import math

NUMBER_OF_CARDS = 1000
SUM_A = 124951
SUM_B = 375549
CROSSOVER_PROBABILITY = 0.8
MUTATION_PROBABILITY = 0.04
MAX_ITERATIONS = 1000
MI=40
LAMBDA=50
MIN = 11

def find_solution(argv):
	while True:
		genotype = phenotype.Phenotype(size = NUMBER_OF_CARDS)
		genotype.calc_fitness_function(SUM_A, SUM_B)
		if genotype.fitness > MIN:
			break;
	if len(argv) == 0:
		print "First  parameter like: 1Plus1 or 1Plus1Paralleled or EvolutionaryProgramming or MiPlusLambda or MiLambda!"
		return 
	if  argv[0]!= "1Plus1"   and argv[0]!="1Plus1Paralleled" and argv[0]!="EvolutionaryProgramming" and argv[0]!= "MiPlusLambda" and	argv[0]!= "MiLambda":
		print "First  parameter like: 1Plus1 or 1Plus1Paralleled or EvolutionaryProgramming or MiPlusLambda or MiLambda!"
	
	if argv[0]=="MiPlusLambda" or argv[0]== "MiLambda":
		if len(argv) == 1:
			print "Second parameter like: RouletteSelection or TournamentSelection or RankingSelection!"
			return
		if argv[1]== "RouletteSelection" or argv[1]== "TournamentSelection" or argv[1]== "RankingSelection":
			if len(argv) == 2:
				argv.append("single-point")
			if argv[2] != "single-point" and argv[2]!= "two-point" and argv[2]!= "uniform":
				print "Third parameter like: single-point or two-point or uniform!"
				return
		else:
			print "Second parameter like: RouletteSelection or TournamentSelection or RankingSelection!"
			return
				
			
			
	if argv[0] == "1Plus1":
		h = generation.OnePlusOneStrategy(genotype.genotype)	
		#print "\n",argv[0],"strategy:\nBest before:", h.get_best().fitness
		print h.get_best().fitness
		print h.get_avg_fitness()
		while h.num_iterations < h.max_iterations:
			h.step()
			print h.get_best().fitness
			print h.get_avg_fitness()
			if h.population[0].fitness < MIN:
				break
		#print "Best after: ",h.population[0].fitness, ". Iterations:", h.num_iterations, "\n"
	
	if argv[0] == "1Plus1Paralleled":
		h = generation.OnePlusOneParalleledStrategy(MI,genotype.genotype)
		#print "\n",argv[0], "strategy:\nBest before:", h.get_best().fitness
		print h.get_best().fitness
		print h.get_avg_fitness()
		while h.num_iterations < h.max_iterations:
			h.step()
			print h.get_best().fitness
			print h.get_avg_fitness()
			if h.population[0].fitness < MIN:
				break
		#print "Best after: ",h.population[0].fitness, ". Iterations:", h.num_iterations, "\n"
	
	if argv[0] == "MiPlusLambda":
		h = generation.MiPlusLambdaStrategy(MI, LAMBDA, argv[1],argv[2])
		while h.get_best().fitness < MIN + 1:
			h = generation.MiPlusLambdaStrategy(MI, LAMBDA, argv[1],argv[2])
		#print "\n", argv[0], argv[1], argv[2], "\nBest before:", h.get_best().fitness
		print h.get_best().fitness
		print h.get_avg_fitness()
		while h.num_iterations < h.max_iterations:
			h.step()
			print h.get_best().fitness
			print h.get_avg_fitness()
			if h.population[0].fitness < MIN:
				break
		#print "Best after: ",h.population[0].fitness, ". Iterations:", h.num_iterations, "\n"
	

	if argv[0] == "MiLambda":
		h = generation.MiLambdaStrategy(MI, LAMBDA, argv[1],argv[2])
		while h.get_best().fitness < MIN + 1:
			h = generation.MiLambdaStrategy(MI, LAMBDA, argv[1],argv[2])
		#print "\n", argv[0], "strategy",argv[1], argv[2], "\nBest before:", h.get_best().fitness
		print h.get_best().fitness
		print h.get_avg_fitness()
		while h.num_iterations < h.max_iterations:
			h.step()
			print h.get_best().fitness
			print h.get_avg_fitness()
			if h.population[0].fitness < MIN:
				break
		#print "Best after: ",h.population[0].fitness, ". Iterations:", h.num_iterations, "\n"
	
	
	if argv[0] == "EvolutionaryProgramming":
		h = generation.EvolutionaryProgrammingStrategy(MI)	
		while h.get_best().fitness < MIN + 1:
			h = generation.EvolutionaryProgrammingStrategy(MI)
		#print "\n", argv[0], "strategy", argv[1], argv[2], "\nBest before:", h.get_best().fitness 
		print h.get_best().fitness
		print h.get_avg_fitness()
		while h.num_iterations < h.max_iterations:
			h.step()
			print h.get_best().fitness
			print h.get_avg_fitness()
			if h.population[0].fitness < MIN:
				break
		#print "Best after: ",h.population[0].fitness, ". Iterations:", h.num_iterations, "\n"

	return
def main(argv):
	
	# find solution
	find_solution(argv)

if __name__ == "__main__":
	main(sys.argv[1:])
