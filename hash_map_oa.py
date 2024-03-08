# Name: Nolan Reichkitzer
# OSU Email: reichkin@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 3/14/2024
# Description:

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates the key/value pair in the hash map. If the given key already exists, its associated value is replaced
        with the new value. If the given key is not in the hash map, a new key/value pair is added.

        Args:
            key: string - the key associated to input value
            value: object - the value associated to the input key

        Returns:
            None - key/value pair will be updated or added to the hash map
        """
        # Check the load factor and resize the table if greater than or equal to 1
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        # Initialize new HashEntry, and determine the index for the given key
        hash_entry = HashEntry(key, value)
        hash_value = self._hash_function(key)
        index = hash_value % self._capacity
        probe = 1

        # If an object exists at index, check its key and tombstone property. Move to next index if needed
        while self._buckets[index]:

            # If the key at index matches the input key, replace it with the new hash entry
            if self._buckets[index].key == key and not self._buckets[index].is_tombstone:
                self._buckets[index] = hash_entry
                return

            # If the object at index is a tombstone, replace it with the new hash entry and update size
            if self._buckets[index].is_tombstone:
                self._buckets[index] = hash_entry
                self._size += 1
                return

            # Determine next index using quadratic probing scheme
            index = (index + probe ** 2) % self._capacity
            probe += 1

        # When we reach an open index, add in the new hash entry and update size
        self._buckets[index] = hash_entry
        self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the underlying dynamic array. All existing key/value pairs are rehashed and put into
        the array. The new capacity should be a prime number. If it is not prime, the capacity will be changed to the
        next prime number.

        Args:
            new_capacity: int - the proposed capacity for the underlying dynamic array.
                                This will change if the proposed capacity is not prime.

        Returns:
            None - underlying dynamic array will have a new capacity and existing key/value pairs will be rehashed.
        """
        # new_capacity must be greater than the current number of elements
        if new_capacity < self._size:
            return

        # new_capacity must be prime. If it is not prime, change it to the next prime number
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # Store the keys and values of each element in the table. Update self._capacity and clear the hash table
        da = self.get_keys_and_values()
        self._capacity = new_capacity
        self.clear()

        # Loop through the keys & values and add them to the new hash table
        for index in range(da.length()):
            self.put(da[index][0], da[index][1])

    def table_load(self) -> float:
        """
        Returns the current hash table load factor
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table
        """
        return self._capacity - self._size

    def get(self, key: str) -> object:
        """
        Returns the value associated with the given key if the key exists in the hash map.

        Args:
            key: str - the key associated with the value to be returned

        Returns:
            value: object - the value associated to the given key
            Returns None if the key does not exist in the hash map
        """
        # Determine the index for the given key
        hash_value = self._hash_function(key)
        index = hash_value % self._capacity
        probe = 1

        # If an object exists at index, compare its key to the input key
        while self._buckets[index]:

            # If the keys match, return the value of the object
            if self._buckets[index].key == key and not self._buckets[index].is_tombstone:
                return self._buckets[index].value

            # Determine next index using quadratic probing scheme
            index = (index + probe ** 2) % self._capacity
            probe += 1

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map, otherwise it returns False.

        Args:
            key: str - the key to be searched for in the hash map

        Returns:
            True - if the given key is found in the hash map
            False - if the given key is not found in the hash map
        """
        # Determine the index for the given key
        hash_value = self._hash_function(key)
        index = hash_value % self._capacity
        probe = 1

        # If an object exists at index, compare its key to the input key
        while self._buckets[index]:

            # If the keys match, return True
            if self._buckets[index].key == key and not self._buckets[index].is_tombstone:
                return True

            # Determine next index using quadratic probing scheme
            index = (index + probe ** 2) % self._capacity
            probe += 1

        # If key was not found, return False
        return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from the hash map.
        If the key is not in the hash map, the method does nothing.

        Args:
            key: str - the key to be searched for and removed from the hash map

        Returns:
            None - the key/value pair will be removed if found.
        """
        # Determine the index for the given key
        hash_value = self._hash_function(key)
        index = hash_value % self._capacity
        probe = 1

        # If an object exists at index, compare its key to the input key
        while self._buckets[index]:

            # If the keys match, remove it by setting its tombstone data member to True
            if self._buckets[index].key == key and not self._buckets[index].is_tombstone:
                self._buckets[index].is_tombstone = True
                self._size -= 1
                return

            # Determine next index using quadratic probing scheme
            index = (index + probe ** 2) % self._capacity
            probe += 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple of a key/value pair stored in the hash map.

        Returns:
            da - dynamic array containing tuples of the key/value pairs stored in the hash map
        """
        # Initialize a new Dynamic Array
        da = DynamicArray()

        # Loop through the elements in the hash map
        for element in self:

            # Store each elements key and value as a tuple in the dynamic array, skipping None objects and tombstones
            if element and not element.is_tombstone:
                da.append((element.key, element.value))

        return da

    def clear(self) -> None:
        """
        Clears the contents of the hash map. It does not change the underlying hash table capacity.
        """
        # To clear the contents of the hash map, set self._buckets to a new Dynamic Array, repopulate with None objects,
        # and update self._size
        self._buckets = DynamicArray()

        for _ in range(self._capacity):
            self._buckets.append(None)

        self._size = 0

    def __iter__(self):
        """
        Create iterator for loop
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Obtain next value and advance iterator
        """
        try:
            value = self._buckets[self._index]
        except DynamicArrayException:
            raise StopIteration

        self._index += 1
        return value


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)

    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
