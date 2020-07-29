from solution import Solution
from problemDefinition import DiscreteOpt
from grasp import grasp
import numpy as np
from report.report import createReport


instance_file = '/home/bravo/Documents/TCC/TCC-repo/andre/evolutionary-computation/instances/real/instance.txt'

studentsXselectedMaterials_file = '/home/bravo/Documents/TCC/TCC-repo/andre/evolutionary-computation/studentXselectedMaterials-02-06-2020.csv'

studentsXfitness_file = '/home/bravo/Documents/TCC/TCC-repo/andre/evolutionary-computation/student_fitnessFunction-02-06-2020.csv'

""" --------------------------------------------------- """

""" Para cada estudante (materials_concepts) o grasp será chamado.
    Pois cada aluno tem objetivos diferentes e isso é um dos fatores analizados na geração do valor de fitness."""

initialSolution = Solution(instance_file, studentsXselectedMaterials_file, studentsXfitness_file)

improvedSolution = []

# student = initialSolution.students_list[14]

students_list_report = list()

for student in initialSolution.students_list:
    if(student.fitnessConcepts != 0.0):
        problem = DiscreteOpt(student)
        materials_concepts, fitness = grasp(problem, max_Iterations=100, alfa=0.8, seed=0)

        with open('iteration_log.txt', 'a') as f:
            print(f'------ Aluno: {student.student_id}', file=f)


        modified_materials = list()
        for index, material_zip in enumerate(zip(student.materials_concepts, materials_concepts)):
            old_material = material_zip[0]
            new_material = material_zip[1]

            removed_concepts = list()
            added_concepts = list()

            if not np.array_equal(old_material, new_material):
                material_id = index

                diff = new_material - old_material
                changed_concepts_index = np.where(diff != 0)[0]

                for conceito in changed_concepts_index:
                    mat = diff[conceito]
                    if(mat < 0):
                        removed_concepts.append(conceito)
                    else:
                        added_concepts.append(conceito)

                changed_material = {"material_id": material_id,
                                    "removed_concepts": removed_concepts,
                                    "added_concepts": added_concepts
                                    }
                            
                modified_materials.append(changed_material)

        student = {"student_id": student.student_id,
                   "fitness_before": student.fitnessConcepts,
                   "fitness_now": fitness,
                   "modified_materials": len(modified_materials),
                   "materials": modified_materials
                   }

        students_list_report.append(student)

    else:
        materials_concepts = student.materials_concepts

improvedSolution.append(materials_concepts)

# create report

template_vars = {"total_students": 24, "students": students_list_report, "number_of_modified_students": len(students_list_report)}
filename = "grasp_report"

createReport(filename, template_vars)
