import tkinter as tk
from tkinter import ttk # get tkinter from import.
import subprocess
import sys
import os

def run_speedtest():
    subprocess.Popen([sys.executable, "speedtest_gui.py"])

def run_network_scanner():
    subprocess.Popen([sys.executable, "network_scanner.py"])

root = tk.Tk()
root.title("Dashboard Jaringan")
root.geometry("300x200")

ttk.Label(root, text="Pilih Fitur", font=("Arial", 16)).pack(pady=20)

ttk.Button(root, text="🔄 Speedtest Internet", command=run_speedtest).pack(pady=10)
ttk.Button(root, text="📡 Network Scanner", command=run_network_scanner).pack(pady=10)

root.mainloop()
