from pyngrok import ngrok

# Ganti TOKEN_KAMU dengan authtoken ngrok kamu
# Dapatkan di: https://dashboard.ngrok.com/get-started/your-authtoken
NGROK_AUTH_TOKEN = "3IR4h33L7CWvSdNBNCyXvFA0B4Y_2ygpWa7Yg3wHwBZ2Ksm82"

ngrok.set_auth_token(NGROK_AUTH_TOKEN)

# Buat tunnel ke port 8502 (port streamlit yang sedang jalan)
public_url = ngrok.connect(8502)

print("=" * 50)
print("✅ Streamlit app berhasil di-tunnel ke ngrok!")
print(f"🌐 URL Public: {public_url}")
print("=" * 50)
print("Tekan Ctrl+C untuk menghentikan tunnel...")

# Jaga tunnel tetap berjalan
try:
    ngrok.get_ngrok_process().proc.wait()
except KeyboardInterrupt:
    print("\nTunnel dihentikan.")
    ngrok.kill()
