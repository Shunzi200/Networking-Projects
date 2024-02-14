
# Networking Projects

This repository contains a collection of Python scripts demonstrating basic networking concepts and implementations. Each script serves as a standalone project showcasing different aspects of network programming, from simple HTTP server operations to simulating TCP functionality over a lossy network.

## Projects Overview

### `curl-clone.py`
A simplified version of the `curl` tool, designed for fetching web resources using HTTP GET requests. It showcases basic network programming concepts, handling of HTTP protocols, and response parsing.

### `TCP.py`
Implements a basic version of TCP over a simulated lossy network environment, demonstrating reliable data transmission, packet sequencing, acknowledgments, and handling of network unreliabilities.

### `http_server.py`
A basic HTTP server capable of handling GET requests and serving static HTML content. It illustrates how to set up a server, manage incoming connections, and serve web content based on request paths.

## Getting Started
To use these scripts, clone the repository and navigate to the desired project directory. Each script is designed to be run independently, with usage instructions detailed in the respective project sections below.

### Prerequisites
- Python 3.x
- Basic understanding of networking concepts

## Project Details

### `curl_clone.py`
#### Features
- HTTP GET request handling
- Command-line URL input
- HTTP redirect following

#### Usage
Run the script with a URL as an argument to fetch and display the content of the specified web page.

### `TCP.py`
#### Features
- TCP-like reliability over UDP
- Sequence numbering and acknowledgments
- Data integrity checks with MD5

#### Usage
Instantiate and use the `Streamer` class within your Python scripts to simulate TCP's reliable data transmission over an unreliable network.

### `http_server.py`
#### Features
- Basic HTTP GET request handling
- Static HTML content serving
- Customizable listening port

#### Usage
Run the script with a port number to start the server, then access served content using a web browser or a tool like `curl`.
