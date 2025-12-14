# Prompt for Building "Tarqim" - The Lightweight Markdown Viewer

**Role:** You are an expert Python Desktop Application Developer specializing in creating ultra-lightweight, high-performance tools using standard libraries.

**Objective:** Build **"Tarqim"**, a fast and native desktop application to view and browse Markdown files.

**Core Philosophy:**

* **Zero Bloat:** Do NOT use Electron, Qt, or heavy web frameworks.
* **Native Performance:** The app must start instantly (< 1s) and use minimal RAM (< 50MB).
* **Simplicity:** Clean, focused UI.

---

## 1. Technology Stack

* **Language:** Python 3.x
* **GUI Framework:** `tkinter` (Standard Library) with `ttk` widgets.
* **Markdown Parsing:** Use a lightweight library like `markdown2` or `mistune` to parse text, but render it natively using `tkinter.Text` tags (do not embed a web browser).
* **Theme:** Use `ttk.Style` with the `'clam'` theme for a modern, flat look.

## 2. UI Layout & Design

The interface should follow a "Paned" layout (resizable split view):

* **Left Panel (Sidebar):**
  * **File Explorer:** A `ttk.Treeview` showing the current directory structure.
  * **Filter:** Only show `.md` or `.markdown` files (and folders).
  * **Interaction:** Single click to select, double click (or single click depending on UX preference) to open/render the file in the right panel.

* **Right Panel (Preview):**
  * **Viewer:** A read-only `tkinter.Text` widget.
  * **Styling:**
    * **Headers (H1, H2...):** Larger font, bold, distinct colors.
    * **Code Blocks:** Monospaced font, slightly different background color.
    * **Lists:** Indented with bullet points.
    * **Links:** Blue text (clickable if possible, opening in default browser).

* **Status Bar (Bottom):**
  * Display current file path, word count, or status messages (e.g., "File loaded in 0.02s").

## 3. User Experience (UX) Requirements

* **Keyboard Shortcuts:**
  * `Ctrl+O`: Open Folder/File.
  * `Ctrl+Q`: Quit.
* **Persistence:** Remember the last opened directory upon restart (save to a JSON config file).
* **Visual Polish:**
  * Use padding (`padx`, `pady`) so elements aren't cramped.
  * Use `ttk.LabelFrame` to group sections if necessary.
  * Ensure the window title updates with the current filename.

## 4. Implementation Steps (Workflow)

Please follow this specific workflow:

1. **Phase 1: Prototype (Single File)**
    * Create a single script `tarqim.py`.
    * Implement the basic GUI with dummy data to verify the layout.
    * Implement the Markdown rendering logic (parsing MD -> Text Widget Tags).

2. **Phase 2: Functionality**
    * Connect the File Explorer to the real file system.
    * Implement file reading and rendering.
    * Add the "Open Folder" dialog.

3. **Phase 3: Refactor & Structure**
    * Split the code into a clean project structure:
        * `main.py`
        * `app/ui/` (Sidebar, PreviewPanel, MainWindow)
        * `app/core/` (MarkdownRenderer, ConfigManager)
    * Ensure code is modular and typed.

4. **Phase 4: Packaging**
    * Create a `.desktop` file for Linux integration (Icon, Name, Exec path).
    * Create a `README.md` explaining the "Lightweight" advantage.

## 5. Deliverables

* Full source code.
* `requirements.txt` (should be very short).
* `tarqim.desktop` file.
* Instructions on how to run.
