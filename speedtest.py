import speedtest

def test_speed():
    print("Mengukur kecepatan internet... Mohon tunggu...")
    
    st = speedtest.Speedtest()
    st.get_best_server()

    download_speed = st.download() / 1_000_000  # bps ke Mbps
    upload_speed = st.upload() / 1_000_000
    ping = st.results.ping

    print(f"\nHasil Pengukuran:")
    print(f"Ping           : {ping:.2f} ms")
    print(f"Kecepatan Unduh: {download_speed:.2f} Mbps")
    print(f"Kecepatan Unggah: {upload_speed:.2f} Mbps")

if __name__ == "__main__":
    test_speed()
