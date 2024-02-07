import tkinter as tk
from tkinter import ttk
import csv

class TareasWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Tareas")
        self.root.geometry("600x400")

        # Frame para la selección de opciones
        self.options_frame = ttk.LabelFrame(self.root, text="Opciones")
        self.options_frame.pack(fill="both", expand=True, padx=20, pady=20)

        ttk.Button(self.options_frame, text="Crear Tarea", command=self.create_task).pack(side="left", padx=10, pady=10)
        ttk.Button(self.options_frame, text="Asignar Tarea", command=self.assign_task).pack(side="left", padx=10, pady=10)
        ttk.Button(self.options_frame, text="Seguimiento", command=self.show_progress).pack(side="left", padx=10, pady=10)

        # Frame para crear tarea
        self.create_task_frame = ttk.LabelFrame(self.root, text="Crear Tarea")
        self.create_task_frame.pack(fill="both", expand=True, padx=20, pady=20)

        ttk.Label(self.create_task_frame, text="Nombre de la Tarea:").pack(pady=5)
        self.task_name_entry = ttk.Entry(self.create_task_frame)
        self.task_name_entry.pack(fill="x", padx=5, pady=5)

        ttk.Label(self.create_task_frame, text="Descripción:").pack(pady=5)
        self.task_description_entry = ttk.Entry(self.create_task_frame)
        self.task_description_entry.pack(fill="x", padx=5, pady=5)

        ttk.Button(self.create_task_frame, text="Crear Tarea", command=self.save_task).pack(pady=10)

        # Frame para asignar tarea
        self.assign_task_frame = ttk.LabelFrame(self.root, text="Asignar Tarea")
        # Frame para el seguimiento del progreso de tareas
        self.progress_frame = ttk.LabelFrame(self.root, text="Seguimiento")

        # Mostrar solo las opciones al inicio
        self.hide_frames()

    def create_task(self):
        self.hide_frames()
        self.create_task_frame.pack(fill="both", expand=True)

    def assign_task(self):
        self.hide_frames()
        self.assign_task_frame.pack(fill="both", expand=True)

        # Limpiar lista de opciones
        for widget in self.assign_task_frame.winfo_children():
            widget.destroy()

        # Leer tareas del archivo CSV
        tasks = self.read_tasks()

        # Crear opciones de selección
        if tasks:
            ttk.Label(self.assign_task_frame, text="Selecciona una tarea:").pack(pady=5)
            self.selected_task = tk.StringVar()
            for task in tasks:
                ttk.Radiobutton(self.assign_task_frame, text=task[0], variable=self.selected_task, value=task[0]).pack(anchor="w", padx=5)
            ttk.Label(self.assign_task_frame, text="Nombre del Estudiante:").pack(pady=5)
            self.student_name_entry = ttk.Entry(self.assign_task_frame)
            self.student_name_entry.pack(fill="x", padx=5, pady=5)
            ttk.Button(self.assign_task_frame, text="Asignar Tarea", command=self.assign_selected_task).pack(pady=10)
        else:
            ttk.Label(self.assign_task_frame, text="No hay tareas disponibles").pack(pady=5)

    def show_progress(self):
        self.hide_frames()
        self.progress_frame.pack(fill="both", expand=True)

        # Limpiar lista de tareas
        for widget in self.progress_frame.winfo_children():
            widget.destroy()

        # Leer tareas del archivo CSV
        tasks = self.read_tasks()

        # Mostrar tareas y su estado actual si hay tareas disponibles
        if tasks:
            ttk.Label(self.progress_frame, text="Tareas y estado:").pack(pady=5)
            for task in tasks:
                if len(task) >= 4:  # Comprobación de que la lista tiene al menos 4 elementos
                    ttk.Label(self.progress_frame, text=f"{task[0]} - Estado: {task[3]}").pack(anchor="w", padx=5)
                else:
                    ttk.Label(self.progress_frame, text=f"{task[0]} - Estado: ERROR: Faltan datos").pack(anchor="w", padx=5)
        else:
            ttk.Label(self.progress_frame, text="No hay tareas disponibles").pack(pady=5)

    def hide_frames(self):
        self.create_task_frame.pack_forget()
        self.assign_task_frame.pack_forget()
        self.progress_frame.pack_forget()

    def save_task(self):
        task_name = self.task_name_entry.get()
        task_description = self.task_description_entry.get()
        if task_name and task_description:
            # Guardar la tarea en un archivo CSV
            with open('tareas.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([task_name, task_description, "", "Pendiente"])
            print("Tarea creada y guardada:")
            print("Nombre de la Tarea:", task_name)
            print("Descripción:", task_description)

            # Limpiar los campos de entrada después de crear la tarea
            self.task_name_entry.delete(0, tk.END)
            self.task_description_entry.delete(0, tk.END)

    def assign_selected_task(self):
        task_name = self.selected_task.get()
        student_name = self.student_name_entry.get()
        if task_name and student_name:
            # Leer tareas del archivo CSV
            tasks = self.read_tasks()
            # Actualizar tarea seleccionada
            with open('tareas.csv', mode='w', newline='') as file:
                writer = csv.writer(file)
                for task in tasks:
                    if task[0] == task_name:
                        task[2] = student_name
                        task[3] = "En Curso"
                    writer.writerow(task)
            print("Tarea asignada y actualizada:")
            print("Nombre de la Tarea:", task_name)
            print("Estudiante Asignado:", student_name)
            print("Estado: En Curso")

            # Limpiar los campos de entrada después de asignar la tarea
            self.student_name_entry.delete(0, tk.END)
            self.selected_task.set("")

    def read_tasks(self):
        try:
            with open('tareas.csv', mode='r', newline='') as file:
                reader = csv.reader(file)
                tasks = list(reader)
                return tasks
        except FileNotFoundError:
            return []

def run():
    root = tk.Tk()
    app = TareasWindow(root)
    root.mainloop()

if __name__ == "__main__":
    run()
