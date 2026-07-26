import socket

from app import create_app

if __name__ == "__main__":
    app = create_app()
    
    # Get local IP
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    # print("="*60)
    # print(f"✅ Server running!")
    # print(f"   Local:     http://127.0.0.1:5000")
    # print(f"   Network:   http://{local_ip}:5000")
    # print("="*60)
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        ssl_context=('127.0.0.1+3.pem', '127.0.0.1+3-key.pem')
    )