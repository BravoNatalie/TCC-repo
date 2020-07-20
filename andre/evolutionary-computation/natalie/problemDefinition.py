import numpy as np
from student import Student


class OptimizationProblem:
  def __init__(self, student):
    self.state = student
    self.representation = student.materials_concepts
    self.fitness = student.fitnessConcepts
    self.shape = student.materials_concepts.shape
    self.neighborhood = []

  
  def __neighborhood_fitness_list(self):
    fitness_list = []
    for neighbor in self.neighborhood:
      fitness_list.append(neighbor.fitnessConcepts)
    return fitness_list
  
  def minCost_neighbor(self):
    """Return the neighbor with minimal cost of current state."""
    fitness_list = self.__neighborhood_fitness_list()
    best = self.neighborhood[np.argmin(fitness_list)]
    return best
  
  def minCost(self):
    min_neighbor = self.minCost_neighbor()
    if min_neighbor.fitnessConcepts < self.fitness:
      return min_neighbor.fitnessConcepts
    else:
      return self.fitness
  
  def maxCost_neighbor(self):
    fitness_list = self.__neighborhood_fitness_list()
    best = self.neighborhood[np.argmax(fitness_list)]
    return best

  def maxCost(self):
    max_neighbor = self.maxCost_neighbor()
    if max_neighbor.fitnessConcepts > self.fitness:
      return max_neighbor.fitnessConcepts
    else:
      return self.fitness


  def __repr__(self):
    return f'---- OptimizationProblem -----\n state: {self.state}, representation: {self.representation}, neighborhood: {self.neighborhood}, fitness: {self.fitness}, shape: {self.shape} \n'


class DiscreteOpt(OptimizationProblem):
  def __init__(self, state):
    OptimizationProblem.__init__(self, state)

  def find_neigthbors(self):
    """Find all neighbors of the current state. """
    self.neighborhood = []

    for i in range(self.shape[0]):
      for j in range(self.shape[1]):
        representation = np.copy(self.representation)
        representation[i][j] = np.abs(representation[i][j] - 1)
        neighbor = Student(self.state.student_id, representation, self.state.materials)
        self.neighborhood.append(neighbor)

  def random_neighbor(self):
    """Return random neighbor of current state vector."""
    representation = np.copy(self.representation)
    i = np.random.randint(0, self.shape[0])
    j = np.random.randint(0, self.shape[1])
    representation[i][j] = np.abs( representation[i][j] - 1)

    return Student(self.state.student_id, representation, self.state.materials)
