import unittest
from proj3 import count_frequency, create_priority_queue, insert, extract_min, generate_codes, encode, decode, build_tree_from_queue, huffman_encoding, MinHeap, Node

class TestStudentHuffman(unittest.TestCase):
    def test_count_frequency_empty(self):
        self.assertEqual(count_frequency(""), {})

    def test_count_frequency_repeated(self):
        self.assertEqual(count_frequency("aaabbc"), {"a": 3, "b": 2, "c": 1})

    def test_heap_insert_and_extract(self):
        heap = MinHeap([])
        heap = insert(heap, Node(5, "z"))
        heap = insert(heap, Node(1, "a"))
        heap = insert(heap, Node(3, "m"))
        new_heap, min_node = extract_min(heap)
        self.assertEqual(min_node.char, "a")
        self.assertEqual(min_node.freq, 1)
        self.assertEqual(len(new_heap.data), 2)
        self.assertEqual(new_heap.data[0].char, "m")

    def test_build_tree_single_character(self):
        pq = create_priority_queue({"X": 4})
        root = build_tree_from_queue(pq)
        self.assertIsNotNone(root)
        self.assertIsNone(root.left)
        self.assertIsNone(root.right)
        codes = generate_codes(root)
        self.assertEqual(codes, {"X": "0"})
        self.assertEqual(encode("XXXX", codes), "0000")
        self.assertEqual(decode("0000", root), "XXXX")

    def test_encode_decode_empty(self):
        encoded, decoded, codes = huffman_encoding("")
        self.assertEqual(encoded, "")
        self.assertEqual(decoded, "")
        self.assertEqual(codes, {})

    def test_generate_codes_tree_shape(self):
        frequency = {"a": 2, "b": 1, "c": 1}
        pq = create_priority_queue(frequency)
        root = build_tree_from_queue(pq)
        codes = generate_codes(root)
        self.assertEqual(set(codes.keys()), {"a", "b", "c"})
        self.assertGreaterEqual(len(codes["a"]), 1)
        self.assertGreaterEqual(len(codes["b"]), 1)
        self.assertGreaterEqual(len(codes["c"]), 1)

if __name__ == "__main__":
    unittest.main()
