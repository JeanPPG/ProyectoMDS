import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from frontend.tareas import TareasWindow
from frontend.proyectos import ProyectosWindow

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Tareas y Proyectos")
        self.root.geometry("600x400")

        # Obtener la ruta del directorio actual
        current_dir = os.path.dirname(__file__)

        # Cargar imágenes de los iconos desde el directorio actual
        tasks_icon = Image.open(os.path.join(current_dir, "icons/tareas.png")).resize((100, 100))
        projects_icon = Image.open(os.path.join(current_dir, "icons/proyectos.png")).resize((100, 100))
        reports_icon = Image.open(os.path.join(current_dir, "icons/reportes.png")).resize((100, 100))

        self.tasks_icon = ImageTk.PhotoImage(tasks_icon)
        self.projects_icon = ImageTk.PhotoImage(projects_icon)
        self.reports_icon = ImageTk.PhotoImage(reports_icon)

        # Crear los botones de la ventana principal
        self.tasks_button = ttk.Button(self.root, image=self.tasks_icon, text="Tareas", compound="top", command=self.open_tasks)
        self.tasks_button.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.projects_button = ttk.Button(self.root, image=self.projects_icon, text="Proyectos", compound="top", command=self.open_projects)
        self.projects_button.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        self.reports_button = ttk.Button(self.root, image=self.reports_icon, text="Reportes", compound="top", command=self.open_reports)
        self.reports_button.grid(row=0, column=2, padx=20, pady=20, sticky="nsew")

        # Configurar el grid para que los botones se expandan y se centren
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure((0, 1, 2), weight=1)

    def open_tasks(self):
        # Abrir la ventana de tareas
        tareas_window = tk.Toplevel(self.root)
        tareas_app = TareasWindow(tareas_window)

    def open_projects(self):
        # Abrir la ventana de proyectos
        proyectos_window = tk.Toplevel(self.root)
        proyectos_app = ProyectosWindow(proyectos_window)

    def open_reports(self):
        # Lógica para abrir la ventana de reportes
        pass

def run():
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    run()
