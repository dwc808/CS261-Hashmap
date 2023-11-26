# Name:
# OSU Email:
# Course: CS261 - Data Structures
# Assignment:
# Due Date:
# Description:


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        Puts the key-value pair into the hashmap. If the key already exists, the value will be
        overridden with the new value. put() will call resize_table() as needed.

        :param key:     the key to be placed in the hash map
        :param value:   the corresponding value that the key refers to

        :return:        None, this method will put the key-value pair into the hashmap
        """

        if self.table_load() >= 1.0:
            self.resize_table(self._capacity*2)

        #find the bucket of the key
        hash = self._hash_function(key)
        index = hash % self._capacity

        #if bucket empty
        if self._buckets.get_at_index(index)._head == None:
            self._buckets.get_at_index(index).insert(key, value)
            self._size += 1
            return

        #search the bucket for same key
        for item in self._buckets.get_at_index(index):
            if item.key == key:
                item.value = value
                return

        self._buckets.get_at_index(index).insert(key, value)
        self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the table for the hashmap. If the new capacity is not prime it will be changed
        to the next greatest prime number. Data is re-mapped into hashmap based on new capacity.

        :param new_capacity:    the intended size of the hashmap after the resize

        :return None:           None, the table is resized
        """

        #do nothing if new capacity is less than 1
        if new_capacity < 1:
            return None

        #store old capacity
        old_cap = self._capacity

        #if new capacity is prime, set it
        if self._is_prime(new_capacity):
            self._capacity = new_capacity

        #otherwise move to next greatest prime and set
        else:
            new_capacity = self._next_prime(new_capacity)
            self._capacity = new_capacity

        #transfer items from old DA into new one
        new_da = DynamicArray()
        old_da = self._buckets
        for _ in range(self._capacity):
            new_da.append(LinkedList())

        #update hashmap buckets to be new da
        self._buckets = new_da
        self._size = 0

        for i in range(old_cap):
            for object in old_da.get_at_index(i):
                self.put(object.key, object.value)


    def table_load(self) -> float:
        """
        Returns a float with the table's current load factor.

        :return:    the load factor of the table as a float
        """

        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        Returns an integer with the number of empty buckets in the hash table.

        :return:    an int, the number of empty bucktes in the hash table

        """

        count = 0

        #for each bucket that is empty, increment the count
        for i in range(self._capacity):
            if self._buckets.get_at_index(i)._head == None:
                count += 1

        return count

    def get(self, key: str) -> object:
        """
        Takes a key as a parameter and returns the value associated with the key.

        :param key:     the key (a string) for the key-value pair

        :return:        the value associated with the key
        """

        # find the bucket of the key
        hash = self._hash_function(key)
        index = hash % self._capacity

        # search the bucket for same key
        for item in self._buckets.get_at_index(index):
            if item.key == key:
                return item.value

        return

    def contains_key(self, key: str) -> bool:
        """
        Takes a key as a parameter and returns True if the key is found in the hash table,
        and False if it is not. It will return False if the table is empty.

        :param key:     a string, the key to be searched for in the hash table

        :return:        True if the key is found, False if not
        """

        if self._size == 0:
            return False

        # find the bucket of the key
        hash = self._hash_function(key)
        index = hash % self._capacity

        # search the bucket for same key
        for item in self._buckets.get_at_index(index):
            if item.key == key:
                return True

        return False


    def remove(self, key: str) -> None:
        """
        Searches the hash table for the key, and removes the key-value pair if it exists. If
        it is not found, the method does nothing.

        :param key:     a string, the key of the key-value pair to be removed

        :return:        None, the key-value pair is removed if found
        """

        # find the bucket of the key
        hash = self._hash_function(key)
        index = hash % self._capacity

        #set pointer for last and current
        last = None
        current = self._buckets.get_at_index(index)._head

        # search the bucket for same key
        for item in self._buckets.get_at_index(index):
            if item.key == key:
                #if removing the head
                if current == self._buckets.get_at_index(index)._head:
                    self._buckets.get_at_index(index)._head = current.next
                    self._size -= 1
                    return
                #removing any other items
                else:
                    last.next = current.next
                    self._size -= 1
                    return
                return

            #update pointers
            last = current
            current = current.next

        return


    def get_keys_and_values(self) -> DynamicArray:
        """
        This method returns a new dynamic array with all of the key-value pairs in the hash table.
        The key-value pairs are stored as tuples.

        :return:        A dynamic array with tuples containing every key-value pair in the hash table
        """

        keys_and_values = DynamicArray()

        #iterate through buckets, storing any key-value pairs found
        for i in range(self._capacity):

            for pair in self._buckets.get_at_index(i):
                keys_and_values.append((pair.key, pair.value))

        return keys_and_values

    def clear(self) -> None:
        """
        This method will empty the hash map, but will not alter its current capacity. All
        key-value pairs stored in the buckets will be removed and size will be reset to 0.

        :return:    None - the hash map is emptied, retaining its capacity
        """

        #iterate through buckets, clearing any that are not empty
        for i in range(self._capacity):
            if self._buckets.get_at_index(i)._head != None:
                self._buckets.set_at_index(i, LinkedList())

        self._size = 0


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    This function will find the mode of a dynamic array, and return a tuple with two items:
    a new dynamic array containing the mode, and an integer with the count for the mode value(s).
    It makes use of a hashmap to store the count of items encountered in the dynamic array.

    :param da:      the dynamic array to find the mode of

    :return:        a tuple containing a dynamic array of the mode, and an integer with their count
    """

    map = HashMap()
    highest_instance = 0
    count = 0

    #iterate over the dynamic array
    for i in range(da.length()):
        #if already in hashmap, increment value
        if map.contains_key(da.get_at_index(i)):
            value = map.get(da.get_at_index(i))
            map.put(da.get_at_index(i), value+1)
            count = map.get(da.get_at_index(i))

            #if the count is higher than current mode, add item to new da
            if count > highest_instance:
                highest_instance = count
                mode_da = DynamicArray()
                mode_da.append(da.get_at_index(i))

            #if count equal to current mode, append item to da
            elif count == highest_instance:
                mode_da.append(da.get_at_index(i))

        #add new item to hashmap
        else:
            map.put(da.get_at_index(i), 1)
            count = map.get(da.get_at_index(i))

            #for first item added
            if highest_instance == 0:
                highest_instance = count
                mode_da = DynamicArray()
                mode_da.append(da.get_at_index(i))
            #until mode greater than 1
            elif highest_instance == 1:
                mode_da.append(da.get_at_index(i))

    return mode_da, highest_instance

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
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

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
    m = HashMap(53, hash_function_1)
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

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
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

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
