
# curl-clone.py

## Description
A lightweight Python script that mimics the basic functionality of the `curl` command for fetching resources from the web. It's designed to handle HTTP GET requests and is capable of following redirects, making it a useful tool for testing and interacting with web servers in a simplified manner.

## Features
- **HTTP GET Requests**: Sends HTTP GET requests to fetch resources from web servers.
- **Command-line URL Input**: Allows users to specify the target URL directly from the command line.
- **Redirect Handling**: Automatically follows HTTP redirects up to a predefined limit.

## Usage
To use `curl-clone.py`, run the script from the command line with the desired URL as an argument. The script will then attempt to fetch the resource and display its content if the content type is `text/html`.

```bash
python3 curl-clone.py [URL]
```

## Limitations
- The script only supports HTTP URLs and will not work with HTTPS.
- It is primarily intended for educational and testing purposes and may not include all features of the actual `curl` command.

## Requirements
- Python 3.x
