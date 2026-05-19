from __future__ import annotations
from dataclasses import dataclass, field

@dataclass(order=True, frozen=True)
class Node:
    freq: int
    char: str
    left: Node | None = None
    right: Node | None = None

    def __str__(self):
        return f"Node: {self.char}, Freq: {self.freq}"

@dataclass(frozen=True)
class MinHeap:
    data: list[Node] = field(default_factory=list)

def heapify_up(heap: MinHeap, index: int) -> MinHeap:
    data = heap.data[:]
    while index > 0:
        parent_index = (index - 1) // 2
        if data[index] < data[parent_index]:
            data[index], data[parent_index] = data[parent_index], data[index]
            index = parent_index
        else:
            break
    return MinHeap(data)

def insert(heap: MinHeap, element: Node) -> MinHeap:
    data = heap.data[:] + [element]
    return heapify_up(MinHeap(data), len(data) - 1)

def heapify_down(heap: MinHeap, index: int) -> MinHeap:
    data = heap.data[:]
    size = len(data)
    while True:
        left_index = 2 * index + 1
        right_index = 2 * index + 2
        smallest = index

        if left_index < size and data[left_index] < data[smallest]:
            smallest = left_index
        if right_index < size and data[right_index] < data[smallest]:
            smallest = right_index
        if smallest == index:
            break
        data[index], data[smallest] = data[smallest], data[index]
        index = smallest
    return MinHeap(data)

def extract_min(heap: MinHeap) -> tuple[MinHeap, Node]:
    if not heap.data:
        raise IndexError("extract_min from empty heap")
    data = heap.data[:]
    min_node = data[0]
    if len(data) == 1:
        return MinHeap([]), min_node
    new_data = data[:-1]
    new_data[0] = data[-1]
    return heapify_down(MinHeap(new_data), 0), min_node

def count_frequency(s: str) -> dict[str, int]:
    frequency: dict[str, int] = {}
    for char in s:
        frequency[char] = frequency.get(char, 0) + 1
    return frequency

def create_priority_queue(frequency: dict[str, int]) -> MinHeap:
    heap = MinHeap([])
    for char in sorted(frequency):
        heap = insert(heap, Node(frequency[char], char))
    return heap

def build_tree_from_queue(priority_queue: MinHeap) -> Node | None:
    heap = priority_queue
    if not heap.data:
        return None
    while len(heap.data) > 1:
        heap, left = extract_min(heap)
        heap, right = extract_min(heap)
        # Set internal node char to the minimum child char to provide deterministic tie-breaking
        combined_char = min(left.char, right.char)
        combined = Node(left.freq + right.freq, combined_char, left, right)
        heap = insert(heap, combined)
    return heap.data[0]

def build_tree(priority_queue: MinHeap) -> Node | None:
    return build_tree_from_queue(priority_queue)

def generate_codes(node: Node | None, prefix: str = "", code: dict | None = None) -> dict:
    if code is None:
        code = {}
    if node is None:
        return code
    if node.left is None and node.right is None:
        code[node.char] = prefix or "0"
        return code
    if node.left is not None:
        generate_codes(node.left, prefix + "0", code)
    if node.right is not None:
        generate_codes(node.right, prefix + "1", code)
    return code

def encode(s: str, codes: dict) -> str:
    return "".join(codes[char] for char in s)

def decode(encoded_string: str, root: Node | None) -> str:
    if root is None:
        return ""
    if root.left is None and root.right is None:
        return root.char * len(encoded_string)
    decoded_chars: list[str] = []
    node = root
    for bit in encoded_string:
        if bit == "0":
            node = node.left
        else:
            node = node.right
        if node is None:
            raise ValueError("Encoded string does not match Huffman tree")
        if node.left is None and node.right is None:
            decoded_chars.append(node.char)
            node = root
    return "".join(decoded_chars)


def huffman_encoding(s: str):
    #Do Not Change this function
    frequency = count_frequency(s)
    pq = create_priority_queue(frequency)
    root = build_tree_from_queue(pq)
    codes = generate_codes(root)
    encoded_string = encode(s, codes)
    decoded_string = decode(encoded_string, root)
    return encoded_string, decoded_string, codes
