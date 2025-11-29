import tkinter as tk
from tkinter import messagebox, ttk
from app.database import DatabaseManager
from app import config
from app.ui.sidebar import TableExplorer
from app.ui.query_panel import QueryPanel

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Bayanat - PostgreSQL Client")
        self.root.geometry("1100x750")
        
        # Configure global styles
        self.configure_styles()
        
        self.db_manager = DatabaseManager()

        # Main Container with padding
        main_container = ttk.Frame(root, padding="5")
        main_container.pack(fill=tk.BOTH, expand=True)

        # Layout: PanedWindow
        self.paned_window = tk.PanedWindow(main_container, orient=tk.HORIZONTAL, sashrelief=tk.FLAT, sashwidth=4, bg="#d9d9d9")
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        # Components
        self.sidebar = TableExplorer(self.paned_window, self.db_manager, self.on_table_double_click, self.update_status)
        self.paned_window.add(self.sidebar, minsize=250)

        self.query_panel = QueryPanel(self.paned_window, self.db_manager, self.connect_db, self.update_status)
        self.paned_window.add(self.query_panel, minsize=500)

        # Status Bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W, padding=(5, 2))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Initial Load
        self.load_initial_config()

    def configure_styles(self):
        style = ttk.Style()
        # General
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabel", background="#f0f0f0", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10))
        
        # Treeview
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=25)
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        
        # Custom styles
        style.configure("Header.TLabel", font=("Segoe UI", 12, "bold"), foreground="#333")
        style.configure("Action.TButton", font=("Segoe UI", 10, "bold"))

    def load_initial_config(self):
        conn_str = config.load_config()
        self.query_panel.set_connection_string(conn_str)
        if conn_str:
            self.root.after(100, self.connect_db)

    def connect_db(self):
        conn_str = self.query_panel.get_connection_string()
        if not conn_str:
            messagebox.showwarning("Input Error", "Please enter a connection string.")
            return

        self.update_status("Connecting...")
        try:
            self.db_manager.connect(conn_str)
            config.save_config(conn_str)
            self.update_status("Connected to database.")
            self.sidebar.refresh_tables()
        except Exception as e:
            self.update_status("Connection failed.")
            messagebox.showerror("Connection Failed", str(e))

    def on_table_double_click(self, table_name):
        query = f"SELECT * FROM {table_name} LIMIT 50;"
        self.query_panel.set_query(query)
        self.query_panel.run_query()

    def update_status(self, message):
        self.status_var.set(message)
