# Name: Darren Choate
# OSU Email: choated@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 - HashMap OA
# Due Date: 12/7/2023
# Description: This is a hashmap implementation that uses open addressing to handle collisions. It
# employs quadratic probing. It uses a Dynamic Array as the underlying data structure, and uses a
# simply HashEntry class to store key-value pairs. It has a maximum load-size of .5.

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
        Adds an item to the hashmap. Utilizes a hash function to compute the index,
        and attempts to place the object at that index. If the index is full, uses
        quadratic probing to find an empty bucket. Put will call resize_table if
        the load factor of the hashtable is .5 or greater.

        :param key:     the key of the object to be added
        :param value:   the value of the object to be added

        :return:        None, the object is added to the hashmap
        """

        #double capacity if load factor is .5 or greater
        if self.table_load() >= .5:
            self.resize_table(self._capacity*2)

        #find index of key
        hash = self._hash_function(key)
        index = hash % self._capacity

        #if bucket empty, add key-value pair
        if self._buckets.get_at_index(index) == None:
            self._buckets.set_at_index(index, HashEntry(key, value))
            self._size += 1
            return

        #if bucket is full but it's a tombstone
        if self._buckets.get_at_index(index).is_tombstone == True:
            self._buckets.set_at_index(index, HashEntry(key, value))
            self._size += 1
            return

        #if bucket is full, but key is same, update value
        if self._buckets.get_at_index(index).key == key:
            self._buckets.get_at_index(index).value = value
            return

        #otherwise, use quadratic probing to find spot
        j = 1
        initial_index = index
        while self._buckets.get_at_index(index) != None:
            #replace a tombstone if hit
            if self._buckets.get_at_index(index).is_tombstone == True:
                self._buckets.set_at_index(index, HashEntry(key, value))
                self._size += 1
                return
            # if bucket is full, but key is same, update value
            if self._buckets.get_at_index(index).key == key:
                self._buckets.get_at_index(index).value = value
                return
            #use quadratic probing to check new index
            index = (initial_index + j**2) % self._capacity
            j += 1

        #empty bucket found, add key-value pair
        self._buckets.set_at_index(index, HashEntry(key, value))
        self._size += 1
        return

    def resize_table(self, new_capacity: int) -> None:
        """
        This method will resize the table for the hashmap. It will always be called by put
        if the table load is greater than .5, but can be called directly. It should be passed
        the desired new capacity as a parameter; the method will ensure that the new capacity is
        prime. This method will call put to rehash all the existing items in the table.

        :param new_capacity:    the desired capacity for the hashmap after resizing

        :return:                None, the table is resized and elements are re-addressed.
        """

        #do nothing if new_capacity is less than current number of elements in the has map
        if new_capacity < self._size:
            return

        #store old_capacity
        old_cap = self._capacity

        #if new_capacity is prime
        if self._is_prime(new_capacity):
            self._capacity = new_capacity

        #if not, find next prime
        else:
            self._capacity = self._next_prime(new_capacity)

        new_da = DynamicArray()
        old_da = self._buckets

        #initialize new_da and replace buckets with it
        for i in range(self._capacity):
            new_da.append(None)
        self._buckets = new_da
        self._size = 0

        #iterate over old buckets, re-hashing each key-value pair into new buckets
        for i in range(old_cap):
            if old_da.get_at_index(i) != None:
                #don't transfer tombstones
                if old_da.get_at_index(i).is_tombstone != True:
                    self.put(old_da.get_at_index(i).key, old_da.get_at_index(i).value)

    def table_load(self) -> float:
        """
        Returns the current table load.

        :return:        the current table load, as a float
        """

        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets currently in the HashMap.

        :return:        an integer, the amount of empty buckets
        """

        return self._capacity - self._size

    def get(self, key: str) -> object:
        """
        Return the value associated with the given key. If the key is not found, returns None.

        :param key:     the key to search for

        :return:        the value associated with the key provided
        """

        if self._size == 0:
            return None

        # find index of key
        hash = self._hash_function(key)
        index = hash % self._capacity

        j = 1
        initial_index = index

        #search for the key, using quadratic probing if index is full
        for i in range(self._capacity):
            if self._buckets.get_at_index(index) == None:
                return None
            if self._buckets.get_at_index(index).key == key:
                return self._buckets.get_at_index(index).value

            index = (initial_index + j ** 2) % self._capacity
            j += 1


    def contains_key(self, key: str) -> bool:
        """
        Returns true if the key provided exists in the HashMap, otherwise returns False.

        :param key:     the key to search for

        :return:        True if key is found, False otherwise
        """

        if self._size == 0:
            return False

        # find index of key
        hash = self._hash_function(key)
        index = hash % self._capacity

        j = 1
        initial_index = index

        for i in range(self._capacity):
            if self._buckets.get_at_index(index) == None:
                return False
            if self._buckets.get_at_index(index).key == key:
                return True

            index = (initial_index + j ** 2) % self._capacity
            j += 1


    def remove(self, key: str) -> None:
        """
        This method removes an key-value pair from the Hashmap. When a pair is removed, it is
        left as a tombstone. If the key to be removed is not found, remove will do nothing.

        :param key:     the key to remove from the HashMap

        :return:        None, either the key is removed or it is not found
        """

        # find index of key
        hash = self._hash_function(key)
        index = hash % self._capacity

        j = 1
        initial_index = index

        while self._buckets.get_at_index(index) != None:
            if self._buckets.get_at_index(index).key == key and self._buckets.get_at_index(index).is_tombstone == False:
                self._buckets.get_at_index(index).is_tombstone = True
                self._size -= 1
                return
            index = (initial_index + j**2) % self._capacity
            j += 1

        return

    def get_keys_and_values(self) -> DynamicArray:
        """
        This method returns an array with every key-value pair in the HashMap. The key-value
        pairs are stored in the array as tuples.

        :return:        new DynamicArray with all key-value pairs in the HashMap
        """

        keys_and_values = DynamicArray()

        for i in range(self._capacity):

            if self._buckets.get_at_index(i) != None and self._buckets.get_at_index(i).is_tombstone == False:
                keys_and_values.append((self._buckets.get_at_index(i).key, self._buckets.get_at_index(i).value))

        return keys_and_values

    def clear(self) -> None:
        """
        This method empties the HashMap entirely, without altering its current capacity.

        :return:        None, the HashMap is emptied
        """

        for i in range(self._capacity):
            self._buckets.set_at_index(i, None)

        self._size = 0

    def __iter__(self):
        """
        Initialize the iterator for the HashMap.
        """

        self._index = 0

        return self

    def __next__(self):
        """
        Iterate to the next full bucket in the HashMap.
        """

        try:
            value = self._buckets[self._index]
        except DynamicArrayException:
            raise StopIteration

        if value != None and value.is_tombstone == False:
            self._index = self._index + 1
            return value
        else:
            self._index = self._index + 1
            return self.__next__()


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
