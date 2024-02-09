import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
import csv

class ProyectosWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Proyectos")
        self.root.geometry("600x400")

        # Frame principal
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        # Frame para la selección de opciones
        self.options_frame = ttk.LabelFrame(self.main_frame, text="Opciones")
        self.options_frame.pack(fill="both", expand=True, padx=20, pady=20)

        ttk.Button(self.options_frame, text="Crear Proyecto", command=self.create_project).pack(side="left", padx=10, pady=10)
        ttk.Button(self.options_frame, text="Asignar Miembros", command=self.assign_members).pack(side="left", padx=10, pady=10)
        ttk.Button(self.options_frame, text="Seguimiento del Progreso", command=self.show_progress).pack(side="left", padx=10, pady=10)

        # Frame para crear proyecto
        self.create_project_frame = ttk.LabelFrame(self.main_frame, text="Crear Proyecto")
        ttk.Label(self.create_project_frame, text="Título del Proyecto:").pack(pady=5)
        self.project_title_entry = ttk.Entry(self.create_project_frame)
        self.project_title_entry.pack(fill="x", padx=5, pady=5)

        ttk.Label(self.create_project_frame, text="Objetivos:").pack(pady=5)
        self.project_objectives_entry = ttk.Entry(self.create_project_frame)
        self.project_objectives_entry.pack(fill="x", padx=5, pady=5)

        ttk.Label(self.create_project_frame, text="Alcance:").pack(pady=5)
        self.project_scope_entry = ttk.Entry(self.create_project_frame)
        self.project_scope_entry.pack(fill="x", padx=5, pady=5)

        ttk.Label(self.create_project_frame, text="Fecha Inicial:").pack(pady=5)
        self.start_date_calendar = Calendar(self.create_project_frame, selectmode='day', date_pattern='dd/mm/yyyy')
        self.start_date_calendar.pack(fill="x", padx=5, pady=5)

        ttk.Label(self.create_project_frame, text="Fecha Final:").pack(pady=5)
        self.end_date_calendar = Calendar(self.create_project_frame, selectmode='day', date_pattern='dd/mm/yyyy')
        self.end_date_calendar.pack(fill="x", padx=5, pady=5)

        ttk.Button(self.create_project_frame, text="Crear Proyecto", command=self.save_project).pack(pady=10)

        # Frame para asignar miembros del equipo
        self.assign_members_frame = ttk.LabelFrame(self.main_frame, text="Asignar Miembros del Equipo")
        # Frame para el seguimiento del progreso del proyecto
        self.progress_frame = ttk.LabelFrame(self.main_frame, text="Seguimiento del Progreso")

        # Mostrar solo las opciones al inicio
        self.hide_frames()

    def create_project(self):
        self.hide_frames()
        self.create_project_frame.pack(fill="both", expand=True)

    def assign_members(self):
        self.hide_frames()
        self.assign_members_frame.pack(fill="both", expand=True)

    def show_progress(self):
        self.hide_frames()
        self.progress_frame.pack(fill="both", expand=True)

    def hide_frames(self):
        self.create_project_frame.pack_forget()
        self.assign_members_frame.pack_forget()
        self.progress_frame.pack_forget()

    def save_project(self):
        project_title = self.project_title_entry.get()
        project_objectives = self.project_objectives_entry.get()
        project_scope = self.project_scope_entry.get()
        start_date = self.start_date_calendar.get_date()
        end_date = self.end_date_calendar.get_date()
        if project_title and project_objectives and project_scope and start_date and end_date:
            # Guardar el proyecto en un archivo CSV
            with open('proyectos.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([project_title, project_objectives, project_scope, start_date, end_date, "En Progreso"])
            print("Proyecto creado y guardado:")
            print("Título del Proyecto:", project_title)
            print("Objetivos:", project_objectives)
            print("Alcance:", project_scope)
            print("Fecha Inicial:", start_date)
            print("Fecha Final:", end_date)

            # Limpiar los campos de entrada después de crear el proyecto
            self.project_title_entry.delete(0, tk.END)
            self.project_objectives_entry.delete(0, tk.END)
            self.project_scope_entry.delete(0, tk.END)

def run():
    root = tk.Tk()
    app = ProyectosWindow(root)
    root.mainloop()

if __name__ == "__main__":
    run()
