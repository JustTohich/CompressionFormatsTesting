import struct
from textwrap import wrap
from collections import Counter


def compressor(text, level=1):
    string_text = text.decode('utf-8')
    ba = bytearray()
    n = 6 + level
    for string in wrap(string_text, n):
        letters, probability = zip(*[(c[0], c[1] / len(string)) for c in Counter(string).items()])
        encoded = arithmetic_encoding(letters=letters, probability=probability, s=string)
        # decoded = arithmetic_decoding(letters=letters,
        #                               probability=probability, code=encoded,
        #                               n=len(string))
        # if string != decoded:
        #     return compressor(text, level+1)
        ba += bytearray(struct.pack("f", encoded))
    return ba


class Segment:
    left = 0
    right = 0


class SegmentDecode(Segment):
    character = None


def define_segments(letters, probability):
    l = 0
    segments = {letter: Segment() for letter in letters}

    for i in range(len(letters)):
        segments[letters[i]].left = l
        segments[letters[i]].right = l + probability[i]
        l = segments[letters[i]].right
    return segments


def arithmetic_encoding(letters, probability, s):
        segments = define_segments(letters, probability)
        left, right = float(0), float(1)

        for symb in s:
            right, left = left + (right - left) * segments[symb].right, left + (right - left) * segments[symb].left

        return (left + right)/2


def define_segments_decode(letters, probability):
    l = 0
    segments = [SegmentDecode() for _ in range(len(letters))]

    for i in range(len(letters)):
        segments[i].left = l
        segments[i].right = l + probability[i]
        segments[i].character = letters[i]
        l = segments[i].right

    return segments


def arithmetic_decoding(letters, probability, code, n):
    segments = define_segments_decode(letters, probability)
    s = ""

    for i in range(n):
        for seg in segments:
            if seg.left <= code < seg.right:
                s += seg.character
                code = (code - seg.left) / (seg.right - seg.left)
                break
    return s
