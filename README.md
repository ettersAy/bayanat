# Bayanat - Lightweight PostgreSQL Client

Bayanat is a streamlined, native desktop application for PostgreSQL, designed for developers who need a fast, no-nonsense tool to query databases and inspect schemas.

## 🚀 Why Bayanat?

In a world of heavy, web-based desktop apps, Bayanat stands out by being **native and efficient**.

| Feature | Bayanat (Python/Tkinter) | Typical Electron App (pgAdmin, etc.) |
|---------|--------------------------|--------------------------------------|
| **Memory Usage** | **~37 MB** | **150 MB - 500 MB+** |
| **Startup Time** | **Instant (< 1s)** | Slow (5s - 10s+) |
| **Tech Stack** | Standard Python (Tkinter) | Chromium + Node.js |
| **Dependencies** | Minimal (`psycopg2`) | Hundreds of node modules |

### Key Advantages

*   **Ultra Lightweight**: Runs comfortably on any hardware, consuming minimal system resources.
*   **Zero Bloat**: No embedded web browser, no tracking, no background services.
*   **Focused Workflow**: A clean interface that puts your data and queries front and center.
*   **Native Performance**: Snappy UI interactions with no input lag.

## ✨ Features

*   **Connection Management**: Connect to any PostgreSQL database (supports Neon.tech, AWS RDS, local, etc.). Remembers your last connection.
*   **Table Explorer**: Quickly browse tables in the `public` schema.
    *   View column names, data types, and constraints (Primary Keys, Not Null).
*   **Query Editor**: Multi-line SQL editor for writing complex queries.
*   **Dual Result Views**:
    *   **Table View**: Structured, scrollable grid for `SELECT` results.
    *   **Text View**: Plain text output for easy copying or viewing logs/errors.
*   **Status Bar**: Real-time feedback on connection status and query execution.

## 🛠️ Installation & Run

### Prerequisites
*   Python 3.x
*   `psycopg2` library

### Setup

1.  **Install Dependencies**:
    ```bash
    pip install psycopg2-binary
    ```
    *(Note: On some Linux systems, you might need `sudo apt install python3-tk` if it's not pre-installed).*

2.  **Run the App**:
    ```bash
    python3 main.py
    ```

## 📂 Project Structure

The project is structured for maintainability while keeping it simple:

*   `main.py`: Entry point.
*   `app/database.py`: Handles all PostgreSQL connections and queries.
*   `app/ui/`: Contains the user interface components (Sidebar, Query Panel, Main Window).
*   `app/config.py`: Manages persistent configuration (connection strings).
