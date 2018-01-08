#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
'''
TT.AE.4
Masz 10 kart ponumerowanych od 1 do 10. Znajdź przy użyciu algorytmu ewolucyjnego 
sposób na podział kart na dwie kupki w taki sposób, że suma kart na pierwszej kupce jest jak 
najbliższa wartości A, a suma kart na drugiej kupce jest jak najbliższa wartości B.
'''

__author__ = "Rafał Koguciuk adn Bartosz Rajkowski and Piotr Frysz"
__version__ = "1.0.0"
__maintainer__ = "Tomasz Trzciński"

import sys
import random
import phenotype
import generation
import math

NUMBER_OF_CARDS = 50
SUM_A = 320
SUM_B = 955
CROSSOVER_PROBABILITY = 0.8
MUTATION_PROBABILITY = 0.03
MAX_ITERATIONS = 30
MI=10
LAMBDA=12


def find_solution():
	g = OnePlusOneStrategy()
	print "1 + 1 Strategy:\nBefore:"
	print g
	while g.num_iterations < g.max_iterations:

		if g.population[0].fitness == 0:
			break
		g.step()
	print "After:",g.num_iterations, "iterations:\n",g

	
	print "\nmi plus lambda Strategy:\nBest before:\n" 
	h = MiPlusLambdaStrategy(MI, LAMBDA, "RouletteSelection","single-point")
	while h.get_best().fitness == 0:
		h = MiPlusLambdaStrategy(MI, LAMBDA, "RouletteSelection","single-point")

	#print h.get_best()
	while h.num_iterations < h.max_iterations:

		if h.get_best().fitness == 0:
			break
		h.step()

	print "\nBest after:",h.num_iterations, "iterations:\n", h.get_best()
	
	
	
	print "\nmi lambda Strategy:\nBest before:\n" 
	h = MiLambdaStrategy(MI, LAMBDA, "RouletteSelection","single-point")
	while h.get_best().fitness == 0:
		h = MiLambdaStrategy(MI, LAMBDA, "RouletteSelection","single-point")

	#print h.get_best()
	while h.num_iterations < h.max_iterations:

		if h.get_best().fitness == 0:
			break
		h.step()

	print "\nBest after:",h.num_iterations, "iterations:\n", h.get_best()




def main(argv):
	
	# Parser
	parser = argparse.ArgumentParser()
	#parser.add_argument("-i", "--input", help="bla bla bla", type=str, required=True)
    args = vars(parser.parse_args())

    # find solution
    find_solution()

if __name__ == "__main__":
	main(sys.argv[1:])
