import random
from abc import abstractmethod
from objects import Starter

class GeneticAlgorithmSearch:
    def __init__(self):
        self.num_generations = 1000
        self._current_population = []
        self.mutation_rate = 10  # 10%
        self.salary_cap=70000000

    @abstractmethod
    def _generate_initial_population(self):
        raise NotImplementedError

    @abstractmethod
    def do_crossover(self, chromosome1, chromosome2):
        raise NotImplementedError

    @abstractmethod
    def do_mutation(self, chromosome):
        raise NotImplementedError

    @abstractmethod
    def evaluate_chromosome(self, chromosome):
        raise NotImplementedError

    def __create_probabalistic_population_for_pick(self):
        #Devuelve un quinteto de 5 jugadores
        to_return = []
        #Chromosome = Starter
        for position, chromosome in enumerate(self._current_population):
            to_return.extend([chromosome]*position)
        return to_return

    def run_search(self):
        self._current_population = self._generate_initial_population()
        for _ in range(self.num_generations):
            # Evaluate
            self._current_population.sort(key=self.evaluate_chromosome)
            self._best_so_far = self._current_population[-1]
            # Creating new population
            new_population = []
            # Copy best over if needed
            new_population.append(self._best_so_far)
            # Filling the rest
            probabilistic_population_for_mating = self.__create_probabalistic_population_for_pick()
            while len(new_population) < len(self._current_population):
                parent1 = random.choice(probabilistic_population_for_mating)
                parent2 = random.choice(probabilistic_population_for_mating)
                # Performing crossover
                child = self.do_crossover(parent1, parent2)
                # Performing mutation
                child = self.do_mutation(child)
                # Ensuring child is good
                if self.check_ok(child):
                    continue

                new_population.append(child)

            self._current_population = new_population

    def get_result(self):
        return self._best_so_far


    def check_ok(self, starter: Starter) -> bool:
        """
        Comprobar que:
            1. NO se sobrepasa el límite salarial.
            2. Hay un jugador por posición.
        """
        return not (
            sum(player.salary for player in starter) < self.salary_cap
            and self.count_position(1,starter) == 1
            and self.count_position(2,starter) == 1
            and self.count_position(3,starter) == 1
            and self.count_position(4,starter) == 1
            and self.count_position(5,starter) == 1
            and len(set(starter)) == 5
        )

    def count_position(self, position: int, starter: Starter) -> bool:
            return sum(player.position == position for player in starter)