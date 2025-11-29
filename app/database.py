import psycopg2

class DatabaseManager:
    def __init__(self):
        self.conn = None

    def connect(self, conn_str):
        """Connects to the database."""
        if self.conn and not self.conn.closed:
            self.conn.close()
        self.conn = psycopg2.connect(conn_str)

    def close(self):
        """Closes the connection."""
        if self.conn and not self.conn.closed:
            self.conn.close()

    def is_connected(self):
        return self.conn is not None and not self.conn.closed

    def fetch_tables(self):
        """Fetches public tables."""
        if not self.is_connected():
            return []
        
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                ORDER BY table_name;
            """)
            return [row[0] for row in cur.fetchall()]

    def fetch_columns(self, table_name):
        """Fetches columns and primary keys for a table."""
        if not self.is_connected():
            return [], set()

        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns
                WHERE table_name = %s AND table_schema = 'public'
                ORDER BY ordinal_position;
            """, (table_name,))
            columns = cur.fetchall()
            
            cur.execute("""
                SELECT c.column_name
                FROM information_schema.table_constraints tc
                JOIN information_schema.constraint_column_usage AS ccu USING (constraint_schema, constraint_name)
                JOIN information_schema.columns AS c ON c.table_schema = tc.constraint_schema
                    AND tc.table_name = c.table_name AND ccu.column_name = c.column_name
                WHERE constraint_type = 'PRIMARY KEY' AND tc.table_name = %s AND tc.table_schema = 'public';
            """, (table_name,))
            pks = {row[0] for row in cur.fetchall()}
            
            return columns, pks

    def execute_query(self, query):
        """Executes a query and returns (columns, rows) for SELECT or (None, rowcount) for others."""
        if not self.is_connected():
            raise Exception("Not connected to database.")

        with self.conn.cursor() as cur:
            cur.execute(query)
            
            if cur.description:
                columns = [desc[0] for desc in cur.description]
                rows = cur.fetchall()
                return columns, rows
            else:
                self.conn.commit()
                return None, cur.rowcount
    
    def rollback(self):
        if self.conn and not self.conn.closed:
            self.conn.rollback()
