class Contact:
    '''Contact class to represent a contact with a name and number.'''

    def __init__(self, name: str, number: str):
        self.name = name
        self.number = number

    def __str__(self) -> str:
        return f"{self.name}: {self.number}"


class Node:
    '''Node class to represent a single entry in the hash table.'''

    def __init__(self, key: str, value: Contact):
        self.key = key
        self.value = value
        self.next = None


class HashTable:
    '''Hash table for contacts, using linked lists for collisions.'''

    def __init__(self, size: int):
        if size <= 0:
            raise ValueError("Hash table size must be positive")
        self.size = size
        self.data = [None] * size

    def hash_function(self, key: str) -> int:
        total = 0
        for char in key:
            total += ord(char)
        return total % self.size

    def insert(self, key: str, number: str) -> None:
        index = self.hash_function(key)
        current = self.data[index]

        if current is None:
            self.data[index] = Node(key, Contact(key, number))
            return

        while current:
            if current.key == key:
                current.value.number = number
                return
            if current.next is None:
                break
            current = current.next

        current.next = Node(key, Contact(key, number))

    def search(self, key: str):
        index = self.hash_function(key)
        current = self.data[index]
        while current:
            if current.key == key:
                return current.value
            current = current.next
        return None

    def print_table(self) -> None:
        for index in range(self.size):
            current = self.data[index]
            if current is None:
                print(f"Index {index}: Empty")
            else:
                contacts = []
                while current:
                    contacts.append(f"- {current.value}")
                    current = current.next
                print(f"Index {index}: {' '.join(contacts)}")


# Test your hash table implementation here.
if __name__ == "__main__":
    table = HashTable(10)
    print("Empty table:")
    table.print_table()

    table.insert("John", "909-876-1234")
    table.insert("Rebecca", "111-555-0002")
    print("\nAfter inserting contacts:")
    table.print_table()
    print("\nSearch result:", table.search("John"))

    # Amy and May have the same character sum, so they collide.
    table.insert("Amy", "111-222-3333")
    table.insert("May", "222-333-1111")
    assert table.hash_function("Amy") == table.hash_function("May")
    print("\nAfter collision test:")
    table.print_table()
    assert table.search("Amy").number == "111-222-3333"
    assert table.search("May").number == "222-333-1111"

    table.insert("Rebecca", "999-444-9999")
    print("\nAfter updating Rebecca:")
    table.print_table()
    assert table.search("Rebecca").number == "999-444-9999"

    print("\nMissing contact:", table.search("Chris"))
    assert table.search("Chris") is None
    print("All tests passed.")


# DESIGN MEMO
# A hash table is a good choice for this contact management system because it
# allows contacts to be found quickly by their names. Instead of searching
# through every contact in a list, the program uses a hash function to calculate
# the index where a name belongs. This makes searching, inserting, and updating
# contacts O(1) on average when the entries are spread out well. That speed is
# useful for a contact directory because users expect names and phone numbers
# to appear quickly, even when the directory contains hundreds of contacts.
#
# I handled collisions using separate chaining with linked lists. My hash
# function adds the Unicode values of the characters in a name using ord(),
# then uses the remainder after dividing by the table size to choose an index.
# Two different names can produce the same index, so each slot can hold a chain
# of Node objects. When inserting a contact, the program checks the chain for
# an existing name. If it finds one, it updates that contact's phone number.
# Otherwise, it adds a new node. Searching follows the same chain until it
# finds the name or reaches the end.
#
# An engineer might choose a hash table instead of a list when fast lookups
# and unique keys matter more than preserving order. A tree may be better when
# records need to stay sorted or support range searches. Hash tables do use
# extra space, and too many collisions can slow them down, but they fit this
# contact management task because quick name-based access is the main goal.
