import csv
import random

from nbasearch import GeneticAlgorithmSearch
from objects import *

class NBASearch(GeneticAlgorithmSearch):
    def __init__(self, filename: str, population_size=20):
        GeneticAlgorithmSearch.__init__(self)
        self._population_size = population_size
        self._all_players = generateDataFromCSV(filename)
        self.bases_list = [x for x in self._all_players if x.position == 1]
        self.escoltas_list = [x for x in self._all_players if x.position == 2]
        self.aleros_list = [x for x in self._all_players if x.position == 3]
        self.alapivots_list = [x for x in self._all_players if x.position == 4]
        self.pivots_list = [x for x in self._all_players if x.position == 5]
        self.position_to_player_list_map = {
            1: self.bases_list,
            2: self.escoltas_list,
            3: self.aleros_list,
            4: self.alapivots_list,
            5: self.pivots_list,
        }

    def generar_poblacion_inicial(self) -> [Starter]:
        population = []
        for _ in range(self._population_size):
            starter = [random.choice(self.bases_list)]
            starter.append(random.choice(self.escoltas_list))
            starter.append(random.choice(self.aleros_list))
            starter.append(random.choice(self.alapivots_list))
            starter.append(random.choice(self.pivots_list))
            population.append(Starter(starter))
        return population

    @staticmethod
    def __find_player_to_replace(starter: Starter, position: str) -> Player:
        players_of_position = {player for player in starter if player.position == position}
        for player in players_of_position:
            if starter.count(player) > 1:
                return player
        raise ValueError("Unable to find duplicate players in starter!")

    def realizar_crossover(self, padre1: Starter, padre2: Starter) -> Starter:
        indice_crossover = random.randint(0, len(padre1))
        new_starter = Starter(padre1[:indice_crossover] + padre2[indice_crossover:])
        return new_starter


    def realizar_mutacion(self, starter: Starter) -> Starter:
        for index, player in enumerate(starter):
            if random.randint(0, 100) < self.probabilidad_mutacion:
                # picking new random player of same position not already in starter
                starter[index] = self.jugador_aleatorio(starter, player.position)
        return starter

    def jugador_aleatorio(self, starter: Starter, position: str):
        return random.choice(list(set(self.position_to_player_list_map[position]).difference({p for p in starter if p.position == position})))

'''
Asegurarse que los jugadores sin datos no manchan el resultado.
Si un jugador no tiene información de producción esperada o salario se pone:
    - Salario = 100 veces el tope salarial:
        Así se evita que con un valor de 0 el algoritmo lo cuente como una buena opción ya que no gasta dinero
    - Producción = 0
        Así se evita que la producción sea alta y se considere buena opción.
'''
def calculate_salary(column):    
    return int(70000000*100) if column == '' else  float(column)
def calculate_points(column):
    return float(0) if column == '' else  float(column)
def calculate_position(column):
    return int(1) if column == '' else int(column)

def generateDataFromCSV(filename: str) -> [Player]:
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        return [
            Player(
                name=row['player'],
                salary = calculate_salary(row['truesalary']),
                adjusted_production=calculate_points(row['adjusted_production']),
                team=row['tm'],
                position = calculate_position(row['rounded_position'])
            )
            for row in reader
            ]

if __name__ == '__main__':
    nbasearch = NBASearch('nba-list-2016.csv')
    nbasearch.iniciar_busqueda()
    mejor_quinteto = nbasearch.obtener_resultado()
    if(len(mejor_quinteto)>0):
        print('Mejor quinteto: {} puntos por ${}'.format(sum(player.adjusted_production for player in mejor_quinteto)/1000,sum(player.salary for player in mejor_quinteto)))
        for player in mejor_quinteto:
            print(player)
    else:
        print("No se ha podido encontrar ningún quinteto")
