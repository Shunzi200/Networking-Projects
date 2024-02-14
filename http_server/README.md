
# http_server.py

## Description
This script is a basic implementation of an HTTP server that listens for incoming connections and serves static HTML files. It handles HTTP GET requests, checks for file existence and type, and returns appropriate responses. It's designed to demonstrate the fundamental workings of a web server, including connection handling, request processing, and response delivery.

## Features
- **HTTP GET Request Handling**: Processes incoming HTTP GET requests to serve content.
- **Static Content Serving**: Serves static HTML files from the server's directory.
- **Content-Type Validation**: Only serves files with `.html` or `.htm` extensions for security reasons.
- **Response Status Codes**: Returns HTTP 200, 404, or 403 status codes based on the request and file availability.

## Usage
Run the script with a port number as an argument. The server will listen on the specified port for incoming connections. Access the served content using a web browser or a tool like `curl` by navigating to `http://localhost:<port>/<file_name>`.

```bash
python http_server.py <port>
```

## Limitations
- The server is basic and intended for educational purposes, lacking advanced features like dynamic content handling, HTTPS support, or comprehensive security measures.

## Requirements
- Python 3.x
