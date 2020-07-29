from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML


def createReport(filename, template_vars):
    env = Environment(loader=FileSystemLoader(searchpath="./natalie/report"))
    template = env.get_template("template.html")
    
    html_out = template.render(template_vars)
    HTML(string=html_out).write_pdf("./natalie/report/" + filename + ".pdf", stylesheets=["./natalie/report/styles.css"])


if __name__ == "__main__":
    template_vars = {"total_students": 1, "students": [{"student_id": 1, "fitness_before": 5, "fitness_now": 0, "modified_materials": 2, "materials": [{"material_id": 11, "removed_concepts": ['Logica'], "added_concepts": ['Calculo', 'Prog']}]}], "number_of_modified_students": 1}
    filename = "grasp_report"

    createReport(filename, template_vars)
