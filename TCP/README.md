
# TCP.py

## Description
This Python script simulates TCP's reliability and transmission control mechanisms over an unreliable network environment, showcasing how TCP achieves reliable data transmission through sequence numbering, acknowledgments, and retransmissions. The script uses a `Streamer` class for managing connections and data flow, emphasizing the TCP-like behavior in handling packet loss, reordering, and ensuring data integrity.

## Features
- **TCP-like Reliability**: Ensures data transmission reliability over an unreliable network, simulating TCP's behavior.
- **Sequence Numbering and Acknowledgments**: Utilizes sequence numbers for packets and acknowledgments to confirm receipt, maintaining data order and integrity.
- **Data Integrity Checks**: Employs MD5 checksums to verify data integrity upon receipt.
- **Packet Loss and Reordering Handling**: Manages packet loss and reordering through retransmissions and sequence control.

## Usage
The script is intended to be used within Python programs. Instantiate the `Streamer` class with destination and source IP/port information, then use the `send` and `recv` methods for data transmission.

```python
from TCP import Streamer
# Instantiate the Streamer
streamer = Streamer(dst_ip, dst_port, src_ip, src_port)
# Send data
streamer.send(data_bytes)
# Receive data
received_data = streamer.recv()
```

## Limitations
- The script is a simplified representation of TCP and does not cover all aspects, such as congestion control.
- Intended for educational purposes and may not be suitable for real-world applications.

## Requirements
- Python 3.x
- `lossy_socket` module for simulating network conditions

## Run
In separate terminals, run:
```bash
python3 test.py 8000 8001 1
```
```bash
python3 test.py 8000 8001 2
```