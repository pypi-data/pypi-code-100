from copy import copy
from typing import Generic, TypeVar, Union
# Local imports
from .exceptions import ListIsEmptyError

T = TypeVar("T")


class PolymorphicList(Generic[T]):
    """A generic class to represent a polymorphic list that stores objects of type T

    This class is the superclass of EmptyList and NonEmptyList.
    This class is not meant to be instantiated, so the __init__ method also raises errors.
    It throws errors for many method because the subclasses define these methods.
    Only methods that have the same implementation in NonEmptyList and EmptyList are implemented here.

    Args:
        Generic (T): The type of the objects that will be stored in the list.
    """
    def __init__(self):
        """Init function throws NotImplementedError to prevent instantiation of a List object.

        Raises:
            NotImplementedError: Prevent instantiation of a list object.
        """
        self.length = 0
        raise NotImplementedError()

    def __str__(self) -> str:
        """Creates a string for the object.

        Returns:
            str: string representation of the object.
        """
        raise NotImplementedError()

    def __eq__(self, other: object) -> bool:
        """Checks if the current object is equal to the given object.

        Args:
            other (object): the input object to compare to.

        Returns:
            bool: a bool indication whether the current object is equal to the given object
        """
        raise NotImplementedError()

    def __contains__(self, element: T) -> bool:
        """Overrides membership op to check whether an element exists in the list.

        Args:
            element (T): The element to look for.

        Returns:
            bool: a boolean indication of whether the element was found.
        """
        raise NotImplementedError()

    def __copy__(self) -> Union['NonEmptyList[T]', 'EmptyList[T]']:
        """Returns a copy of the list

        Returns:
            Union[NonEmptyList[T], EmptyList[T]]: A copy of the list.
        """
        raise NotImplementedError()

    def __add__(self,
                other: object) -> Union['NonEmptyList[T]', 'EmptyList[T]']:
        """Adds two Polymorphic lists together, independent of the input lists

        Args:
            other (PolymorphicList[T]): The list to add to current list.

        Raises:
            TypeError: TypeError raised if other is not a PolymorphicList

        Returns:
            Union[NonEmptyList[T], EmptyList[T]]: returns either an EmptyList[T] or a NonEmptyList[T] with elements of the two lists together
        """
        if (isinstance(other, NonEmptyList) or isinstance(other, EmptyList)):
            return copy(self)._add(copy(other))
        else:
            raise TypeError(
                "`other` must be an object with super type PolymorphicList")

    def _add(
        self, other: Union['NonEmptyList[T]', 'EmptyList[T]']
    ) -> Union['NonEmptyList[T]', 'EmptyList[T]']:
        """Helper method for __add__. Adds two lists together

        Args:
            other (Union[NonEmptyList[T], EmptyList[T]]): The list to add to current list.

        Returns:
            Union[NonEmptyList[T], EmptyList[T]]: Returns a NonEmptyList result of adding the two lists together.
        """
        raise NotImplementedError()

    def size(self) -> int:
        """Finds the size/length of the list

        Returns:
            int: The size/length of the list
        """
        return self.length

    def append(self, element: T) -> 'NonEmptyList[T]':
        """Appends an element to the beginning of the list

        Args:
            element (T): The element to be appended

        Returns:
            NonEmptyList: Object for the new list after append operation.
        """
        raise NotImplementedError()

    def prepend(self, element: T) -> 'NonEmptyList[T]':
        """Prepends an element to the beginning of the list

        Args:
            element (T): The element to be prepended

        Returns:
            NonEmptyList: Object for the new list after prepend operation.
        """
        raise NotImplementedError()

    def insert(self, element: T, index: int) -> 'NonEmptyList[T]':
        """Inserts a specified element at the specified index in the list

        Raises:
            IndexError: raised if the specified index is out of range

        Returns:
            NonEmptyList[T]: The new list after insert operation.
        """
        raise NotImplementedError()

    def remove_head(self) -> Union['NonEmptyList[T]', 'EmptyList[T]']:
        """Removes the first element from the list

        Raises:
            ListIsEmptyError: Raised if the list is empty, and no first element can be removed.

        Returns:
            Union[NonEmptyList[T], EmptyList[T]]: The new head of the list
        """
        raise NotImplementedError()

    def remove_tail(self) -> Union['NonEmptyList[T]', 'EmptyList[T]']:
        """Removes the last element from the list.

        Raises:
            ListIsEmptyError: Raised if the list is empty, and no first element can be removed.
        
        Returns:
            Union[NonEmptyList[T], EmptyList[T]]: The new head of the list
        """
        raise NotImplementedError()

    def remove_element(self,
                       element: T) -> Union['NonEmptyList[T]', 'EmptyList[T]']:
        """Removes the specified element from the list.

        Raises:
            ValueError: Raised if the input element is not in the list and can't be removed.
        
        Returns:
            Union[NonEmptyList[T], EmptyList[T]]: The new head of the list after the element is removed.
        """
        raise NotImplementedError()

    def remove_nth_occurrence(
            self, element: T,
            n: int) -> Union['NonEmptyList[T]', 'EmptyList[T]']:
        """Removes the nth occurrence of the specified element from the list.
        
        Args:
            element (T): The element to look for
            n (int): int for the nth occurrence to look for
        
        Raises:
            ValueError: raised if there are fewer than n occurrences of element in the list
        
        Returns:
            Union[NonEmptyList[T], EmptyList[T]]: The new head of the list after removing the element.
        """
        raise NotImplementedError()

    def remove_all_occurrences(
            self, element: T) -> Union['NonEmptyList[T]', 'EmptyList[T]']:
        """Removes all occurrences of a specified element from the list.
        
        Args:
            element (T): The element to look for
        
        Returns:
            Union[NonEmptyList[T], EmptyList[T]]: The new head of the list after removing the element.
        """
        raise NotImplementedError()

    def remove_index(self,
                     index: int) -> Union['NonEmptyList[T]', 'EmptyList[T]']:
        """Removes the element at a given index if the index is valid

        Raises:
            IndexError: Raised if the index is invalid
            
        Returns:
            Union[NonEmptyList[T], EmptyList[T]]: The new head of the resulting list after removing the element.
        """
        raise NotImplementedError()

    def get(self, index: int) -> 'NonEmptyList[T]':
        """Gets the NonEmptyList at the given index

        Args:
            index (int): An index in the array

        Raises:
            IndexError: raised for invalid indices

        Returns:
            NonEmptyList: Returns the NonEmptyList at the input index if exists.
        """
        raise NotImplementedError()

    def get_tail(self) -> 'NonEmptyList[T]':
        """Gets the last NonEmptyList node in the list.

        Raises:
            ListIsEmptyError: raised since an EmptyList has no last element.

        Returns:
            NonEmptyList: returns the last NonEmptyList object in the list
        """
        raise NotImplementedError()

    def get_nth_occurrence(self, element: T, n: int) -> 'NonEmptyList[T]':
        """Gets the NonEmptyList node with the nth occurrence of the element

        Args:
            element (T): The element to look for
            n (int): int for the nth occurrence to look for

        Raises:
            ValueError: raised if there are fewer than n occurrences of element in the list

        Returns:
            NonEmptyList[T]: The node with the nth occurrence of the element, if found in the list
        """
        raise NotImplementedError()

    def index_of(self, element: T) -> int:
        """Finds the index of the first occurence of a specified element in the polymorphic list

        Args:
            element (T): The type T element to look for.

        Raises:
            ValueError: raised if the element not in list

        Returns:
            int: The index of the first occurence of element if found
        """
        raise NotImplementedError()

    def count_occurrences(self, element: T) -> int:
        """Counts the number of occurrences of element in the list.

        Args:
            element (T): The element to look for

        Returns:
            int: The num occurrences of element found
        """
        raise NotImplementedError()


class NonEmptyList(PolymorphicList[T]):
    """Represents a NonEmptyList with a T type data, and a reference to the next node in the abstraction

    Args:
        PolymorphicList ([type]): Extends the PolymorphicList class to have a generic type T.
    """
    def __init__(self, data, next: Union['NonEmptyList[T]', 'EmptyList[T]']):
        """Initializes the state of the NonEmptyList.

        Args:
            data ([type]): The data stored in this node
            next (PolymorphicList): Reference to the next node
        """
        self.data: T = data
        self.next: Union['NonEmptyList[T]', 'EmptyList[T]'] = next
        self.length: int = self.next.length + 1

    def __str__(self) -> str:
        """Creates a string representation for the NonEmptyList

        Returns:
            str: The string representation of each object in the list separated with arrows.
        """
        # String for the curr data
        curr = str(self.data)
        # Recursively get the next element str
        rest = str(self.next)

        # Add a space if not last node
        curr += " -> " if rest != '' else ''
        return curr + rest

    def __eq__(self, other: object) -> bool:
        """Recursively checks if the entire NonEmptyList is equal to another input object.

        Args:
            other (object): The input object to compare to.

        Returns:
            bool: a bool indication whether the current object is equal to the given object
        """
        if (isinstance(other, NonEmptyList) and self.data == other.data
                and self.size() == other.size()):
            return self.next == other.next
        return False

    def __contains__(self, element: T) -> bool:
        """Overrides membership op to check whether an element exists in the list.

        Args:
            element (T): The element to look for.

        Returns:
            bool: a boolean indication of whether the element was found.
        """
        if self.data == element:
            return True
        return element in self.next

    def __copy__(self) -> 'NonEmptyList[T]':
        """Returns a copy of the NonEmptyList

        Returns:
            NonEmptyList: A copy of the NonEmptyList and its next references.
        """
        return NonEmptyList(self.data, copy(self.next))

    def _add(
        self, other: Union['NonEmptyList[T]', 'EmptyList[T]']
    ) -> Union['NonEmptyList[T]', 'EmptyList[T]']:
        """Helper method for __add__. Adds two lists together

        Args:
            other (Union[NonEmptyList[T], EmptyList[T]]): The list to add to current list.

        Returns:
            Union['NonEmptyList[T]', 'EmptyList[T]']: Returns a NonEmptyList result of adding the two lists together.
        """
        self.next = self.next + other
        self.length += other.length
        return self

    def append(self, element: T) -> 'NonEmptyList[T]':
        """Appends an element to the beginning of the list

        Args:
            element (T): The element to be appended

        Returns:
            NonEmptyList: Object for the new list after append operation.
        """
        self.next = self.next.append(element)
        self.length += 1
        return self

    def prepend(self, element: T) -> 'NonEmptyList[T]':
        """Prepends an element to the beginning of the list

        Args:
            element (T): The element to be prepended

        Returns:
            NonEmptyList: Object for the new list after prepend operation.
        """
        return NonEmptyList(element, self)

    def insert(self, element: T, index: int) -> 'NonEmptyList[T]':
        """Inserts a specified element at the specified index in the list

        Raises:
            IndexError: raised if the specified index is out of range

        Returns:
            NonEmptyList[T]: The new list after insert operation.
        """
        if index > self.size() or index < 0:
            raise IndexError("Index out of range")
        elif index == 0:
            # Insert at head
            return NonEmptyList(element, self)
        elif index == 1:
            # Insert at some other index
            self.next = NonEmptyList(element, self.next)
            self.length += 1
        else:
            # Tell the next node to handle the insert
            self.next.insert(element, index - 1)
            self.length += 1
        return self

    def remove_head(self) -> Union['NonEmptyList[T]', 'EmptyList[T]']:
        """Removes the first element from the list

        Raises:
            ListIsEmptyError: Raised if the list is empty, and no first element can be removed.

        Returns:
            Union[NonEmptyList[T], EmptyList[T]]: The new head of the list
        """
        return self.next

    def remove_tail(self) -> Union['NonEmptyList[T]', 'EmptyList[T]']:
        """Removes the last element from the list.

        Raises:
            ListIsEmptyError: Raised if the list is empty, and no first element can be removed.
        
        Returns:
            Union[NonEmptyList[T], EmptyList[T]]: The new head of the list
        """
        try:
            self.next = self.next.remove_tail()
            self.length -= 1
            return self
        except ListIsEmptyError:
            return EmptyList()

    def remove_element(self,
                       element: T) -> Union['NonEmptyList[T]', 'EmptyList[T]']:
        """Removes the specified element from the list.

        Raises:
            ValueError: Raised if the input element is not in the list and can't be removed.
        
        Returns:
            Union[NonEmptyList[T], EmptyList[T]]: The new head of the list after the element is removed.
        """
        if self.data == element:
            return self.next
        else:
            self.next = self.next.remove_element(element)
            self.length -= 1
            return self

    def remove_nth_occurrence(
            self, element: T,
            n: int) -> Union['NonEmptyList[T]', 'EmptyList[T]']:
        """Removes the nth occurrence of a specified element from the list.
        
        Args:
            element (T): The element to look for
            n (int): int for the nth occurrence to look for
        
        Raises:
            ValueError: raised if there are fewer than n occurrences of element in the list
        
        Returns:
            Union[NonEmptyList[T], EmptyList[T]]: The new head of the list after removing the element.
        """
        if self.data == element:
            if n == 1:
                return self.next
            else:
                self.next = self.next.remove_nth_occurrence(element, n - 1)
        else:
            self.next = self.next.remove_nth_occurrence(element, n)

        self.length -= 1
        return self

    def remove_all_occurrences(
            self, element: T) -> Union['NonEmptyList[T]', 'EmptyList[T]']:
        """Removes all occurrences of a specified element from the list.
        
        Args:
            element (T): The element to look for
        
        Returns:
            Union[NonEmptyList[T], EmptyList[T]]: The new head of the list after removing the element.
        """
        if (self.data == element):
            return self.next.remove_all_occurrences(element)
        else:
            self.next = self.next.remove_all_occurrences(element)
            return self

    def remove_index(self,
                     index: int) -> Union['NonEmptyList[T]', 'EmptyList[T]']:
        """Removes the element at a given index if the index is valid

        Raises:
            IndexError: Raised if the index is invalid
            
        Returns:
            Union[NonEmptyList[T], EmptyList[T]]: The new head of the resulting list after removing the element.
        """
        if index == 0:
            return self.next
        else:
            self.next = self.next.remove_index(index - 1)
            self.length -= 1
            return self

    def get(self, index: int) -> 'NonEmptyList[T]':
        """Gets the NonEmptyList at the given index

        Args:
            index (int): An index in the array

        Raises:
            IndexError: raised for invalid indices

        Returns:
            NonEmptyList: Returns the NonEmptyList at the input index if exists.
        """
        if index > self.size() - 1 or index < 0:
            raise IndexError("Index out of range")
        elif index == 0:
            return self
        else:
            return self.next.get(index - 1)

    def get_tail(self) -> 'NonEmptyList[T]':
        """Gets the last NonEmptyList element in the list.

        Returns:
            NonEmptyList: returns the last NonEmptyList object in the list
        """
        try:
            return self.next.get_tail()
        except ListIsEmptyError:
            return self

    def get_nth_occurrence(self, element: T, n: int) -> 'NonEmptyList[T]':
        """Gets the nth occurrence of the element

        Args:
            element (T): The element to look for
            n (int): int for the nth occurrence to look for

        Raises:
            ValueError: raised if there are fewer than n occurrences of element in the list

        Returns:
            NonEmptyList[T]: The node with the nth occurrence of the element, if found in the list
        """
        if self.data == element:
            if n == 1:
                return self
            else:
                return self.next.get_nth_occurrence(element, n - 1)
        else:
            return self.next.get_nth_occurrence(element, n)

    def index_of(self, element: T) -> int:
        """Finds the index of the first occurence of element param in the polymorphic list

        Args:
            element (T): The type T element to look for.

        Raises:
            ValueError: raised if the element not in list

        Returns:
            int: The index of the first occurence of element if found
        """
        if (self.data != element):
            return 1 + self.next.index_of(element)
        return 0

    def count_occurrences(self, element: T) -> int:
        """Counts the number of occurrences of element in the list.

        Args:
            element (T): The element to look for

        Returns:
            int: The num occurrences of element found
        """
        return (self.data == element) + self.next.count_occurrences(element)


class EmptyList(PolymorphicList[T]):
    """Represents a EmptyList, the last node in the abstraction, which has no data or next pointer

    Args:
        PolymorphicList ([type]): Extends the PolymorphicList class to have a generic type T.
    """
    def __init__(self):
        """Initializes the state of the EmptyList.
        """
        self.length: int = 0
        pass

    def __str__(self) -> str:
        """Creates a string representation for the EmptyList

        Returns:
            str: an empty string, since this is an EmptyList object
        """
        return ''

    def __eq__(self, other: object) -> bool:
        """Checks if this EmptyList is equal to another input object.

        Args:
            other (object): The input object to compare to.

        Returns:
            bool: a bool indication whether the current object is equal to the given object
        """
        # TODO: Check if there is a way to check that other isinstance with EmptyList[T]
        return isinstance(other, EmptyList)

    def __contains__(self, element: T) -> bool:
        """Overrides membership op to check whether an element exists in the list.

        Args:
            element (T): The element to look for.

        Returns:
            bool: a boolean indication of whether the element was found.
        """
        return False

    def __copy__(self) -> 'EmptyList[T]':
        """Returns a copy of the list object

        Returns:
            EmptyList: A copy of the EmptyList object.
        """
        return EmptyList()

    def _add(
        self, other: Union['NonEmptyList[T]', 'EmptyList[T]']
    ) -> Union['NonEmptyList[T]', 'EmptyList[T]']:
        """Helper method for __add__. Adds two lists together

        Args:
            other (Union[NonEmptyList[T], EmptyList[T]]): The list to add to current list.

        Returns:
            Union[NonEmptyList[T], EmptyList[T]]: Returns a NonEmptyList result of adding the two lists together.
        """
        return other

    def append(self, element: T) -> NonEmptyList[T]:
        """Appends an element to the beginning of the list

        Args:
            element (T): The element to be appended

        Returns:
            NonEmptyList: Object for the new list after append operation.
        """
        return NonEmptyList(element, self)

    def prepend(self, element: T) -> NonEmptyList[T]:
        """Prepends an element to the beginning of the list

        Args:
            element (T): The element to be prepended

        Returns:
            NonEmptyList: Object for the new list after prepend operation.
        """
        return NonEmptyList(element, self)

    def insert(self, element: T, index: int) -> NonEmptyList[T]:
        """Inserts a specified element at the specified index in the list

        Raises:
            IndexError: raised if the specified index is out of range

        Returns:
            NonEmptyList[T]: The new list after insert operation.
        """
        raise IndexError("Index out of range")

    def remove_head(self) -> Union['NonEmptyList[T]', 'EmptyList[T]']:
        """Removes the first element from the list

        Raises:
            ListIsEmptyError: Raised if the list is empty, and no first element can be removed.

        Returns:
            Union[NonEmptyList[T], EmptyList[T]]: The new head of the list
        """
        raise ListIsEmptyError()

    def remove_tail(self) -> Union['NonEmptyList[T]', 'EmptyList[T]']:
        """Removes the last element from the list.

        Raises:
            ListIsEmptyError: Raised if the list is empty, and no first element can be removed.
        
        Returns:
            Union[NonEmptyList[T], EmptyList[T]]: The new head of the list
        """
        raise ListIsEmptyError()

    def remove_element(self,
                       element: T) -> Union['NonEmptyList[T]', 'EmptyList[T]']:
        """Removes the first occurrance of a specified element from the list.

        Raises:
            ValueError: Raised if the input element is not in the list and can't be removed.
        
        Returns:
            Union[NonEmptyList[T], EmptyList[T]]: The new head of the list after the element is removed.
        """
        raise ValueError("`element` does not exist in the list")

    def remove_nth_occurrence(
            self, element: T,
            n: int) -> Union['NonEmptyList[T]', 'EmptyList[T]']:
        """Removes the nth occurrence of a specified element from the list.

        Args:
            element (T): The element to look for
            n (int): int for the nth occurrence to look for
        
        Raises:
            ValueError: raised if there are fewer than n occurrences of element in the list
        
        Returns:
            Union[NonEmptyList[T], EmptyList[T]]: The new head of the list after removing the element.
        """
        raise ValueError(
            "There are fewer than `n` occurrences `element` in the list")

    def remove_all_occurrences(
            self, element: T) -> Union['NonEmptyList[T]', 'EmptyList[T]']:
        """Removes all occurrences of a specified element from the list.
        
        Args:
            element (T): The element to look for
        
        Returns:
            Union[NonEmptyList[T], EmptyList[T]]: The new head of the list after removing the element.
        """
        return self

    def remove_index(self,
                     index: int) -> Union['NonEmptyList[T]', 'EmptyList[T]']:
        """Removes the element at a given index if the index is valid

        Raises:
            IndexError: Raised if the index is invalid

        Returns:
            Union[NonEmptyList[T], EmptyList[T]]: The new head of the resulting list after removing the element.
        """
        raise IndexError("Index out of range")

    def get(self, index: int) -> NonEmptyList[T]:
        """Gets the NonEmptyList at the given index

        Args:
            index (int): An index in the array

        Raises:
            IndexError: raised for invalid indices

        Returns:
            NonEmptyList: Returns the NonEmptyList at the input index if exists.
        """
        raise IndexError("Index out of range")

    def get_tail(self) -> NonEmptyList[T]:
        """Gets the last NonEmptyList element in the list. Raises ListIsEmptyError if this is an EmptyList

        Raises:
            ListIsEmptyError: raised since an EmptyList has no last element.
        """
        raise ListIsEmptyError("The list is empty.")

    def get_nth_occurrence(self, element: T, n: int) -> NonEmptyList[T]:
        """Gets the nth occurrence of the element

        Args:
            element (T): The element to look for
            n (int): int for the nth occurrence to look for

        Raises:
            ValueError: raised if there are fewer than n occurrences of element in the list

        Returns:
            NonEmptyList[T]: The node with the nth occurrence of the element, if found in the list
        """
        raise ValueError(
            "There are fewer than `n` occurrences `element` in the list")

    def index_of(self, element: T) -> int:
        """Finds the index of the first occurence of element param in the polymorphic list

        Args:
            element (T): The type T element to look for.

        Raises:
            ValueError: raised if the element not in list

        Returns:
            int: The index of the first occurence of element if found
        """
        raise ValueError("`element` does not exist in the list")

    def count_occurrences(self, element: T) -> int:
        """Counts the number of occurrences of element in the list.

        Args:
            element (T): The element to look for

        Returns:
            int: The num occurrences of element found
        """
        return 0