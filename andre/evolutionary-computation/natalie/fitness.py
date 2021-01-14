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

  @staticmethod
  def get_Instance(materials_concepts):
    individual = list()
    for mat in materials_concepts:
      individual.append(False if mat.sum() == 0 else True)
    return individual

  @classmethod
  def fitness_fn(cls, student_id, materials_concepts):
    individual = FitnessValues.get_Instance(materials_concepts)

    concepts_covered_objective = objective.concepts_covered_function(individual, cls.default_instance, student_id)
    materials_balancing_objective = objective.materials_balancing_function(individual, cls.default_instance, student_id)

    sum_objective = (cls.default_instance.concepts_covered_weight * concepts_covered_objective + FitnessValues.default_instance.materials_balancing_weight * materials_balancing_objective)

    return sum_objective
