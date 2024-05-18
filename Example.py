'''
Author: Feng-Hao, Yeh
Email: zzz3x2c1@gmail.com, yeh.feng.hao@try-n-go.com
Discord: thebestyea
'''

from Huffman.Huffman_Helper import Huffman_Helper

# Create original data containing bytes from 0 to 255
original_data = bytearray([i for i in range(256)])

# Encode the original data using Huffman encoding
encoded_data, tree_bytes = Huffman_Helper.Encode(original_data)

# Decode the encoded data back to its original form
decoded_data = Huffman_Helper.Decode(encoded_data, tree_bytes)

# You could save both encoded_data and tree_bytes to a file or use them in any way you need

# Check if the decoded data matches the original data
print(f'Decoded data is equal to the original data: {original_data == decoded_data}')
