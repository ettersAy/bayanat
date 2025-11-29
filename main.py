import tkinter as tk
from app.ui.main_window import MainWindow

if __name__ == "__main__":
    root = tk.Tk()
    style = tk.ttk.Style()
    try:
        style.theme_use('clam')
    except tk.TclError:
        pass  # Fallback to default if clam is not available
    
    app = MainWindow(root)
    root.mainloop()
