import tkinter as tk
from tkinter import ttk
import threading
import socket
from scapy.all import ARP, Ether, srp

COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 8080] # Port yang dituju

def scan_network():
    btn_scan.config(state=tk.DISABLED)
    status.set("Scaning
               jaringan...")

    def scan():
        ip_range = entry_ip.get() or "192.168.1.1/24"
        devices = []

        try:
            arp = ARP(pdst=ip_range)
            ether = Ether(dst="ff:ff:ff:ff:ff:ff")
            packet = ether/arp

            result = srp(packet, timeout=3, verbose=0)[0]

            for _, received in result:
                ip = received.psrc
                mac = received.hwsrc
                try:
                    host = socket.gethostbyaddr(ip)[0]
                except:
                    host = "Unknown"

                ports = check_ports(ip)
                devices.append((ip, mac, host, ports))

            update_list(devices)
            status.set("Selesai.")
        except Exception as e:
            status.set(f"Error: {e}")
        finally:
            btn_scan.config(state=tk.NORMAL)

    threading.Thread(target=scan).start()

def check_ports(ip):
    open_ports = []
    for port in COMMON_PORTS:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            if sock.connect_ex((ip, port)) == 0:
                open_ports.append(port)
            sock.close()
        except:
            pass
    return open_ports

def update_list(devices):
    listbox.delete(0, tk.END)
    for ip, mac, host, ports in devices:
        listbox.insert(tk.END, f"{ip} | {host} | {mac}")
        if ports:
            listbox.insert(tk.END, f"   🔓 Port terbuka: {', '.join(map(str, ports))}")
        else:
            listbox.insert(tk.END, "   🔒 Tidak ada port umum terbuka.")

# === GUI Setup ===
root = tk.Tk()
root.title("Network Scanner")
root.geometry("700x600")

ttk.Label(root, text="Scanner Jaringan", font=("Arial", 16)).pack(pady=10)

frame_ip = ttk.Frame(root)
frame_ip.pack()
ttk.Label(frame_ip, text="IP Range (mis: 192.168.1.1/24):").pack(side=tk.LEFT)
entry_ip = ttk.Entry(frame_ip, width=20)
entry_ip.pack(side=tk.LEFT, padx=5)

btn_scan = ttk.Button(root, text="Mulai Scan", command=scan_network)
btn_scan.pack(pady=5)

status = tk.StringVar()
ttk.Label(root, textvariable=status).pack()

listbox = tk.Listbox(root, width=100, height=25)
listbox.pack(pady=10)

root.mainloop()
