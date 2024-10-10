from flask import Flask, request
import requests 
import socket 
app = Flask(__name__)


@app.route('/')
def hello():
    return "HELLO"

@app.route('/fibonacci', methods = ['GET'])
def fibonacci():
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')

    # any missing then respond with 400 
    if hostname and fs_port and number and as_ip and as_port:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            msg = f"TYPE=A\nNAME={hostname}".encode()
            s.sendto(msg, (as_ip, int(as_port)))
            
            response, addr = s.recvfrom(1024)
            s.close()
            response = response.decode().split('\n')
            
            for line in response:   
                if "=" in line:
                    k,v = line.split("=")
                    if k == "VALUE":
                        ip = v
                        response = requests.get(f"http://{ip}:{fs_port}/fibonacci?number={number}")
                        return response.text, response.status_code
        except Exception as e:
            return f"Error: {e}", 500
        return "Hostname not found", 404
    else:
        return "BAD REQUEST", 400
if __name__ == "__main__":
    # Docker command (powershell)
    # docker build -t us . ; docker run -it -p 8080:8080 us
    app.run(host="0.0.0.0", port= 8080, debug=True)