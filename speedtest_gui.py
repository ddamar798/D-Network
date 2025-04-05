import tkinter as tk
from tkinter import ttk
import threading
import speedtest_gui
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

log_data = []

def run_speedtest():
    btn_speedtest.config(state=tk.DISABLED)
    status.set("Mengukur kecepatan...")

    def test():
        try:
            st = speedtest_gui.Speedtest()
            st.get_best_server()
            download = st.download() / 1_000_000
            upload = st.upload() / 1_000_000
            ping = st.results.ping

            label_download.config(text=f"Unduh : {download:.2f} Mbps")
            label_upload.config(text=f"Unggah : {upload:.2f} Mbps")
            label_ping.config(text=f"Ping   : {ping:.2f} ms")
            status.set("Selesai.")

            update_graph(download, upload)

            timestamp = datetime.now().strftime("%H:%M:%S")
            log_data.append(f"[{timestamp}] Unduh: {download:.2f} Mbps, Unggah: {upload:.2f} Mbps, Ping: {ping:.2f} ms")
            update_log()
        except Exception as e:
            status.set(f"Error: {e}")
        finally:
            btn_speedtest.config(state=tk.NORMAL)

    threading.Thread(target=test).start()

def update_graph(download, upload):
    ax.clear()
    ax.bar(["Unduh", "Unggah"], [download, upload], color=["skyblue", "lightgreen"])
    ax.set_ylabel("Mbps")
    ax.set_title("Grafik Kecepatan")
    ax.set_ylim(0, max(download, upload) + 10)
    canvas.draw()

def update_log():
    log_box.config(state=tk.NORMAL)
    log_box.delete(1.0, tk.END)
    for entry in reversed(log_data[-10:]):
        log_box.insert(tk.END, entry + "\n")
    log_box.config(state=tk.DISABLED)

# === GUI Setup ===
root = tk.Tk()
root.title("Speedtest Internet")
root.geometry("500x600")

ttk.Label(root, text="Speedtest Internet", font=("Arial", 16)).pack(pady=10)

btn_speedtest = ttk.Button(root, text="Mulai Tes", command=run_speedtest)
btn_speedtest.pack()

status = tk.StringVar()
ttk.Label(root, textvariable=status).pack(pady=5)

label_download = ttk.Label(root, text="Unduh : - Mbps")
label_download.pack()
label_upload = ttk.Label(root, text="Unggah : - Mbps")
label_upload.pack()
label_ping = ttk.Label(root, text="Ping   : - ms")
label_ping.pack()

fig, ax = plt.subplots(figsize=(4, 3))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(pady=10)

ttk.Label(root, text="Riwayat Pengujian:").pack()
log_box = tk.Text(root, height=8, width=60, state=tk.DISABLED)
log_box.pack()

root.mainloop()
