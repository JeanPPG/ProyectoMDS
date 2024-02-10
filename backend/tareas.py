import os
import tkinter as tk
from tkinter import ttk
from tkinter import ttk, messagebox
import csv

from PIL import Image, ImageTk

class TareasWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Tareas")
        self.root.geometry("600x800")

        # Obtener la ruta del directorio actual
        current_dir = os.path.dirname(__file__)

        # Cargar iconos
        create_icon = Image.open(os.path.join(current_dir, "icons/create_icon.png")).resize((32, 32))
        assign_icon = Image.open(os.path.join(current_dir, "icons/assign_icon.png")).resize((32, 32))
        progress_icon = Image.open(os.path.join(current_dir, "icons/progress_icon.png")).resize((32, 32))

        # Convertir iconos a formato PhotoImage
        self.create_icon = ImageTk.PhotoImage(create_icon)
        self.assign_icon = ImageTk.PhotoImage(assign_icon)
        self.progress_icon = ImageTk.PhotoImage(progress_icon)

        # Frame para la selección de opciones
        self.options_frame = ttk.LabelFrame(self.root, text="Opciones")
        self.options_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Botones de opciones con iconos
        ttk.Button(self.options_frame, text="Crear Tarea", image=self.create_icon, compound=tk.LEFT, command=self.create_task).pack(side="left", padx=10, pady=10)
        ttk.Button(self.options_frame, text="Asignar Tarea", image=self.assign_icon, compound=tk.LEFT, command=self.assign_task).pack(side="left", padx=10, pady=10)
        ttk.Button(self.options_frame, text="Seguimiento", image=self.progress_icon, compound=tk.LEFT, command=self.show_progress).pack(side="left", padx=10, pady=10)

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
        self.assign_task_frame.pack(fill="both", expand=True, padx=20, pady=20)

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

        # Crear lista desplegable para seleccionar tarea
        if tasks:
            ttk.Label(self.assign_task_frame, text="Selecciona una tarea:").pack(pady=5)
            self.selected_task = ttk.Combobox(self.assign_task_frame, values=[task[0] for task in tasks], state="readonly")
            self.selected_task.pack(pady=5)
        else:
            ttk.Label(self.assign_task_frame, text="No hay tareas disponibles").pack(pady=5)

        # Leer nombres de estudiantes del archivo CSV
        student_names = self.read_student_names()

        # Crear lista desplegable para seleccionar nombre de estudiante
        if student_names:
            ttk.Label(self.assign_task_frame, text="Selecciona un estudiante:").pack(pady=5)
            self.selected_student = ttk.Combobox(self.assign_task_frame, values=student_names, state="readonly")
            self.selected_student.pack(pady=5)
        else:
            ttk.Label(self.assign_task_frame, text="No hay nombres de estudiantes disponibles").pack(pady=5)

        # Botón para asignar tarea
        ttk.Button(self.assign_task_frame, text="Asignar Tarea", command=self.assign_selected_task).pack(pady=10)

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
            # Crear tabla de tareas
            self.table = ttk.Treeview(self.progress_frame, columns=("Nombre", "Descripción", "Alumno", "Estado"), show="headings")
            self.table.heading("Nombre", text="Nombre")
            self.table.heading("Descripción", text="Descripción")
            self.table.heading("Alumno", text="Alumno")
            self.table.heading("Estado", text="Estado")
            for task in tasks:
                self.table.insert("", "end", values=task)
            self.table.pack(pady=5)
            # Botón para eliminar tarea
            ttk.Button(self.progress_frame, text="Eliminar Tarea", command=self.delete_task).pack(pady=10)
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
            # Mostrar mensaje de éxito
            messagebox.showinfo("Éxito", "Tarea creada y guardada exitosamente.")

            # Limpiar los campos de entrada después de crear la tarea
            self.task_name_entry.delete(0, tk.END)
            self.task_description_entry.delete(0, tk.END)

    def assign_selected_task(self):
        task_name = self.selected_task.get()
        student_name = self.selected_student.get()
        if task_name and student_name:
            # Leer tareas del archivo CSV
            tasks = self.read_tasks()
            # Actualizar tarea seleccionada
            updated_tasks = []
            for task in tasks:
                if task[0] == task_name:
                    task[2] = student_name
                    task[3] = "En Curso"
                updated_tasks.append(task)
            # Escribir las tareas actualizadas en el archivo CSV
            with open('tareas.csv', mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(updated_tasks)
            print("Tarea asignada y actualizada:")
            print("Nombre de la Tarea:", task_name)
            print("Estudiante Asignado:", student_name)
            print("Estado: En Curso")
            # Mostrar mensaje de éxito
            messagebox.showinfo("Éxito", "Tarea asignada y actualizada exitosamente.")

            # Limpiar los campos de entrada después de asignar la tarea
            self.selected_task.set("")
            self.selected_student.set("")

    def delete_task(self):
        selected_item = self.table.selection()[0]
        task_name = self.table.item(selected_item, "values")[0]
        if task_name:
            # Leer tareas del archivo CSV
            tasks = self.read_tasks()
            # Eliminar tarea seleccionada
            updated_tasks = [task for task in tasks if task[0] != task_name]
            # Escribir las tareas actualizadas en el archivo CSV
            with open('tareas.csv', mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(updated_tasks)
            print("Tarea eliminada:", task_name)
            # Mostrar mensaje de éxito
            messagebox.showinfo("Éxito", "Tarea eliminada exitosamente.")

            # Actualizar la vista de seguimiento de tareas
            self.show_progress()

    def read_student_names(self):
        try:
            with open('lista_estudiantes.csv', mode='r', newline='') as file:
                reader = csv.reader(file)
                student_names = [row[0] for row in reader]
                return student_names
        except FileNotFoundError:
            return []

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
