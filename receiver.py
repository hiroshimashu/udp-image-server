import cv2
import numpy as np
import socket 
import struct
import math
import io
from PIL import Image

MAX_DGRAM = 2 ** 16

def dump_buffer(s):
  """Emptying buffer frame"""
  while True:
    seg, addr = s.recvfrom(MAX_DGRAM)
    print(seg[0])
    if struct.unpack("B", seg[0:1])[0] == 1:
      print("finish emptying buffer")
      break



def get_chunk_number(chunk):
    return struct.unpack("B", chunk[0:1])[0]

def get_chunk_body(chunk):
    return chunk[1:]

def transform_to_np_array(bytes):
    return np.frombuffer(bytes, dtype="uint8")

def decode_buffer_img(socket):
  received_data = bytes()
  while True:
    seg, addr = socket.recvfrom(MAX_DGRAM)
      
    chunk_number = get_chunk_number(seg)
    if chunk_number > 1:
      received_data += get_chunk_body(seg)
    else:
      received_data += get_chunk_body(seg)
      img = cv2.imdecode(transform_to_np_array(received_data), 1)

def show_image(data_in_bytes):
  print("Try to show image...")
  try:
    img = cv2.imdecode(transform_to_np_array(data_in_bytes), 1)
    result = cv2.imshow('image', img)
    if result:
      print("Successfully show image")
      return
    print("Failed to save image")
  except Exception as e:
    print(e)

def main():
  """Getting image udp frame & concate before decode and output image"""
  data_in_bytes = b''
  # Set up socket
  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  sock.bind(('localhost', 12345))
  dump_buffer(sock)
  
  while True:
    print ("Waiting to receive message from client") 
    data, addr = sock.recvfrom(MAX_DGRAM)

    print ("received %s bytes from %s" % (len(data), addr))
    print("Data: %s" % data)

    if struct.unpack("B", data[0:1])[0] > 1:
      data_in_bytes += data[1:]
    else:
      data_in_bytes += data[1:]
      show_image(data_in_bytes)
      if cv2.waitKey(1) & 0xFF == ord('q'):
        break
      data_in_bytes = b''
  cv2.destroyAllWindows()
  sock.close()


if __name__ == "__main__":
  main()