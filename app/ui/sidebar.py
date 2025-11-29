import tkinter as tk
from tkinter import ttk

class TableExplorer(ttk.Frame):
    def __init__(self, parent, db_manager, on_table_double_click, status_callback):
        super().__init__(parent, padding="10")
        self.db_manager = db_manager
        self.on_table_double_click = on_table_double_click
        self.status_callback = status_callback
        
        # Header
        ttk.Label(self, text="Database Explorer", style="Header.TLabel").pack(anchor=tk.W, pady=(0, 10))
        
        # Treeview Container (for scrollbar)
        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Treeview
        self.tree = ttk.Treeview(tree_frame, show="tree", selectmode="browse", yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=self.tree.yview)
        
        # Bindings
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.tree.bind("<Double-Button-1>", self.on_tree_double_click_event)

    def refresh_tables(self):
        """Fetches table names and populates the treeview."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            tables = self.db_manager.fetch_tables()
            for table_name in tables:
                # Add table icon or just text
                node_id = self.tree.insert("", tk.END, text=f" {table_name}", open=False, values=("table", table_name))
                self.tree.insert(node_id, tk.END, text="Loading...")
            self.status_callback(f"Loaded {len(tables)} tables.")
        except Exception as e:
            self.status_callback(f"Error loading tables: {e}")
            print(f"Error refreshing tables: {e}")

    def on_tree_select(self, event):
        """Handles single click to expand and show columns."""
        selection = self.tree.selection()
        if not selection:
            return
        
        node_id = selection[0]
        values = self.tree.item(node_id, "values")
        
        if values and values[0] == "table":
            table_name = values[1]
            self.tree.item(node_id, open=True)
            
            children = self.tree.get_children(node_id)
            if children and self.tree.item(children[0], "text") == "Loading...":
                self.load_columns(node_id, table_name)

    def load_columns(self, node_id, table_name):
        """Fetches columns for a table and updates the tree node."""
        for child in self.tree.get_children(node_id):
            self.tree.delete(child)
            
        try:
            columns, pks = self.db_manager.fetch_columns(table_name)

            for col in columns:
                col_name, data_type, is_nullable, default_val = col
                constraints = []
                if col_name in pks:
                    constraints.append("PK")
                if is_nullable == "NO":
                    constraints.append("NN")
                
                # Format: name (TYPE) [PK, NN]
                type_str = data_type.upper()
                constraint_str = f"[{', '.join(constraints)}]" if constraints else ""
                
                display_text = f" {col_name}  :  {type_str} {constraint_str}"
                self.tree.insert(node_id, tk.END, text=display_text, values=("column", col_name))
        except Exception as e:
            self.status_callback(f"Error loading columns for {table_name}")
            print(f"Error loading columns: {e}")

    def on_tree_double_click_event(self, event):
        """Handles double-click event."""
        selection = self.tree.selection()
        if not selection:
            return
        
        node_id = selection[0]
        values = self.tree.item(node_id, "values")
        
        if values and values[0] == "table":
            table_name = values[1]
            self.on_table_double_click(table_name)
