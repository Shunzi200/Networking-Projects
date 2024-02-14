# do not import anything else from loss_socket besides LossyUDP
from lossy_socket import LossyUDP
# do not import anything else from socket except INADDR_ANY
from socket import INADDR_ANY
import struct
import heapq
from concurrent.futures import ThreadPoolExecutor
import time 
import hashlib
import threading

class Streamer:
    def __init__(self, dst_ip, dst_port,
                 src_ip=INADDR_ANY, src_port=0):
        """Default values listen on all network interfaces, chooses a random source port,
           and does not introduce any simulated packet loss."""
        self.socket = LossyUDP()
        self.socket.bind((src_ip, src_port))
        self.dst_ip = dst_ip
        self.dst_port = dst_port
        self.sequenceNumberSending = 0
        self.sequenceNumberArrival = 0
        self.ackNumber = 0 
        self.buffer = {}
        self.ackBuffer = {}
        self.closed = False
        self.finAck = False
        self.fin = False

        executor = ThreadPoolExecutor(max_workers=1)
        executor.submit(self.listener)  
        #print("opening")

    def compute_hash(self, packet):
        return hashlib.md5(packet).digest()

    def buildTCPPacket(self, seg, ack, ackFlag, finFlag, chunk):
        chunkHash = self.compute_hash(chunk)  # Compute hash of the chunk.
        chunkSize = len(chunk)
        hashSize = len(chunkHash)
        formatString = f"IIbb{hashSize}s{chunkSize}s"
        packedData = struct.pack(formatString, seg, ack, ackFlag, finFlag, chunkHash, chunk)
        return packedData

    def send(self, data_bytes: bytes) -> None:
        """Note that data_bytes can be larger than one packet."""
        
        bytesSplit = []
        sizeBytes = len(data_bytes)

        for i in range(0, sizeBytes, 1446): # splits the bytes in chunks of 1446 bytes (that way each package data is 1472 bytes when counting the header and ACK byte)
            chunk = data_bytes[i:i+1446]
            chunkSize = len(chunk)
            packedData = self.buildTCPPacket(self.sequenceNumberSending, 0000, 0, 0, chunk)
            bytesSplit.append((self.sequenceNumberSending, packedData))
            self.sequenceNumberSending += chunkSize

        for seq, packedChunk in bytesSplit:
            self.socket.sendto(packedChunk, (self.dst_ip, self.dst_port))

            startTime = time.time()

            while seq not in self.ackBuffer: 
                current = time.time()
                if current-startTime > 0.25: # resend packet after time out
                    self.socket.sendto(packedChunk, (self.dst_ip, self.dst_port))     
                    startTime =  time.time()
                time.sleep(0.01)
                
    def recv(self) -> bytes:
        """Blocks (waits) if no data is ready to be read from the connection."""

        while self.sequenceNumberArrival not in self.buffer: # until we have the correct segment we want, keep waiting
            pass
        
        correctChunk = self.buffer[self.sequenceNumberArrival] # get the correct segment

        headerSize = 10
        hashSize = 16  # MD5 hash size in bytes
        correctChunkSize = len(correctChunk) - headerSize - hashSize

        unpackFormat = f"IIbb{hashSize}s{correctChunkSize}s"
        sequence, ack, ackFlag, finFlag, receivedHash, payload  = struct.unpack(unpackFormat, correctChunk)
        self.sequenceNumberArrival += correctChunkSize # update the sequence number we need to receive

        return payload
    
    def listener(self):
        while not self.closed: 
            try:
                data, addr = self.socket.recvfrom() # receive
                if len(data) <= 0 :
                    continue
                
                headerSize = 10 
                hashSize = 16  # MD5 hash size
                payloadSize = len(data) - headerSize - hashSize  # Calculate payload size
                
                # Unpack the data to get the payload and then the hash.
                unpackFormat = f"IIbb{hashSize}s{payloadSize}s"
                sequence, ack, ackFlag, finFlag, receivedHash, payload  = struct.unpack(unpackFormat, data)
            
                
                computedHash = self.compute_hash(payload)
            
                if receivedHash != computedHash:
                    #print("Hash mismatch detected, discarding corrupted packet.")
                    continue


                if ackFlag == 0 and finFlag == 0:
                    self.buffer[sequence] = data # add it to queue, sorted by sequence number
                    self.ackNumber +=1
                    packedData = self.buildTCPPacket(sequence, self.ackNumber,1,0, b'')
                    self.socket.sendto(packedData, (self.dst_ip, self.dst_port))  

                elif ackFlag == 1 and finFlag == 0:
                    self.ackBuffer[sequence] = ack # received ack

                elif ackFlag == 0 and finFlag == 1:
                    self.fin = True
                    #print("got fin, sending finACK")
                    packedData = self.buildTCPPacket(self.sequenceNumberSending+1, 0000, 1, 1, b'') # send ACKFIN
                    self.socket.sendto(packedData, (self.dst_ip, self.dst_port))  

                elif finFlag == 1 and ackFlag == 1:
                    self.finAck = True
                    #print("got finACk")

            except Exception as e:
                print("listener died!")
                print(e)

    def close(self) -> None:
        """Cleans up. It should block (wait) until the Streamer is done with all
           the necessary ACKs and retransmissions"""
        #print("close function")
        
        packedData = self.buildTCPPacket(self.sequenceNumberSending+1, 0000, 0, 1, b'')
        self.socket.sendto(packedData, (self.dst_ip, self.dst_port))  
        #print("sending fin")
        startTime = time.time()
        
        while not self.finAck: 
            current = time.time()
            if current-startTime > 0.25: # resend packet after time out
                self.socket.sendto(packedData, (self.dst_ip, self.dst_port))   # resends FIN packet 
                #print("resending FIN")
                startTime =  time.time()
            time.sleep(0.01)

        while not self.fin:
            time.sleep(0.01)

        #print("waiting 2")
        time.sleep(2)

        #print("closing")
        self.closed = True
        self.socket.stoprecv()