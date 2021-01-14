import numpy as np
from acs.instance import Instance
import acs.objective as objective
import os

import sys
np.set_printoptions(threshold=sys.maxsize)
dir = os.path.dirname(__file__)

class FitnessValues:
  file = os.path.join(dir,'..','instances','real','instance.txt')
  default_instance = Instance.load_from_file(file)

  def __init__(self, fitness_list):
    self.concepts_covered = fitness_list[0]
    self.difficulty = fitness_list[1]
    self.total_time = fitness_list[2]
    self.materials_balancing = fitness_list[3]
    self.learning_style = fitness_list[4]
    self.total = fitness_list[5]

  def __repr__(self):
    return f'---- FitnessValues ----\n concepts_covered: {self.concepts_covered}, difficulty: {self.difficulty}, total_time: {self.total_time}, materials_balancing: {self.materials_balancing}, learning_style: {self.learning_style}, total: {self.total} \n'

  @classmethod
  def concepts_covered_fn(cls, student_id, materials_concepts):
    # conceitos que foram indicados aos alunos
    objectives = cls.default_instance.objectives[student_id]

    all_covered_concepts = np.logical_or.reduce(materials_concepts).astype(int)
    over_covered_concepts = np.copy(all_covered_concepts)
    over_covered_concepts[objectives] = 0

    under_covered_concepts = objectives & (all_covered_concepts == 0)

    result = (over_covered_concepts.sum() + (FitnessValues.default_instance.missing_concepts_coeficient * under_covered_concepts.sum()))

    return result

  @classmethod
  def materials_balancing_fn(cls, student_id, materials_concepts):
    objectives = cls.default_instance.objectives[student_id].astype(bool)

    amount_of_materials_for_all_concepts = materials_concepts.astype(bool).sum()
    mean_concepts_per_objective = amount_of_materials_for_all_concepts / objectives.sum()

    amount_of_materials_per_objectives = materials_concepts.sum(axis=0)
    amount_of_materials_per_objectives = amount_of_materials_per_objectives[amount_of_materials_per_objectives != 0]

    # if(student_id == 5):
    #   print("amount_of_materials_for_all_concepts: ", materials_concepts.astype(bool))
    #   print("mean_concepts_per_objective: ", mean_concepts_per_objective)
    #   print("\n")

    distance_from_mean = np.abs(amount_of_materials_per_objectives - mean_concepts_per_objective)

    return distance_from_mean.sum()

  @staticmethod
  def get_Instance(materials_concepts):
    individual = list()
    for mat in materials_concepts:
      individual.append(False if mat.sum() == 0 else True)
    return individual

  @classmethod
  def fitness_fn(cls, student_id, materials_concepts):
    # concepts_covered_objective = cls.concepts_covered_fn(
    #     student_id, materials_concepts)
    # materials_balancing_objective = cls.materials_balancing_fn(
    #     student_id, materials_concepts)

    individual = FitnessValues.get_Instance(materials_concepts)

    concepts_covered_objective = objective.concepts_covered_function(individual, cls.default_instance, student_id)
    materials_balancing_objective = objective.materials_balancing_function(individual, cls.default_instance, student_id)

    sum_objective = (cls.default_instance.concepts_covered_weight * concepts_covered_objective + FitnessValues.default_instance.materials_balancing_weight * materials_balancing_objective)

    return sum_objective
