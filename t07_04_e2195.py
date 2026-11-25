import sys


class HashTable:

    def __init__(self, capacity):
        self.capacity = capacity
        self.keys = [None] * capacity
        self.used = [False] * capacity
        self.size = 0

    def _hash(self, key):
        h = 0
        for ch in key:
            h = (h * 131 + ord(ch)) % 1000000007
        return h % self.capacity

    def _slot(self, key):
        i = self._hash(key)
        while self.keys[i] is not None and self.keys[i] != key:
            i = (i + 1) % self.capacity
        return i

    def add(self, key):
        i = self._slot(key)
        if self.keys[i] is None:
            self.keys[i] = key
            self.size += 1

    def mark(self, key):
        i = self._slot(key)
        if self.keys[i] is None:
            return False
        self.used[i] = True
        return True

    def all_used(self):
        for i in range(self.capacity):
            if self.keys[i] is not None and not self.used[i]:
                return False
        return True


def split_words(text):
    words = []
    cur = []
    for ch in text:
        if 'a' <= ch <= 'z' or 'A' <= ch <= 'Z':
            cur.append(ch.lower())
        elif cur:
            words.append("".join(cur))
            cur = []
    if cur:
        words.append("".join(cur))
    return words


def main():
    lines = sys.stdin.read().split("\n")
    n, m = map(int, lines[0].split())
    table = HashTable(4099)
    for i in range(1, n + 1):
        table.add(lines[i].strip().lower())
    text = "\n".join(lines[n + 1:])
    unknown = False
    for w in split_words(text):
        if not table.mark(w):
            unknown = True
    if unknown:
        print("Some words from the text are unknown.")
    elif not table.all_used():
        print("The usage of the vocabulary is not perfect.")
    else:
        print("Everything is going to be OK.")


main()
