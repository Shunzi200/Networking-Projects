import socket
import os
import sys
import select

def extractArgument():
    if len(sys.argv) > 1:
        return int(sys.argv[1])

def extractFileName(requestString):
    suffixSlice = requestString[4:len(requestString)]  # slices to avoid the GET keyword
    separatedData = suffixSlice.split(" HTTP")  # splits on HTTP so the first is the filename
    fileName = separatedData[0][1:len(separatedData[0])]  # ignores the starting / of the name

    if fileName.endswith(".html") or fileName.endswith(".htm"):
        if checkFileInDir(fileName):
            return (fileName, 200)
        return (fileName, 404)

    return (fileName, 403)

def checkFileInDir(fileName):
    return os.path.exists(fileName)

def handleRequest(clientSocket):
    try:
        request = clientSocket.recv(4096)
    except socket.error as e:
        return None, None

    if not request:
        return None, None  # Handle empty request by returning None

    requestString = request.decode()

    # Check if the request starts with "GET"
    if not requestString.startswith("GET"):
        return None, None

    fileName, responseCode = extractFileName(requestString)
    return fileName, responseCode

def sendResponse(clientSocket, fileName, responseCode):
    if responseCode == 200:
        with open(fileName, 'rb') as file:
            fileContent = file.read()
        responseHeader = f"HTTP/1.0 200 OK\r\nContent-Length: {len(fileContent)}\r\n\r\n".encode()
        clientSocket.sendall(responseHeader + fileContent)
    elif responseCode == 404:
        response = "HTTP/1.0 404 Not Found\r\nContent-Length: 14\r\n\r\nFile not found".encode()
        clientSocket.sendall(response)
    else:  # responseCode == 403
        response = "HTTP/1.0 403 Forbidden\r\nContent-Length: 14\r\n\r\nAccess denied".encode()
        clientSocket.sendall(response)

def main():
    port = extractArgument()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("", port))
    server.listen(5)
    open_connections = [server]

    while True:
        read_sockets, _, _ = select.select(open_connections, [], [])

        for sock in read_sockets:
            if sock is server:
                clientSocket, clientAddress = server.accept()
                open_connections.append(clientSocket)
            else:
                fileName, responseCode = handleRequest(sock)
                if fileName is not None:  # Only send a response if the request was valid
                    sendResponse(sock, fileName, responseCode)
                open_connections.remove(sock)
                sock.close()

if __name__ == "__main__":
    main()