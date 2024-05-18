'''
Author: Feng-Hao, Yeh
Email: zzz3x2c1@gmail.com, yeh.feng.hao@try-n-go.com
Discord: thebestyea
'''

from typing import Tuple

class Huffman_Node:
    _NODE_VALUE: int = -1
    _NODE_BIT: int = 0
    _DATA_BIT: int = 1

    def __init__(self: 'Huffman_Node', value: int = _NODE_VALUE, frequency: int = 0) -> None:
        self.left: Huffman_Node = None
        self.right: Huffman_Node = None
        self.value: int = value
        self.frequency: int = frequency

    @staticmethod
    def __concat_bit(left_bytes_array: bytearray, left_bit_index: int, right_bytes_array: bytearray) -> bytearray:
        result = bytearray(left_bytes_array)
        for i in range(len(right_bytes_array)):
            result, left_bit_index = Huffman_Node.__put_byte(result, right_bytes_array[i], left_bit_index)
        return result, left_bit_index

    @staticmethod
    def __put_bit(bytes_array: bytearray, bit: int, bit_index: int) -> Tuple[bytearray, int]:
        current_bit_index = bit_index & 0x7
        byte_index = bit_index >> 3
        if(byte_index == len(bytes_array)):
            bytes_array = bytes_array + bytearray([0])
        bytes_array[byte_index] |= (bit << current_bit_index)
        return bytes_array, bit_index + 1
    
    @staticmethod
    def __get_bit(bytes_array: bytearray, bit_index: int) -> Tuple[int, int]:
        current_bit_index = bit_index & 0x7
        byte_index = bit_index >> 3
        if(byte_index >= len(bytes_array)):
            raise AssertionError("Bit index out of range.")
        return (bytes_array[byte_index] >> current_bit_index) & 1, bit_index + 1

    @staticmethod
    def __put_byte(bytes_array: bytearray, byte: int, bit_index: int) -> Tuple[bytearray, int]:
        for _ in range(8):
            bytes_array, bit_index = Huffman_Node.__put_bit(bytes_array, byte & 1, bit_index)
            byte >>= 1
        return bytes_array, bit_index
    
    @staticmethod
    def __get_byte(bytes_array: bytearray, bit_index: int) -> Tuple[int, int]:
        value = 0
        for i in range(8):
            bit, bit_index = Huffman_Node.__get_bit(bytes_array, bit_index)
            value = value | (bit << i)
        return value, bit_index
        
    def __Is_Node(self):
        return self.value == Huffman_Node._NODE_VALUE
    
    def __Set_As_Node(self):
        self.value = Huffman_Node._NODE_VALUE
    
    def Encode_Node_To_Bytes(self: 'Huffman_Node', bytes_array: bytearray = bytearray(), bit_index: int = 0) \
        -> Tuple[bytearray, int]:
        if(self.__Is_Node()):
            bytes_array, bit_index = Huffman_Node.__put_bit(bytes_array, Huffman_Node._NODE_BIT, bit_index)
            bytes_array, bit_index = self.left.Encode_Node_To_Bytes(bytes_array, bit_index)
            bytes_array, bit_index = self.right.Encode_Node_To_Bytes(bytes_array, bit_index)
        else:
            bytes_array, bit_index = Huffman_Node.__put_bit(bytes_array, Huffman_Node._DATA_BIT, bit_index)
            bytes_array, bit_index = Huffman_Node.__put_byte(bytes_array, self.value, bit_index)
        return bytes_array, bit_index
    
    def __Decode_Byte_To_Nodes(self: 'Huffman_Node', bytes_array: bytearray = bytearray(), bit_index: int = 0) \
        -> Tuple[bytearray, int, 'Huffman_Node']:
        bit, bit_index = Huffman_Node.__get_bit(bytes_array, bit_index)
        if(bit == Huffman_Node._NODE_BIT):
            self.__Set_As_Node()
            bit_index, left = Huffman_Node().__Decode_Byte_To_Nodes(bytes_array, bit_index)
            bit_index, right = Huffman_Node().__Decode_Byte_To_Nodes(bytes_array, bit_index)
            self.left = left
            self.right = right
        else:
            self.value, bit_index = Huffman_Node.__get_byte(bytes_array, bit_index)
        return bit_index, self
    
    def __create_node_dict(self: 'Huffman_Node', dict: dict = {}, current_deep: int = 0, \
        current_bits: bytearray = bytearray(), current_bit_length: int = 0) -> dict:
        if(self.__Is_Node()):
            left_bits, left_bit_length = Huffman_Node.__put_bit(bytearray(current_bits), 0, current_bit_length) # Node Left
            self.left.__create_node_dict(dict, current_deep + 1, left_bits, left_bit_length)
            right_bits, right_bit_length = Huffman_Node.__put_bit(bytearray(current_bits), 1, current_bit_length) # Node Right
            self.right.__create_node_dict(dict, current_deep + 1, right_bits, right_bit_length)
        else:
            dict[self.value] = (current_bits, current_deep)
        return dict

    def Encode_Data(self: 'Huffman_Node', bytes_array: bytearray = bytearray()) -> Tuple[bytearray, int]:
        result = bytearray()
        bit_index = 0
        dict = self.__create_node_dict()
        total_bits_length = 0
        for i in range(len(bytes_array)):
            encoded_bits, bits_length = dict[bytes_array[i]]
            total_bits_length += bits_length
            current_bit_index = 0
            for j in range(bits_length):
                result, bit_index = Huffman_Node.__put_bit(result, (encoded_bits[current_bit_index >> 3] >> (j & 0x7)) & 1, bit_index)
                current_bit_index += 1
        return result, total_bits_length
    
    def Decode_Data(self: 'Huffman_Node', bytes_array: bytearray = bytearray()) -> bytearray:
        bit_index = 0
        target_index = (len(bytes_array) << 3) - self.frequency # As a decoded node, the head frequency indicates the bits to ignore.
        result = bytearray()
        while(bit_index < target_index):
            node = self
            while(bit_index <= target_index):
                if(not node.__Is_Node()):
                    result = result + bytearray([node.value])
                    break
                bit, bit_index = Huffman_Node.__get_bit(bytes_array, bit_index)
                node = node.left if bit == 0 else node.right
        return result

    @staticmethod
    def Decode_To_Nodes(bytes_array: bytearray = bytearray()) -> 'Huffman_Node':
        head = Huffman_Node()
        head.frequency = bytes_array[0] # As a decoded node, the head frequency indicates the bits to ignore.
        bytes_array = bytes_array[1:]
        head.__Decode_Byte_To_Nodes(bytes_array)
        return head
        