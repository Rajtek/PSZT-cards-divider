# PSZT-cards-divider

## Uruchamianie
./uruchum strategia metodaSelekcji metodaKrzyżowania

strategia ∈ { 1Plus1 ; 1Plus1Paralleled ; EvolutionaryProgramming ; MiPlusLambda ; MiLambda } \n
metodaSelekcji ∈ { RouletteSelection ; TournamentSelection ; RankingSelekction } \n
metodaKrzyżowania ∈ { single-point ; two-point ; uniform }

Program uruchamia odpowiedni algorytm, a wyniki zapisuje w postaci wykresu o odpowiedniej dla wywołania nazwie.
Aby zmienić parametry algorytmów (mi, lambde, ilość kart) należy zmienić makro definicje w pliku solution.py.

## Kodowanie genotypu
Dla n kard o wartościach od 1 do n potrzebujemy n bitów. 
1 oznacza że dana karta jest w lewej grupie
0 w prawej

## TODO
* strategia elitarna ( chyba nie bedziemy robić )
* sposób testowania
* dokumentacja
* ...


## Zrobione
* (1+1) ✓
* (1+1) zrównoleglony ✓
* (μ+λ) ✓
* (μ,λ) ✓
* różne strategie selekcji  ✓
* różne sposoby krzyżowania ✓
* programowanie ewolucyjne  ✓
