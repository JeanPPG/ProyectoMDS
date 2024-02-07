import tkinter as tk
from frontend.gui import TaskManagerApp

def run():
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    run()
