from flask import Flask, request
import socket 

app = Flask(__name__)

@app.route('/')
def hello():
    return "HELLO This is Fibonacci Server"

@app.route('/register', methods = ['PUT'])
def register():
    data = request.get_json()
    hostname = data.get('hostname')
    ip = data.get('ip')
    as_ip = data.get('as_ip')
    as_port = data.get('as_port')

    if hostname and ip and as_port and as_ip:
        dns_msg = f"TYPE=A\nNAME={hostname}\nVALUE={ip}\nTTL=10"
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(dns_msg.encode(), (as_ip, int(as_port)))
        s.close()

        return 'Successfully Registered.', 201


@app.route('/fibonacci', methods = ['GET'])
def fibonacci():
    number = request.args.get('number')
    try:
        if number.isdigit() and int(number) >= 0:
            X = int(number)
            res = 0
            if X in [0,1]:
                res = X
            else:
                a = 0 
                b = 1
                for i in range(1,X):
                    c = a + b 
                    a = b 
                    b = c
                res = b
            return str(res), 200
        else: 
            return 'Bad Request: sequence is not integer or less than zero. ', 400
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    # Docker command (powershell)
    # docker build -t fs . ; docker run -it -p 9090:9090 fs
    app.run(host="0.0.0.0", port = 9090, debug=True)

