import cv2
import numpy as np
import socket 
import struct
import math
import io
import time
from PIL import Image


MAX_DGRAM = 2**16
MAX_IMAGE_DGRAM = MAX_DGRAM - 64
SOC = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
PORT = 12345
ADDR = "localhost"

def calculate_chunk_num(packet_size):
    return math.ceil(packet_size / (MAX_IMAGE_DGRAM))

def get_packet_size(encoded_image):
    return len(encoded_image)

def create_packet_chunk(encoded_image, chunk_count, pos_start, pos_end):
    return struct.pack("B", chunk_count) + encoded_image[pos_start:pos_end]

def send_packet_chunk(chunk):
    SOC.sendto(chunk, (ADDR, PORT))
    return

def compress_image(img):
    """
    Encode jpeg image and return compressed binary image
    """

    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]
    result, encimg = cv2.imencode('.jpg', img, encode_param)
    if result == False:
        print('could not encode image!')
        exit()

    dat = encimg.tobytes()
    return dat

def transform_from_byte_to_string(data_in_byte):
    data_in_byte_string = str(data_in_byte)
    return data_in_byte_string

def run():
    img = cv2.imread("image/4k_image_sample.jpeg")
    compressed_image = compress_image(img)
    data_in_byte_string = transform_from_byte_to_string(compressed_image)
    packet_size = get_packet_size(data_in_byte_string)
    
    print("Packet size: ", packet_size)
    chunk_num = calculate_chunk_num(packet_size)
    print("Chunk num: ", chunk_num)
    
    pos_start = 0
    while chunk_num:
        pos_end = min(packet_size, pos_start + MAX_IMAGE_DGRAM)
        packet_chunk = create_packet_chunk(compressed_image, chunk_num, pos_start, pos_end)
        print("Packet chunk: ", packet_chunk)
        send_packet_chunk(packet_chunk)
        pos_start = pos_end
        chunk_num -= 1

def main():
    """ Top level main function """
    count_num = 100

    while count_num > 0:
        run()
        time.sleep(5)
        count_num -= 1
    
    cv2.destroyAllWindows()
    SOC.close()

if __name__ == "__main__":
    main()