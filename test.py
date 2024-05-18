'''
Author: Feng-Hao, Yeh
Email: zzz3x2c1@gmail.com, yeh.feng.hao@try-n-go.com
Discord: thebestyea
'''

import random
import secrets
from Huffman.Huffman_Helper import Huffman_Helper

test_times = 10  # Number of times to run the test

for i in range(test_times):
    # Generate a random length for the test data
    data_length = random.randint(100, 1638400)
    # Generate random bytes of the specified length
    testing_data = secrets.token_bytes(data_length)

    # Encode the testing data using Huffman encoding
    encoded_data, tree_bytes = Huffman_Helper.Encode(testing_data)
    # Decode the encoded data back to its original form
    decoded_data = Huffman_Helper.Decode(encoded_data, tree_bytes)
    
    # Verify if the decoded data matches the testing data
    if testing_data != decoded_data:
        print("Testing Failed.")
        exit()

    print(f'==================[Test {i}]==================')
    print(f'Testing data length: {len(testing_data)}')
    print(f'Encoded data length: {len(encoded_data)}')
    print(f'Tree data length: {len(tree_bytes)}')
    print(f'Compressed rate without tree: {(len(encoded_data) / len(testing_data) * 100):.2f}%')
    print(f'Compressed rate with tree: {(((len(encoded_data) + len(tree_bytes)) / len(testing_data)) * 100):.2f}%')

print("Testing Passed.")

# Final output: Testing Passed.