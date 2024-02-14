import socket
import sys

## Data parsing helpers ##
def extractArgument(): # extracts the url passed in the cmd
    if len(sys.argv) > 1:
        return sys.argv[1]  
    else:
        print("No arguments received.", file=sys.stderr)
        sys.exit(1)

def extractHeaderBody(stringData): # returns the header and body of the response
    separatedData = stringData.split("\r\n\r\n")
    headers = separatedData[0]
    body = ""
    if len(separatedData) > 1:
        body = separatedData[1]

    return (headers, body)

def extractField(stringData, field): # can extract any field in the header
    if field in stringData:
        separatedData = stringData.split(field)
        holder = separatedData[1]
        newSplit = holder.split("\r\n")

        return newSplit[0]

    return "-1"
 
def getResponseCode(headers): # extracts the response code
    responseCode = headers[9:12]

    return int(responseCode)

def sanitizeInput(hostName): # checks if url is valid and extracts the host, port and paths
    if hostName.startswith("https"):
        print("Error: cannot handle https", file=sys.stderr)
        sys.exit(1)
    elif hostName.startswith("http://"):
        noPrefix = hostName[7:len(hostName)]
        sepNoPrefix = noPrefix.split("/")
        path = "/".join(sepNoPrefix[1:])
        hostPort = sepNoPrefix[0]
        if ":" in hostPort:
            host, port = hostPort.split(":")
        else:
            host = hostPort
            port = 80
        return (host,path,int(port))

    else:
        sys.exit(1)

## request sending helpers ##

def sendRequest(host, path, port): # sends request using socket
    obj = socket.socket()
    obj.connect((host, port))

    request = f"GET /{path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
    obj.sendall(request.encode())

    response = ""
    
    while True:
        chunk = obj.recv(4096)
        if not chunk:
            break  # Server closed the connection, no more data
        response += chunk.decode()
  
    obj.close()

    return response


def handleRedirect(data, responseCode, count): # redirects url using recursion
    if count >= 10:
        sys.exit(1)

    if responseCode == 301 or responseCode == 302:
        newLocation = extractField(data.lower(), "location: ")
    else:
        return data

    print(f"Redirected to: {newLocation}", file=sys.stderr)

    newHost, newPath, newPort = sanitizeInput(newLocation)
    newData = sendRequest(newHost, newPath, newPort)
    newResponseCode = getResponseCode(newData)

    result = handleRedirect(newData, newResponseCode, count+1)

    return result

## main ##

def main():
    url = extractArgument()
    host, path, port = sanitizeInput(url) 

    data = sendRequest(host, path, port)

    responseCode = getResponseCode(data)
    data = handleRedirect(data, responseCode, 0)
   
    responseCode = getResponseCode(data)

    headers, body = extractHeaderBody(data)
    contentType = extractField(data, "Content-Type: ")
   
    if responseCode == 200:
        if contentType.startswith('text/html'):
            print(body, file=sys.stdout)
            sys.exit(0)
        else:
            sys.exit(1)
        
    elif responseCode >= 400:
        if contentType.startswith('text/html'):
            print(body, file=sys.stdout)
        sys.exit(1)
    else:
        sys.exit(1)


main()