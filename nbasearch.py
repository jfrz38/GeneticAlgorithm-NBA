import random
from abc import abstractmethod
from objects import Starter

class GeneticAlgorithmSearch:
    def __init__(self):
        self.n_iteraciones = 10000
        self.poblacion_actual = []
        self.probabilidad_mutacion = 10  # 10%
        self.limite_salarial=70000000

    @abstractmethod
    def generar_poblacion_inicial(self):
        raise NotImplementedError

    @abstractmethod
    def realizar_crossover(self, chromosome1, chromosome2):
        raise NotImplementedError

    @abstractmethod
    def realizar_mutacion(self, chromosome):
        raise NotImplementedError

    def evaluate_chromosome(self, starter: Starter) -> float:
        return sum(player.adjusted_production for player in starter)

    def crear_poblacion_a_elegir(self):
        #Devuelve un quinteto de 5 jugadores
        #Cromosoma = Starter
        to_return = []
        for position, chromosome in enumerate(self.poblacion_actual):
            to_return.extend([chromosome]*position)
        return to_return

    def iniciar_busqueda(self):
        self.poblacion_actual = self.generar_poblacion_inicial()
        for _ in range(self.n_iteraciones):
            # Evaluación: Ordenar por valor de la producción.
            # El jugador con peor producción estará en la última posición.
            # Se utilizan los 4 jugadores restantes como "mejor quinteto"
            self.poblacion_actual.sort(key=self.evaluate_chromosome)
            self.mejores_genes  = self.poblacion_actual[-1]
            # Crear la nueva población con los 4 mejores anteriores
            nueva_poblacion = []
            nueva_poblacion.append(self.mejores_genes )
            # Añadir el último jugador
            poblacion_a_elegir = self.crear_poblacion_a_elegir()
            while(True):
                parent1 = random.choice(poblacion_a_elegir)
                parent2 = random.choice(poblacion_a_elegir)
                # Crossover
                child = self.realizar_crossover(parent1, parent2)
                # Mutación
                child = self.realizar_mutacion(child)
                # Comprobar que el hijo generado es correcto
                if not self.comprobar(child):
                    continue
                else:
                    nueva_poblacion.append(child)
                    break
            self.poblacion_actual = nueva_poblacion

    def obtener_resultado(self):
        if self.comprobar(self.mejores_genes ):
            return self.mejores_genes 
        else:
            return []


    def comprobar(self, starter: Starter) -> bool:
        """
        Comprobar que:
            1. NO se sobrepasa el límite salarial.
            2. Hay un jugador por posición.
        """
        return (
            sum(player.salary for player in starter) < self.limite_salarial
            and self.count_position(1,starter) == 1
            and self.count_position(2,starter) == 1
            and self.count_position(3,starter) == 1
            and self.count_position(4,starter) == 1
            and self.count_position(5,starter) == 1
            and len(set(starter)) == 5
        )

    def count_position(self, position: int, starter: Starter) -> bool:
            return sum(player.position == position for player in starter)