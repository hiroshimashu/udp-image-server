import cv2
import numpy as np
import socket 
import struct
import math
import io
from PIL import Image

MAX_DGRAM = 2 ** 16

def concate_data_segment(dat, data_segment):
      NotImplemented
            

def dump_buffer(s):
  """Emptying buffer frame"""
  print("Dump buffer started")
  while True:
    seg, addr = s.recvfrom(MAX_DGRAM)
    if struct.unpack("B", seg[0:1])[0] == 1:
      print("finish emptying buffer")
      break

def main():
  """Getting image udp frame & concate before decode and output image"""
  # Set up socket
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.bind(('localhost', 12345))
  dat = b''
  dataSegement = [0] * 5

  while True:
    seg, addr = s.recvfrom(MAX_DGRAM)
    print("type: ", type(seg))
    chunk_number = struct.unpack("B", seg[0:1])[0]
    if chunk_number > 1:
        print("chunk_number: ", chunk_number)
        dat += seg[1:]
    else:
        dat += seg[1:]
        img = cv2.imdecode(np.frombuffer(dat, dtype=np.uint8), 1)
        cv2.imwrite("image/4k_image_sample_compressed.jpg", img)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    dat = b""

if __name__ == "__main__":
    main()