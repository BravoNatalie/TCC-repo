from solution import Solution
from problemDefinition import DiscreteOpt
from grasp import grasp
import numpy as np
# from fitness import FitnessValues


instance_file = '/home/bravo/Documents/TCC/TCC-repo/andre/evolutionary-computation/instances/real/instance.txt'

studentsXselectedMaterials_file = '/home/bravo/Documents/TCC/TCC-repo/andre/evolutionary-computation/studentXselectedMaterials-02-06-2020.csv'

studentsXfitness_file = '/home/bravo/Documents/TCC/TCC-repo/andre/evolutionary-computation/student_fitnessFunction-02-06-2020.csv'

""" --------------------------------------------------- """

""" Para cada estudante (materials_concepts) o grasp será chamado.
    Pois cada aluno tem objetivos diferentes e isso é um dos fatores analizados na geração do valor de fitness."""

initialSolution = Solution(instance_file, studentsXselectedMaterials_file, studentsXfitness_file)

improvedSolution = []

# student = initialSolution.students_list[14]

for student in initialSolution.students_list:
    if(student.fitnessConcepts != 0.0):
        problem = DiscreteOpt(student)
        materials_concepts, fitness = grasp(problem, max_Iterations=10, alfa=0.8, seed=0)
        print(f'------ Aluno: {student.student_id}')
        if(np.array_equal(student.materials_concepts, materials_concepts)):
            print('same initial solution')
        else:
            print('different solution found!')
        materials_per_concepts_before = student.materials_concepts.sum(axis=0)
        materials_per_concepts_now = materials_concepts.sum(axis=0)
        diff = materials_per_concepts_before - materials_per_concepts_now
        changed_concepts_index = np.where(diff != 0)[0]
        for i in changed_concepts_index:
            mat = diff[i]
            print(f'Conceito: {i}')
            if(mat > 0):
                print(f'\tmateriais removidos: {mat}')
            else:
                print(f'\tmateriais adicionados: {mat}')
        # print(f'BEFORE -> materials per concepts: {materials_per_concepts_before}')
        # print(f'   NOW -> materials per concepts: {materials_per_concepts_now}')
        print(f'BEFORE -> fitness: {student.fitnessConcepts}')
        print(f'   NOW -> fitness: {fitness}')
    else:
        materials_concepts = student.materials_concepts
    
improvedSolution.append(materials_concepts)
