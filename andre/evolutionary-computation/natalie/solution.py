import csv
import numpy as np
import distutils.util as distutils

from acs.instance import Instance
from student import Student
# from fitness import FitnessValues


class Solution:
  def __init__(self, instance_file, studentsXselectedMaterials_file, studentsXfitness_file):
    self.instance = instance_file
    self.students_list = {'studentsXselectedMaterials_file': studentsXselectedMaterials_file,
                          'studentsXfitness_file': studentsXfitness_file}

  @property
  def instance(self):
    return self.__instance

  @instance.setter
  def instance(self, instance_file):
    self.__instance = Instance.load_from_file(instance_file)

  @property
  def students_list(self):
    return self.__students_list

  @students_list.setter
  def students_list(self, files):

    def generateSudentsFitnessList(studentsXfitness_file):
      students_fitness_values = list()
      with open(studentsXfitness_file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=' ')
        for row in csv_reader:
          fitness_list = list(map(float, row))
          students_fitness_values.append(fitness_list)
      csv_file.close()
      return students_fitness_values

    def generateMaterialsConcepts(materials):
      materials_hasConcepts = self.instance.concepts_materials.transpose()
      materials_concepts = list()

      for i, material in enumerate(materials):
        if material:
          materials_concepts.append(materials_hasConcepts[i])
        else:
          materials_concepts.append(
              np.zeros(len(materials_hasConcepts[i]), dtype=bool))

      return np.array(materials_concepts).astype(int)

    students_list = list()
    with open(files['studentsXselectedMaterials_file'], 'r') as csv_file:
      csv_reader = csv.reader(csv_file, delimiter=',')
      for row in csv_reader:
        student_id = int(int(row[0]) - 1)
        materials = list(map(lambda x: bool(distutils.strtobool(x)), row[1:]))
        materials_concepts = generateMaterialsConcepts(materials)
        student = Student(student_id, materials_concepts, np.array(materials))
        students_list.append(student)
    csv_file.close()

    students_fitness_values = generateSudentsFitnessList(files['studentsXfitness_file'])
    for student, fitness in zip(students_list, students_fitness_values):
      student.fitnessValues = fitness

    self.__students_list = students_list

  def __repr__(self):
    return f'----- Solution ------\n instance: {self.instance}\n students_materials_concepts: {self.students_list}\n'
