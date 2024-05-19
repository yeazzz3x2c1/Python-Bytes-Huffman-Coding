'''
Author: Feng-Hao, Yeh
Email: zzz3x2c1@gmail.com, yeh.feng.hao@try-n-go.com
Discord: thebestyea
'''

from typing import Tuple
from .Huffman_Node import Huffman_Node
import base64

class Huffman_Helper:
    @staticmethod
    def __create_frequency_nodes(data: bytearray) -> list[int]:
        frequency = [0] * 256
        for i in range(len(data)):
            frequency[data[i]] += 1
        result = []
        for i in range(256):
            if(frequency[i] > 0):
                result.append(Huffman_Node(i, frequency[i]))
        return result
    
    @staticmethod
    def __create_tree(freq: list[Huffman_Node]) -> Huffman_Node:
        if(len(freq) == 0):
            return Huffman_Node()
        while(len(freq) > 1):
            freq.sort(key=lambda node: node.frequency)
            l = freq.pop(0)
            r = freq.pop(0)
            new_node = Huffman_Node(value=-1, frequency=l.frequency + r.frequency)
            new_node.left = l
            new_node.right = r
            freq.append(new_node)
        return freq[0]
    
    def Encode(data: bytearray) -> Tuple[bytearray, bytearray]:
        freq = Huffman_Helper.__create_frequency_nodes(data)
        tree = Huffman_Helper.__create_tree(freq)
        encoded_data, total_bit_length = tree.Encode_Data(data)
        tree_bytes, _ = tree.Encode_Node_To_Bytes()
        # The first byte indicates the number of bits to ignore at the tail.
        tree_bytes = bytearray([0 if (total_bit_length & 0x7) == 0 else 0x8 - (total_bit_length & 0x7)]) + tree_bytes
        return encoded_data, tree_bytes

    def Decode(encoded_data: bytearray, tree_bytes: bytearray) -> bytearray:
        tree = Huffman_Node.Decode_To_Nodes(tree_bytes)
        return tree.Decode_Data(encoded_data)

    def Compress_Data(data: bytearray) -> Tuple[bytearray, bytearray]:
        return Huffman_Helper.Encode(base64.b64encode(data))

    def Decompress_Data(compressed_data: bytearray, tree_bytes: bytearray) -> bytearray:
        return base64.b64decode(Huffman_Helper.Decode(compressed_data, tree_bytes))