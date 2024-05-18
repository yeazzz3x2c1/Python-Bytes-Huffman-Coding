'''
Author: Feng-Hao, Yeh
Email: zzz3x2c1@gmail.com, yeh.feng.hao@try-n-go.com
Discord: thebestyea
'''

import random
import secrets
from Huffman.Huffman_Helper import Huffman_Helper

test_times = 100  # Number of times to run the test

for i in range(test_times):
    # Generate a random length for the test data
    data_length = random.randint(100, 16384000)
    # Generate random bytes of the specified length
    test_data = secrets.token_bytes(data_length)

    # Create original data containing bytes from 0 to 255
    original_data = bytes([i for i in range(256)])
    # Encode the original data using Huffman encoding
    encoded_data, tree_bytes = Huffman_Helper.Encode(original_data)
    # Decode the encoded data back to its original form
    decoded_data = Huffman_Helper.Decode(encoded_data, tree_bytes)
    
    # Verify if the decoded data matches the original data
    if original_data != decoded_data:
        print("Testing Failed.")
        exit()

print("Testing Passed.")