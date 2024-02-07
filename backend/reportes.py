import tkinter as tk
from tkinter import ttk

class ReportesWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Reportes")
        self.root.geometry("600x400")

        # Frame para el dashboard
        self.dashboard_frame = ttk.LabelFrame(self.root, text="Dashboard")
        self.dashboard_frame.pack(fill="both", expand=True, padx=20, pady=20)

        ttk.Label(self.dashboard_frame, text="Resumen de Tareas Pendientes:").pack(pady=5)
        self.pending_tasks_label = ttk.Label(self.dashboard_frame, text="0")
        self.pending_tasks_label.pack(pady=5)

        ttk.Label(self.dashboard_frame, text="Resumen de Proyectos en Curso:").pack(pady=5)
        self.ongoing_projects_label = ttk.Label(self.dashboard_frame, text="0")
        self.ongoing_projects_label.pack(pady=5)

        # Frame para los reportes básicos
        self.reports_frame = ttk.LabelFrame(self.root, text="Reportes Básicos")
        self.reports_frame.pack(fill="both", expand=True, padx=20, pady=20)

        ttk.Button(self.reports_frame, text="Generar Reporte", command=self.generate_report).pack(pady=10)

    def generate_report(self):
        # Lógica para generar el reporte
        pass

def run():
    root = tk.Tk()
    app = ReportesWindow(root)
    root.mainloop()

if __name__ == "__main__":
    run()
