import tkinter as tk
from backend.gui import TaskManagerApp

def run():
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    run()
 