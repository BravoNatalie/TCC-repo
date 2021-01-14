from fitness import FitnessValues


class Student:
  """ 
  Classe para representar o aluno

  Attributes
  ----------
  student_id: int
    id de identificação do aluno
  materials_concepts: numpy.array int
    array de duas dimensões materiaisXconceitos, com os valores pertencentes à {0,1}
  materials: numpy.array boolean
    array de materiais indicados ao aluno, 1 para recomendado e 0 caso contrário
  fitnessValues: list float
    lista contento os valores das funcções de fitness: [concepts_covered, difficulty, total_time, materials_balancing, learning_style, total]
  fitnessConcepts: float
    valor associado às funções concepts_covered e materials_balancing

  """

  def __init__(self, student_id, materials_concepts, materials):
    self.student_id = student_id
    self.materials_concepts = materials_concepts
    self.materials = materials
    self.fitnessValues = [0] * 6
    self.fitnessConcepts = FitnessValues.fitness_fn(student_id, materials_concepts)

  @property
  def student_id(self):
    return self.__student_id

  @student_id.setter
  def student_id(self, student_id):
    if student_id < 0:
      raise Exception('Student Id below 0 is not possible')
    self.__student_id = student_id

  @property
  def materials_concepts(self):
    return self.__materials_concepts

  @materials_concepts.setter
  def materials_concepts(self, materials_concepts):
    if materials_concepts.ndim != 2 or type(materials_concepts[0][0].item()) != int:
      raise Exception(
          f'{materials_concepts} needs to be a binary numpy array of dimension two.')
    self.__materials_concepts = materials_concepts

  @property
  def materials(self):
    return self.__materials

  @materials.setter
  def materials(self, materials):
    if materials.ndim != 1 or type(materials[0].item()) != bool:
      raise Exception(
          f'{materials} needs to be a boolean numpy array of dimension one')
    self.__materials = materials

  @property
  def fitnessConcepts(self):
    return self.__fitnessConcepts

  @fitnessConcepts.setter
  def fitnessConcepts(self, val):
    self.__fitnessConcepts = val

  @property
  def fitnessValues(self):
    return self.__fitnessValues

  @fitnessValues.setter
  def fitnessValues(self, fitness_list):
    self.__fitnessValues = FitnessValues(fitness_list)

  def getSelectedConcepts(self):
    selectedConcepts = self.materials_concepts.any(axis=0).astype(int)
    return selectedConcepts

  def __repr__(self):
    return f'---- Student ---- \n student_id: {self.student_id} \n materials_concepts: {self.materials_concepts} \n materials: {self.materials} \n fitnessValues: {self.fitnessValues}\n fitnessConcepts: {self.fitnessConcepts}\n'
