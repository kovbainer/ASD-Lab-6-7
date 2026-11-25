"""
Реалізуйте каталог деякої бібліотеки.
Бібліотека може містити кілька книг одного автора.
"""

EMPTY = None
DELETED = ("<deleted>",)


class HashTable:

    def __init__(self, capacity=16):
        self.capacity = capacity
        self.size = 0
        self.used = 0
        self.keys = [EMPTY] * capacity
        self.values = [EMPTY] * capacity

    def _hash(self, key):
        h = 0
        for ch in key:
            h = (h * 31 + ord(ch)) % 1000000007
        return h % self.capacity

    def _find_slot(self, key):
        i = self._hash(key)
        first_deleted = -1
        while True:
            k = self.keys[i]
            if k is EMPTY:
                return i if first_deleted == -1 else first_deleted, False
            if k is DELETED:
                if first_deleted == -1:
                    first_deleted = i
            elif k == key:
                return i, True
            i = (i + 1) % self.capacity

    def _rehash(self, new_capacity):
        old_keys, old_values = self.keys, self.values
        self.capacity = new_capacity
        self.keys = [EMPTY] * new_capacity
        self.values = [EMPTY] * new_capacity
        self.size = 0
        self.used = 0
        for k, v in zip(old_keys, old_values):
            if k is not EMPTY and k is not DELETED:
                self.put(k, v)

    def put(self, key, value):
        if (self.used + 1) * 2 > self.capacity:
            self._rehash(self.capacity * 2)
        i, found = self._find_slot(key)
        if not found:
            if self.keys[i] is EMPTY:
                self.used += 1
            self.size += 1
            self.keys[i] = key
        self.values[i] = value

    def get(self, key):
        i, found = self._find_slot(key)
        return self.values[i] if found else None

    def remove(self, key):
        i, found = self._find_slot(key)
        if found:
            self.keys[i] = DELETED
            self.values[i] = EMPTY
            self.size -= 1


def _lower_bound(lst, x):
    lo, hi = 0, len(lst)
    while lo < hi:
        mid = (lo + hi) // 2
        if lst[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return lo


catalog = None


def init():
    """ Викликається 1 раз на початку виконання програми. """
    global catalog
    catalog = HashTable()


def addBook(author, title):
    """ Додає книгу до бібліотеки.
    :param author: Автор книги
    :param title: Назва книги
    """
    books = catalog.get(author)
    if books is None:
        catalog.put(author, [title])
        return
    i = _lower_bound(books, title)
    if i == len(books) or books[i] != title:
        books.insert(i, title)


def find(author, title):
    """ Перевірає чи міститься задана книга у бібліотеці.
    :param author: Автор
    :param title: Назва книги
    :return: True, якщо книга міститься у бібліотеці та False у іншому разі.
    """
    books = catalog.get(author)
    if books is None:
        return False
    i = _lower_bound(books, title)
    return i < len(books) and books[i] == title


def delete(author, title):
    """ Видаляє книгу з бібліотеки.
    :param author: Автор
    :param title: Назва книги
    """
    books = catalog.get(author)
    if books is None:
        return
    i = _lower_bound(books, title)
    if i < len(books) and books[i] == title:
        books.pop(i)
        if not books:
            catalog.remove(author)


def findByAuthor(author):
    """ Повертає список книг заданого автора.
    Якщо бібліотека не міститься книг заданого автора, то підпрограма повертає порожній список.
    :param author: Автор
    :return: Список книг заданого автора у алфавітному порядку.
    """
    books = catalog.get(author)
    return list(books) if books is not None else []
