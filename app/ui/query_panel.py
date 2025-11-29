import tkinter as tk
from tkinter import ttk, font

class QueryPanel(ttk.Frame):
    def __init__(self, parent, db_manager, on_connect, status_callback):
        super().__init__(parent, padding="10")
        self.db_manager = db_manager
        self.on_connect = on_connect
        self.status_callback = status_callback
        self.mono_font = font.Font(family="Courier New", size=10)

        # 1. Connection Section
        conn_frame = ttk.LabelFrame(self, text="Connection", padding="10")
        conn_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(conn_frame, text="URI:").pack(side=tk.LEFT)
        
        self.conn_str_var = tk.StringVar()
        self.conn_entry = ttk.Entry(conn_frame, textvariable=self.conn_str_var)
        self.conn_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.connect_btn = ttk.Button(conn_frame, text="Connect", command=self.handle_connect, style="Action.TButton")
        self.connect_btn.pack(side=tk.LEFT)

        # 2. Query Section
        query_frame = ttk.LabelFrame(self, text="SQL Query", padding="10")
        query_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Toolbar
        toolbar = ttk.Frame(query_frame)
        toolbar.pack(fill=tk.X, pady=(0, 5))
        
        self.run_btn = ttk.Button(toolbar, text="▶ Run Query", command=self.run_query, style="Action.TButton")
        self.run_btn.pack(side=tk.RIGHT)
        
        self.query_text = tk.Text(query_frame, height=8, font=self.mono_font, wrap=tk.NONE, bd=1, relief=tk.SOLID)
        self.query_text.pack(fill=tk.BOTH, expand=True)

        # 3. Result Section
        result_frame = ttk.LabelFrame(self, text="Results", padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        self.result_notebook = ttk.Notebook(result_frame)
        self.result_notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: Table View
        self.tab_table = ttk.Frame(self.result_notebook)
        self.result_notebook.add(self.tab_table, text="Table")
        
        self.table_scroll_y = ttk.Scrollbar(self.tab_table, orient="vertical")
        self.table_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.table_scroll_x = ttk.Scrollbar(self.tab_table, orient="horizontal")
        self.table_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.result_tree = ttk.Treeview(self.tab_table, show="headings", 
                                        yscrollcommand=self.table_scroll_y.set, 
                                        xscrollcommand=self.table_scroll_x.set)
        self.result_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.table_scroll_y.config(command=self.result_tree.yview)
        self.table_scroll_x.config(command=self.result_tree.xview)

        # Bind Ctrl+C for copying
        self.result_tree.bind("<Control-c>", self.copy_from_table)

        # Tab 2: Text View
        self.tab_text = ttk.Frame(self.result_notebook)
        self.result_notebook.add(self.tab_text, text="Text")
        
        self.result_text = tk.Text(self.tab_text, height=10, font=self.mono_font, state=tk.DISABLED)
        self.result_text.pack(fill=tk.BOTH, expand=True)

    def set_connection_string(self, conn_str):
        self.conn_str_var.set(conn_str)

    def get_connection_string(self):
        return self.conn_str_var.get().strip()

    def set_query(self, query):
        self.query_text.delete("1.0", tk.END)
        self.query_text.insert(tk.END, query)

    def handle_connect(self):
        self.on_connect()

    def copy_from_table(self, event):
        selection = self.result_tree.selection()
        if not selection:
            return
            
        rows_data = []
        for item_id in selection:
            values = self.result_tree.item(item_id, "values")
            # Convert to tab-separated string
            row_str = "\t".join(map(str, values))
            rows_data.append(row_str)
            
        text_to_copy = "\n".join(rows_data)
        
        self.clipboard_clear()
        self.clipboard_append(text_to_copy)
        self.status_callback(f"Copied {len(selection)} rows to clipboard.")

    def run_query(self):
        query = self.query_text.get("1.0", tk.END).strip()
        if not query:
            self.status_callback("Query is empty.")
            return

        self.status_callback("Executing query...")
        try:
            columns, result = self.db_manager.execute_query(query)
            
            if columns is not None:
                # SELECT query
                rows = result
                count = len(rows)
                self.status_callback(f"Query executed successfully. {count} rows returned.")
                
                # Update Table View
                self.result_tree.delete(*self.result_tree.get_children())
                col_ids = [f"col_{i}" for i in range(len(columns))]
                self.result_tree["columns"] = col_ids
                
                for i, col_name in enumerate(columns):
                    col_id = col_ids[i]
                    self.result_tree.heading(col_id, text=col_name)
                    self.result_tree.column(col_id, width=100, anchor=tk.W)
                
                for row in rows:
                    self.result_tree.insert("", tk.END, values=row)
                
                # Update Text View
                self.update_text_view(columns, rows)
                
                self.result_notebook.select(self.tab_table)
            else:
                # INSERT/UPDATE/DELETE
                rowcount = result
                msg = f"Query OK, {rowcount} rows affected."
                self.status_callback(msg)
                
                self.result_tree.delete(*self.result_tree.get_children())
                self.result_tree["columns"] = []
                
                self.update_text_view_msg(msg)
                self.result_notebook.select(self.tab_text)
                
        except Exception as e:
            self.db_manager.rollback()
            error_msg = f"SQL Error: {e}"
            self.status_callback("Query failed.")
            self.update_text_view_msg(error_msg)
            self.result_notebook.select(self.tab_text)

    def update_text_view(self, columns, rows):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete("1.0", tk.END)
        
        output = []
        output.append(" | ".join(columns))
        output.append("-" * 40)
        for row in rows:
            output.append(" | ".join(map(str, row)))
        
        self.result_text.insert(tk.END, "\n".join(output))
        self.result_text.config(state=tk.DISABLED)

    def update_text_view_msg(self, msg):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, msg)
        self.result_text.config(state=tk.DISABLED)
