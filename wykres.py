import sys
import matplotlib
import pylab
"""
def main(argv):

	plik = open("result.txt", "r")
	liczby = []
	srednia = []
	a = 0
	for val in plik.read().split():
		if a%2 == 0:
			liczby.append(int(val))
		else:
			srednia.append(float(val))
		a += 1
	plik.close()
	x = range(0, len(liczby) )
	m = max(srednia)


	
	pylab.plot(liczby, srednia, 'r')
	pylab.xlabel('Liczba kart')
	pylab.ylabel('Czas dzialania algorytmu')
	pylab.title('Algorytm zachlanny')
	pylab.grid(True)
	pylab.savefig('zachlanny.png')

	return
	
if __name__ == "__main__":
	main(sys.argv[1:])

"""
def main(argv):

	plik = open(argv[0]+"_result.txt", "r")
	liczby = []
	srednia = []
	a = 0
	for val in plik.read().split():
		if a%2 == 0:
			liczby.append(int(val))
		else:
			srednia.append(float(val))
		a += 1
	plik.close()
	x = range(0, len(liczby) )
	m = max(srednia)


	
	pylab.plot(x,liczby, 'r', x, srednia, 'b')
	pylab.legend(['Najlepszy', 'Srednia'])
	pylab.xlabel('Kolejne populacje')
	pylab.ylabel('Funkcja przystosowania')
	pylab.title(argv[0])
	pylab.grid(True)
	pylab.ylim((-2, m+3))
	pylab.savefig(argv[0] + '.png')

	return
	
if __name__ == "__main__":
	main(sys.argv[1:])
