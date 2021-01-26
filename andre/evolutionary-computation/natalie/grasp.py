import os
import numpy as np
from problemDefinition import DiscreteOpt

dir = os.path.dirname(__file__)

def grasp(problem, max_Iterations, alfa, seed):
  bestSolution = problem.representation
  bestFitness = problem.fitness
  iters = 0
  while bestFitness > 0.0 and iters < int( max_Iterations / 2 ):
    iters += 1
    solution, solution_fitness = greadyRandomizedConstruction(problem, alfa, seed)
    newProblem = DiscreteOpt(solution)
    newSolution, newSolution_fitness = hill_climb(newProblem, int( max_Iterations / 2 ))
    """ Update best solution: """
    availableSolutions = {bestFitness: bestSolution,
                          solution_fitness: solution,
                          newSolution_fitness: newSolution }

    bestFitness = min(availableSolutions)
    bestSolution = availableSolutions[bestFitness]

  with open(os.path.join(dir,'iteration_log.txt'), 'a') as f:
    print(f'GRASP - Iterações: {iters}', file=f)

  return bestSolution, bestFitness


def greadyRandomizedConstruction(problem, alfa, seed):
  # solution = []

  problem.find_neigthbors()  # TODO: retornar apenas os vizinhos possíveis
  allCandidateSolutions = np.append([problem.state], problem.neighborhood, axis=0)

  # for index in range(allCandidateSolutions.shape[0]):
  minCost = problem.minCost()
  maxCost = problem.maxCost()
  qualityThreshold = minCost + alfa * (maxCost - minCost)

  # lista restrita de canditados: melhores lenRCS candidatos da lista de todos candidatos
  restrictedCandidateSolutions = [candidate for candidate in allCandidateSolutions if candidate.fitnessConcepts <= qualityThreshold]

  # seleção aleatória de uma solução da lista restrita de candidatos
  np.random.seed(seed)
  randomSolutionIndex = np.random.randint(0, len(restrictedCandidateSolutions), 1)[0]
  randomSolution = np.take(restrictedCandidateSolutions, randomSolutionIndex)

  # Solution = Solution U {randomSolution}
  # solution.append(randomSolution)

  # update lista de todos candidatos
  # allCandidateSolutions = allCandidateSolutions[allCandidateSolutions != randomSolution]

  # update lista de custos
  # candidatesCost = np.delete(candidatesCost, randomSolutionIndex)

  return randomSolution, randomSolution.fitnessConcepts


def hill_climb(problem, max_iterations):
  best_solution = problem.representation
  best_fitness = problem.fitness
  iters = 0

  while best_fitness > 0.0 and iters < max_iterations:
    iters += 1
    problem.find_neigthbors()
    next_solution = problem.minCost_neighbor()
    next_fitness = next_solution.fitnessConcepts

    # If best neighbor is an improvement, move to that state
    if next_fitness < best_fitness:
        best_solution = next_solution.materials_concepts
        best_fitness = next_fitness
    
    problem = DiscreteOpt(next_solution)


  with open(os.path.join(dir,'iteration_log.txt'), 'a') as f:
    print(f'hillClimb - Iterações: {iters}', file=f)

  return best_solution, best_fitness
