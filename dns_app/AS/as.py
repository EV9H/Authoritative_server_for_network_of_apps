import socket 

dns_records = {}

def register(data):
    name = value = ""

    data = data.split('\n')
    
    is_type_A = False
    try:
        for l in data:
            k,v = l.split('=')
            if k == 'TYPE' and v =='A':
                is_type_A = True
            elif k == 'NAME':
                name = v
            elif k == 'VALUE':
                value = v
            else:
                # TTL 
                pass

        if is_type_A and name and value:
            dns_records[name] = value
            return "Registered"
        else:
            return "Invalid Registration"
    except Exception as e:
        return 'Error: ' + str(e)
    

def query(q):
    name = ""
    is_type_A = False

    q = q.split("\n")
    try:
        for l in q:
            k,v = l.split("=")
            if k == "TYPE" and v == "A":
                is_type_A = True
            
            elif k == "NAME":
                name = v

        if is_type_A and name in dns_records:
            
            return f"TYPE=A\nNAME={k}\nVALUE={dns_records[v]}\nTTL=10"
        return "NOT FOUND"

    except Exception as e:
        return 'Error: ' + str(e)
    
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('0.0.0.0',53533))
local_ip, local_port = s.getsockname()
while True:
    data, addr = s.recvfrom(1024)
    if data:
        data = data.decode()
        if 'VALUE' in data:
            response = register(data)
        else:
            response = query(data)
        
        s.sendto(response.encode(), addr)
