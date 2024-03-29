import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
import csv
import os
from PIL import Image, ImageTk

class ProyectosWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Proyectos")
        self.root.geometry("800x600")

        # Frame principal
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        # Obtener la ruta del directorio actual
        current_dir = os.path.dirname(__file__)

        # Cargar iconos
        create_icon = Image.open(os.path.join(current_dir, "icons/createp_icon.png")).resize((32, 32))
        assign_icon = Image.open(os.path.join(current_dir, "icons/assignp_icon.png")).resize((32, 32))
        progress_icon = Image.open(os.path.join(current_dir, "icons/progressp_icon.png")).resize((32, 32))

        # Convertir iconos a formato PhotoImage
        self.create_icon = ImageTk.PhotoImage(create_icon)
        self.assign_icon = ImageTk.PhotoImage(assign_icon)
        self.progress_icon = ImageTk.PhotoImage(progress_icon)

        # Frame para la selección de opciones
        self.options_frame = ttk.LabelFrame(self.main_frame, text="Opciones")
        self.options_frame.pack(fill="both", expand=True, padx=20, pady=20)

        ttk.Button(self.options_frame, text="Crear Proyecto", image=self.create_icon, compound=tk.LEFT, command=self.create_project).pack(side="left", padx=10, pady=10)
        ttk.Button(self.options_frame, text="Asignar Miembros", image=self.assign_icon, compound=tk.LEFT, command=self.assign_members).pack(side="left", padx=10, pady=10)
        ttk.Button(self.options_frame, text="Seguimiento del Progreso", image=self.progress_icon, compound=tk.LEFT, command=self.show_progress).pack(side="left", padx=10, pady=10)

        # Frame para crear proyecto
        self.create_project_frame = ttk.LabelFrame(self.main_frame, text="Crear Proyecto")
        ttk.Button(self.create_project_frame, text="Crear Proyecto", command=self.save_project).pack(pady=10)
        ttk.Label(self.create_project_frame, text="Título del Proyecto:").pack(pady=5)
        self.project_title_entry = ttk.Entry(self.create_project_frame)
        self.project_title_entry.pack(fill="x", padx=5, pady=5)

        ttk.Label(self.create_project_frame, text="Objetivo General:").pack(pady=5)
        self.project_objectives_entry = ttk.Entry(self.create_project_frame)
        self.project_objectives_entry.pack(fill="x", padx=5, pady=5)

        ttk.Label(self.create_project_frame, text="Fecha Inicial:").pack(pady=5)
        self.start_date_calendar = Calendar(self.create_project_frame, selectmode='day', date_pattern='dd/mm/yyyy', width=12, height=8)
        self.start_date_calendar.pack(fill="x", padx=5, pady=5)

        ttk.Label(self.create_project_frame, text="Fecha Final:").pack(pady=5)
        self.end_date_calendar = Calendar(self.create_project_frame, selectmode='day', date_pattern='dd/mm/yyyy', width=12, height=8)
        self.end_date_calendar.pack(fill="x", padx=5, pady=5)

        # Lista para almacenar los nombres de los alumnos asignados al proyecto
        self.assigned_students = []

        # Frame para asignar miembros del equipo
        self.assign_members_frame = ttk.LabelFrame(self.main_frame, text="Asignar Miembros del Equipo")
        self.project_selection_frame = ttk.LabelFrame(self.assign_members_frame, text="Seleccionar Proyecto")
        self.project_selection_frame.grid(row=0, column=0, padx=10, pady=10)
        self.projects_combo = ttk.Combobox(self.project_selection_frame, state="readonly")
        self.projects_combo.grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(self.project_selection_frame, text="Mostrar Proyectos", command=self.populate_projects_combo).grid(row=0, column=1, padx=5, pady=5)

        self.assign_members_label = ttk.Label(self.assign_members_frame, text="Nombres de estudiantes asignados:")
        self.assign_members_label.grid(row=1, column=0, padx=5, pady=5)
        self.assign_members_entry = ttk.Combobox(self.assign_members_frame, state="readonly", values=[])
        self.assign_members_entry.grid(row=1, column=1, padx=5, pady=5)
        self.assign_members_entry.set("Seleccionar estudiante")
        self.assign_members_button = ttk.Button(self.assign_members_frame, text="Asignar", command=self.add_student)
        self.assign_members_button.grid(row=1, column=2, padx=5, pady=5)
        self.save_assigned_students_button = ttk.Button(self.assign_members_frame, text="Guardar Estudiantes", command=self.save_assigned_students)
        self.save_assigned_students_button.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

        # Frame para el seguimiento del progreso del proyecto
        self.progress_frame = ttk.LabelFrame(self.main_frame, text="Seguimiento del Progreso")
        self.progress_tree = ttk.Treeview(self.progress_frame, columns=("Title", "Objectives", "Start Date", "End Date", "Status", "Assigned Students"))
        self.progress_tree.heading("#0", text="ID")
        self.progress_tree.heading("Title", text="Título")
        self.progress_tree.heading("Objectives", text="Objetivos")
        self.progress_tree.heading("Start Date", text="Fecha Inicial")
        self.progress_tree.heading("End Date", text="Fecha Final")
        self.progress_tree.heading("Status", text="Estado")
        self.progress_tree.heading("Assigned Students", text="Estudiantes Asignados")
        self.progress_tree.pack(fill="both", expand=True)

        # Mostrar solo las opciones al inicio
        self.hide_frames()

    def create_project(self):
        self.hide_frames()
        self.create_project_frame.pack(fill="both", expand=True)

    def assign_members(self):
        self.hide_frames()
        self.assign_members_frame.pack(fill="both", expand=True)
        self.populate_students_combo()

    def show_progress(self):
        self.hide_frames()
        self.progress_frame.pack(fill="both", expand=True)
        self.populate_progress_tree()

    def hide_frames(self):
        self.create_project_frame.pack_forget()
        self.assign_members_frame.pack_forget()
        self.progress_frame.pack_forget()

    def save_project(self):
        project_title = self.project_title_entry.get()
        project_objectives = self.project_objectives_entry.get()
        start_date = self.start_date_calendar.get_date()
        end_date = self.end_date_calendar.get_date()
        if project_title and project_objectives and start_date and end_date:
            # Guardar el proyecto en un archivo CSV
            with open('proyectos.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([project_title, project_objectives, start_date, end_date, "En Progreso", ", ".join(self.assigned_students)])
            print("Proyecto creado y guardado:")
            print("Título del Proyecto:", project_title)
            print("Objetivo General:", project_objectives)
            print("Fecha Inicial:", start_date)
            print("Fecha Final:", end_date)
            print("Estudiantes asignados:", ", ".join(self.assigned_students))

            # Mostrar mensaje de éxito
            messagebox.showinfo("Éxito", "Proyecto creado y guardado exitosamente.")

            # Limpiar los campos de entrada después de crear el proyecto
            self.project_title_entry.delete(0, tk.END)
            self.project_objectives_entry.delete(0, tk.END)
            self.start_date_calendar.delete(0, tk.END)
            self.end_date_calendar.delete(0, tk.END)
            self.assigned_students.clear()

    def add_student(self):
        student_name = self.assign_members_entry.get()
        if student_name and student_name not in self.assigned_students:
            self.assigned_students.append(student_name)
            print("Estudiante asignado:", student_name)
            self.update_assigned_students_label()

    def update_assigned_students_label(self):
        if self.assigned_students:
            self.assign_members_label.config(text="Nombres de estudiantes asignados:\n" + "\n".join(self.assigned_students))
        else:
            self.assign_members_label.config(text="Nombres de estudiantes asignados:")

    def populate_projects_combo(self):
        # Limpiar el Combobox
        self.projects_combo["values"] = ()
        # Leer proyectos del archivo CSV
        projects = self.read_projects()
        # Actualizar el Combobox
        if projects:
            project_titles = [project[0] for project in projects]
            self.projects_combo["values"] = project_titles
            self.projects_combo.current(0)

    def populate_students_combo(self):
        try:
            with open('lista_estudiantes.csv', mode='r', newline='') as file:
                reader = csv.reader(file)
                students = list(reader)
                if students:
                    student_names = [student[0] for student in students]
                    self.assign_members_entry["values"] = student_names
                    self.assign_members_entry.current(0)
        except FileNotFoundError:
            print("No se encontró el archivo 'lista_estudiantes.csv'")

    def read_projects(self):
        try:
            with open('proyectos.csv', mode='r', newline='') as file:
                reader = csv.reader(file)
                projects = list(reader)
                return projects
        except FileNotFoundError:
            return []

    def populate_progress_tree(self):
        # Limpiar árbol
        for row in self.progress_tree.get_children():
            self.progress_tree.delete(row)
        # Leer proyectos del archivo CSV
        projects = self.read_projects()
        # Actualizar el árbol
        if projects:
            for idx, project in enumerate(projects, start=1):
                self.progress_tree.insert("", "end", text=str(idx), values=project)

    def save_assigned_students(self):
        selected_project = self.projects_combo.get()
        if selected_project and self.assigned_students:
            # Leer proyectos del archivo CSV
            projects = self.read_projects()
            # Actualizar estudiantes asignados al proyecto seleccionado
            updated_projects = []
            for project in projects:
                if project[0] == selected_project:
                    project[5] = ", ".join(self.assigned_students)
                updated_projects.append(project)
            # Actualizar archivo CSV con los proyectos actualizados
            with open('proyectos.csv', mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(updated_projects)
            print("Estudiantes asignados guardados para el proyecto:", selected_project)
            # Limpiar la lista de estudiantes asignados después de guardar
            self.assigned_students.clear()
            # Actualizar la etiqueta de nombres de estudiantes asignados
            self.update_assigned_students_label()
            # Mostrar mensaje de éxito
            messagebox.showinfo("Éxito", "Estudiantes asignados guardados exitosamente.")
        else:
            print("Por favor selecciona un proyecto y asigna al menos un estudiante.")


def run():
    root = tk.Tk()
    app = ProyectosWindow(root)
    root.mainloop()

if __name__ == "__main__":
    run()
