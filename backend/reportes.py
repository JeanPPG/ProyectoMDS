import tkinter as tk
from tkinter import ttk, messagebox
import csv
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

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
        # Leer datos de tareas desde el archivo CSV
        tasks_data = self.read_csv("tareas.csv")
        # Leer datos de proyectos desde el archivo CSV
        projects_data = self.read_csv("proyectos.csv")

        # Verificar si hay datos disponibles
        if tasks_data or projects_data:
            # Generar PDF
            doc = SimpleDocTemplate("reporte.pdf", pagesize=letter)
            content = []

            # Estilo para el texto centrado
            centered_style = ParagraphStyle(name="Centered", alignment=TA_CENTER)

            # Encabezado
            header_text = "<b>Universidad de las Fuerzas Armadas ESPE</b><br/><br/>Departamento de Ciencias de la Computación<br/><br/>Metodologías del Desarrollo de Software<br/><br/>"
            content.append(Paragraph(header_text, centered_style))

            # Tabla de tareas
            if tasks_data:
                tasks_table = self.create_table(tasks_data)
                content.append(Paragraph("<b>Tareas:</b>", centered_style))
                content.append(tasks_table)

            # Tabla de proyectos
            if projects_data:
                projects_table = self.create_table(projects_data)
                content.append(Paragraph("<b>Proyectos:</b>", centered_style))
                content.append(projects_table)

            doc.build(content)
            messagebox.showinfo("Generación Exitosa", "El reporte se generó correctamente.")
        else:
            messagebox.showwarning("Sin Datos", "No hay datos disponibles para generar el informe.")


    def create_table(self, data):
        table = Table(data)
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                   ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                                   ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                   ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                   ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                   ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                   ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
        return table

    def read_csv(self, filename):
        try:
            with open(filename, mode='r', newline='') as file:
                reader = csv.reader(file)
                data = list(reader)
            return data
        except FileNotFoundError:
            return []

def run():
    root = tk.Tk()
    app = ReportesWindow(root)
    root.mainloop()

if __name__ == "__main__":
    run()
