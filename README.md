# PSZT-cards-divider

## Problem
AE.4 Masz 10 kart ponumerowanych od 1 do 10. Znajdź przy użyciu algorytmu ewolucyjnego sposób na podział kart na dwie kupki w taki sposób, że suma kart na pierwszej kupce jest jak najbliższa wartości A, a suma kart na drugiej kupce jest jak najbliższa wartości B.

## Opis problemu
Problem podziału n kart można rozumieć jako problem przydziału jednej zgrup do każdej z kart.Algorytme wolucyjny ma pomóc efektywnie rozwiązać podany problem. Specyfikacja problemu sprowadza się do dwóch punktów: dysponujemy n kartami ponumerowanymi od 1 do n. Celem jest podział kart na dwie grupy takie, że suma numerów kart z pierwszej grupy jest jak najbardziej zbliżona wartości A, a suma numerów kart z drugiej grupy jak najbliższa wartości B. 


## Uruchamianie
Ze względu na wykorzystane narzędzia, niezbędne jest zainstalowanie interpretera języka Python w wersji 2.7 wraz z bibliotekami: numpy, pylab, matplotlib.

./src/uruchom strategy [selection] [crossover]
./src/solution.py strategy [selection] [crossover]

strategy ∈ { 1Plus1 ; 1Plus1Paralleled ; EvolutionaryProgramming ; MiPlusLambda ; MiLambda }
selection ∈ { RouletteSelection ; TournamentSelection ; RankingSelekction }
crossover ∈ { single-point ; two-point ; uniform }

Program uruchamia odpowiedni algorytm, a wyniki zapisuje w postaci wykresu o odpowiedniej dla wywołania nazwie.
Aby zmienić parametry algorytmów (mi, lambde, ilość kart) należy zmienić makro definicje w pliku solution.py.

## Kodowanie genotypu
Dla n kard o wartościach od 1 do n potrzebujemy n bitów. 
1 oznacza że dana karta jest w lewej grupie 0 w prawej

## Zaimplementowane srategie
* (1+1) 
* (1+1) zrównoleglony 
* (μ+λ) 
* (μ,λ) 
* Programowanie ewolucyjne

## Zaimplementowane metody selekcji
* Selekcja turniejowa
* Selekcja rankingowa
* Selekcja metodą koła ruletki

## Rodzaje krzyżowań
* Jednopunktowe
* Dwupunktowe
* Równomierne
