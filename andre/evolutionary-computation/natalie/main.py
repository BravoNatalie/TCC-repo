import os
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

from solution import Solution
from grasp import grasp
from problemDefinition import DiscreteOpt
from acs.instance import Instance
from report.report import createReport

dir = os.path.dirname(__file__)


new_repository = dict(zip(np.arange(0, 284), np.zeros(284, dtype=int)))
""" Novo repositório gerado com as modificações """

all_new_material = {
    "total": len(new_repository) - 1,
    "materials": []
}
""" materiais novos e o tamanho novo do repositório """


def add_to_allNewMaterial(covered_concepts, parent_material_id):
    """ adiciona um material novo se não existente """
    for mat in all_new_material["materials"]:
        if np.array_equal(covered_concepts, mat[1]):
            return mat
    
    id = all_new_material["total"] + 1
    material = (id, covered_concepts, parent_material_id)
    all_new_material["materials"].append(material)
    all_new_material["total"] += 1
    return material


def add_count_to_dict(dic, value):
    """ dicionário com contagem de value """
    if value in dic:
        dic[value] += 1
    else:
        dic[value] = 1
    return dic


instance_file = os.path.join(dir,'..','instances','real','instance.txt')

studentsXselectedMaterials_file = os.path.join(dir,'..', 'studentXselectedMaterials-02-06-2020.csv')

studentsXfitness_file = os.path.join(dir,'..', 'student_fitnessFunction-02-06-2020.csv')


""" --------------------------------------------------- """

""" Para cada estudante (materials_concepts) o grasp será chamado.
    Pois cada aluno tem objetivos diferentes e isso é um dos fatores analizados na geração do valor de fitness."""

initialSolution = Solution(instance_file, studentsXselectedMaterials_file, studentsXfitness_file)

improvedSolution = []

students_list_report = list()  # lista de alunos no formato exigido para imprimir o relatório

total_removed_materials = dict()  # key: material removido, value: quantidades de vezes 
total_added_materials = dict()  # key: material removido, value: quantidades de vezes  key: material adicionado, value: quantidades de vezes 
removed_materials_concepts = defaultdict(set)  # key: material removido, value: todos conceitos retirados
added_materials_concepts = defaultdict(set)  # key: material adicionado, value: todos conceitos adicionados 

for student in initialSolution.students_list:
    if(student.fitnessConcepts != 0.0):
        problem = DiscreteOpt(student)
        materials_concepts, fitness = grasp(problem, max_Iterations=100, alfa=0.8, seed=0)

        with open(os.path.join(dir,'iteration_log.txt'), 'a') as f:
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

                """ start: chart report """
                
                total_removed_materials = add_count_to_dict(total_removed_materials, material_id)

                if new_material.sum() > 0:
                    new_learning_material = add_to_allNewMaterial(new_material, material_id)
                    total_added_materials = add_count_to_dict(total_added_materials, new_learning_material[0])


                for concept in removed_concepts:
                    removed_materials_concepts[material_id].add(concept)
                
                for concept in added_concepts:
                    removed_materials_concepts[material_id].add(concept)
                
                """end:  chart report """
            # else:
            #     for index, mat in enumerate(materials_concepts):
            #         if materials_concepts[mat].sum() > 0:
            #             new_repository = add_count_to_dict(new_repository, index)

        student = {"student_id": student.student_id,
                   "fitness_before": student.fitnessConcepts,
                   "fitness_now": fitness,
                   "modified_materials": len(modified_materials),
                   "materials": modified_materials
                   }

        students_list_report.append(student)

    else:
        materials_concepts = student.materials_concepts

        """ start: counting frequency of use """
        # for index, mat in enumerate(materials_concepts):
        #     if materials_concepts[mat].sum() > 0:
        #         new_repository = add_count_to_dict(new_repository, index)
                
        """ end: counting frequency of use """


improvedSolution.append(materials_concepts)



y = list(total_removed_materials.keys())
x = list(total_removed_materials.values())

y1 = list(total_added_materials.keys())
x1 = list(total_added_materials.values())

filename = "Removed_Materials&Added_Materials.png"

fig, (ax1, ax2) = plt.subplots(1, 2)

ax1.barh(np.arange(len(y)), x, 0.6)
ax1.set_xticks(np.arange(min(x), 2 * max(x) + 1, 1))
ax1.set_yticks(np.arange(len(y)))
ax1.set_yticklabels(y)
ax1.set_ylabel('Removed Materials')
ax1.set_xlabel('Number of students')

ax2.barh(np.arange(len(y1)), x1, 0.3)
ax2.set_xticks(np.arange(min(x1), 2 * max(x1) + 1, 1))
ax2.set_yticks(np.arange(len(y1)))
ax2.set_yticklabels(y1)
ax2.set_ylabel('Added Materials')
ax2.set_xlabel('Number of students')
fig.tight_layout(pad=4.0)
plt.savefig(os.path.join(dir,'imagens',filename))


# for mat in new_repository:
#     if new_repository[mat] == 0:
#         print(mat)


# new_repository.update(total_added_materials)
# print(new_repository)
# print(len(new_repository))
# y2 = list(new_repository.keys())
# x2 = list(new_repository.values())
# fig, ax = plt.subplots()
# ax.barh(np.arange(len(y2)), x2, 0.0001)
# ax.set_xticks(np.arange(min(x2), max(x2) + 1, 1))
# ax.set_yticks(np.arange(len(y2)))
# ax.set_yticklabels(y2)
# plt.ylabel('Novo repositório')
# plt.xlabel('Quantidade de alunos')
# plt.savefig('./natalie/images/repositórioXquantidadeAlunos.png')

# create report

template_vars = {"total_students": 24, "students": students_list_report, "number_of_modified_students": len(students_list_report), "chart1": os.path.join(dir,'imagens',filename) }
filename = "grasp_report"

createReport(filename, template_vars)
