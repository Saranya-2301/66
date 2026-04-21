import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import sys

# ─────────────────────────────
# WINDOW
# ─────────────────────────────
root = tk.Tk()
root.title("AI Assisted Compiler")
root.geometry("900x500")
root.configure(bg="#f4f6f8")

file_path = tk.StringVar()

# ─────────────────────────────
# FUNCTIONS
# ─────────────────────────────
def select_file():
    file = filedialog.askopenfilename(
        filetypes=[("Source Files", "*.c *.cpp *.java")]
    )
    file_path.set(file)

def detect_language(file):
    if file.endswith(".c"):
        return "C"
    elif file.endswith(".cpp"):
        return "CPP"
    elif file.endswith(".java"):
        return "Java"
    return "C"

def run_project():
    file = file_path.get()

    if not file:
        messagebox.showerror("Error", "Please select a file")
        return

    lang = detect_language(file)

    try:
        cmd = [sys.executable, "corrected.py", lang, file]

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )

        output_box.delete(1.0, tk.END)
        output_box.insert(tk.END, result.stdout + "\n" + result.stderr)

    except Exception as e:
        messagebox.showerror("Error", str(e))

# ─────────────────────────────
# HEADER
# ─────────────────────────────
header = tk.Frame(root, bg="#2c3e50", height=60)
header.pack(fill="x")

tk.Label(header,
         text="AI Assisted Compiler",
         bg="#2c3e50",
         fg="white",
         font=("Segoe UI", 16, "bold")).pack(pady=5)

tk.Label(header,
         text="Lexical & Syntax Assistance",
         bg="#2c3e50",
         fg="#d1d5db",
         font=("Segoe UI", 9)).pack()

# ─────────────────────────────
# MAIN LAYOUT
# ─────────────────────────────
main = tk.Frame(root, bg="#f4f6f8")
main.pack(fill="both", expand=True)

# LEFT PANEL
left = tk.Frame(main, bg="white", width=350)
left.pack(side="left", fill="y", padx=15, pady=15)

# Spacer (push content down)
tk.Frame(left, bg="white", height=80).pack()

# Select file button
tk.Button(left, text="Select File",
          bg="#4CAF50", fg="white",
          font=("Segoe UI", 10),
          padx=10, pady=6,
          command=select_file).pack(pady=10)

# File path
tk.Label(left, textvariable=file_path,
         bg="white", fg="#333",
         wraplength=300,
         justify="left").pack(pady=10)

# Run button
tk.Button(left, text="Run",
          bg="#007acc", fg="white",
          font=("Segoe UI", 11, "bold"),
          padx=25, pady=8,
          command=run_project).pack(pady=20)

# Extra space below
tk.Frame(left, bg="white").pack(expand=True)

# RIGHT PANEL
right = tk.Frame(main, bg="white")
right.pack(side="right", expand=True, fill="both", padx=10, pady=15)

tk.Label(right, text="Output",
         bg="white", fg="#2c3e50",
         font=("Segoe UI", 13, "bold")).pack(pady=5)

frame = tk.Frame(right)
frame.pack(expand=True, fill="both")

scroll = tk.Scrollbar(frame)
scroll.pack(side="right", fill="y")

output_box = tk.Text(
    frame,
    bg="#fafafa",
    fg="#222",
    font=("Consolas", 10),
    yscrollcommand=scroll.set,
    bd=1,
    relief="solid"
)

output_box.pack(expand=True, fill="both")
scroll.config(command=output_box.yview)

# ─────────────────────────────
root.mainloop()