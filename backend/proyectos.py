import tkinter as tk
from tkinter import ttk
import csv

class ProyectosWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Proyectos")
        self.root.geometry("600x400")

        # Frame para la selección de opciones
        self.options_frame = ttk.LabelFrame(self.root, text="Opciones")
        self.options_frame.pack(fill="both", expand=True, padx=20, pady=20)

        ttk.Button(self.options_frame, text="Crear Proyecto", command=self.create_project).pack(side="left", padx=10, pady=10)
        ttk.Button(self.options_frame, text="Asignar Miembros", command=self.assign_members).pack(side="left", padx=10, pady=10)
        ttk.Button(self.options_frame, text="Seguimiento del Progreso", command=self.show_progress).pack(side="left", padx=10, pady=10)

        # Frame para crear proyecto
        self.create_project_frame = ttk.LabelFrame(self.root, text="Crear Proyecto")
        self.create_project_frame.pack(fill="both", expand=True, padx=20, pady=20)

        ttk.Label(self.create_project_frame, text="Título del Proyecto:").pack(pady=5)
        self.project_title_entry = ttk.Entry(self.create_project_frame)
        self.project_title_entry.pack(fill="x", padx=5, pady=5)

        ttk.Label(self.create_project_frame, text="Objetivos:").pack(pady=5)
        self.project_objectives_entry = ttk.Entry(self.create_project_frame)
        self.project_objectives_entry.pack(fill="x", padx=5, pady=5)

        ttk.Label(self.create_project_frame, text="Alcance:").pack(pady=5)
        self.project_scope_entry = ttk.Entry(self.create_project_frame)
        self.project_scope_entry.pack(fill="x", padx=5, pady=5)

        ttk.Label(self.create_project_frame, text="Cronograma:").pack(pady=5)
        self.project_schedule_entry = ttk.Entry(self.create_project_frame)
        self.project_schedule_entry.pack(fill="x", padx=5, pady=5)

        ttk.Button(self.create_project_frame, text="Crear Proyecto", command=self.save_project).pack(pady=10)

        # Frame para asignar miembros del equipo
        self.assign_members_frame = ttk.LabelFrame(self.root, text="Asignar Miembros del Equipo")
        # Frame para el seguimiento del progreso del proyecto
        self.progress_frame = ttk.LabelFrame(self.root, text="Seguimiento del Progreso")

        # Mostrar solo las opciones al inicio
        self.hide_frames()

    def create_project(self):
        self.hide_frames()
        self.create_project_frame.pack(fill="both", expand=True)

    def assign_members(self):
        self.hide_frames()
        self.assign_members_frame.pack(fill="both", expand=True)

        # Limpiar lista de opciones
        for widget in self.assign_members_frame.winfo_children():
            widget.destroy()

        # Leer proyectos del archivo CSV
        projects = self.read_projects()

        # Crear opciones de selección
        if projects:
            ttk.Label(self.assign_members_frame, text="Selecciona un proyecto:").pack(pady=5)
            self.selected_project = tk.StringVar()
            for project in projects:
                ttk.Radiobutton(self.assign_members_frame, text=project[0], variable=self.selected_project, value=project[0]).pack(anchor="w", padx=5)
            ttk.Label(self.assign_members_frame, text="Miembro del Equipo:").pack(pady=5)
            self.team_member_entry = ttk.Entry(self.assign_members_frame)
            self.team_member_entry.pack(fill="x", padx=5, pady=5)
            ttk.Button(self.assign_members_frame, text="Asignar Miembro", command=self.assign_selected_member).pack(pady=10)
        else:
            ttk.Label(self.assign_members_frame, text="No hay proyectos disponibles").pack(pady=5)

    def show_progress(self):
        self.hide_frames()
        self.progress_frame.pack(fill="both", expand=True)

        # Limpiar lista de proyectos
        for widget in self.progress_frame.winfo_children():
            widget.destroy()

        # Leer proyectos del archivo CSV
        projects = self.read_projects()

        # Mostrar proyectos y su estado actual si hay proyectos disponibles
        if projects:
            ttk.Label(self.progress_frame, text="Proyectos y estado:").pack(pady=5)
            for project in projects:
                if len(project) >= 5:  # Comprobación de que la lista tiene al menos 5 elementos
                    ttk.Label(self.progress_frame, text=f"{project[0]} - Estado: {project[4]}").pack(anchor="w", padx=5)
                else:
                    ttk.Label(self.progress_frame, text=f"{project[0]} - Estado: ERROR: Faltan datos").pack(anchor="w", padx=5)
        else:
            ttk.Label(self.progress_frame, text="No hay proyectos disponibles").pack(pady=5)

    def hide_frames(self):
        self.create_project_frame.pack_forget()
        self.assign_members_frame.pack_forget()
        self.progress_frame.pack_forget()

    def save_project(self):
        project_title = self.project_title_entry.get()
        project_objectives = self.project_objectives_entry.get()
        project_scope = self.project_scope_entry.get()
        project_schedule = self.project_schedule_entry.get()
        if project_title and project_objectives and project_scope and project_schedule:
            # Guardar el proyecto en un archivo CSV
            with open('proyectos.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([project_title, project_objectives, project_scope, project_schedule, "En Progreso"])
            print("Proyecto creado y guardado:")
            print("Título del Proyecto:", project_title)
            print("Objetivos:", project_objectives)
            print("Alcance:", project_scope)
            print("Cronograma:", project_schedule)

            # Limpiar los campos de entrada después de crear el proyecto
            self.project_title_entry.delete(0, tk.END)
            self.project_objectives_entry.delete(0, tk.END)
            self.project_scope_entry.delete(0, tk.END)
            self.project_schedule_entry.delete(0, tk.END)

    def assign_selected_member(self):
        project_title = self.selected_project.get()
        team_member = self.team_member_entry.get()
        if project_title and team_member:
            # Leer proyectos del archivo CSV
            projects = self.read_projects()
            # Actualizar proyecto seleccionado
            with open('proyectos.csv', mode='w', newline='') as file:
                writer = csv.writer(file)
                for project in projects:
                    if project[0] == project_title:
                        project.append(team_member)
                    writer.writerow(project)
            print("Miembro asignado y proyecto actualizado:")
            print("Título del Proyecto:", project_title)
            print("Miembro del Equipo:", team_member)

            # Limpiar los campos de entrada después de asignar el miembro
            self.team_member_entry.delete(0, tk.END)
            self.selected_project.set("")

    def read_projects(self):
        try:
            with open('proyectos.csv', mode='r', newline='') as file:
                reader = csv.reader(file)
                projects = list(reader)
                return projects
        except FileNotFoundError:
            return []

def run():
    root = tk.Tk()
    app = ProyectosWindow(root)
    root.mainloop()

if __name__ == "__main__":
    run()
 