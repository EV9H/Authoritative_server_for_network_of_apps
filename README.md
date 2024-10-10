# Authoritative_server_for_network_of_apps

### Instruction to Run (docker)

In /dns_app: (Windows Powershell)
```
docker network create dns_net; cd us; docker build -t us:latest .; cd ..; cd fs; docker build -t fs:latest .; cd ..; cd as; docker build -t as:latest .; cd ..; docker run --network dns_net --name as_server -p 53533:53533/udp -d as:latest; docker run --network dns_net --name fs_server -p 9090:9090 -d fs:latest; docker run --network dns_net --name us_server -p 8080:8080 -d us:latest
```

Use 
```
docker inspect dns_net
```
to get the ip of as,us,fs server. 

### Query example
- PUT query to http://localhost:9090/register
with body 
{
    "hostname": "fibonacci.com", 
    "ip": "172.18.0.3", 
    "as_ip": "172.18.0.2",
    "as_port": "53533"
}
- GET query to: 
http://localhost:8080/fibonacci?hostname=fibonacci.com&fs_port=9090&number=8&as_ip=172.18.0.2&as_port=53533