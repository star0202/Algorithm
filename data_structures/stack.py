from __future__ import annotations

from typing import Generic, Iterable, Iterator, TypeVar

T = TypeVar("T")


class Stack(Generic[T], Iterable[T]):
    """
    Python implementation of a C++20 std::stack.
    """

    def __init__(self, iterable: Iterable[T] = ()) -> None:
        self._list: list[T] = list(iterable)

    def __iter__(self) -> Iterator[T]:
        return iter(self._list)

    def __len__(self) -> int:
        return len(self._list)

    def __str__(self) -> str:
        return f"Stack({self._list})"

    def __repr__(self) -> str:
        return repr(self._list)

    def __contains__(self, item: T) -> bool:
        return item in self._list

    def __getitem__(self, index: int) -> T:
        return self._list[index]

    def __setitem__(self, index: int, item: T) -> None:
        self._list[index] = item

    def __bool__(self) -> bool:
        return bool(self._list)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Stack):
            return self._list == other._list  # type: ignore

        return NotImplemented

    def top(self) -> T:
        return self._list[-1]

    def empty(self) -> bool:
        return len(self._list) == 0

    def size(self) -> int:
        return len(self._list)

    def push(self, item: T) -> None:
        self._list.append(item)

    def pop(self) -> None:
        self._list.pop()

    def emplace(self, *args: T) -> None:
        self._list += args

    def swap(self, other: Stack[T]) -> None:
        self._list, other._list = other._list, self._list


if __name__ == "__main__":
    s = Stack[int]()

    s.push(1)
    s.push(2)

    assert s.top() == 2
    assert s.size() == 2
    assert s.empty() is False
    assert str(s) == "Stack([1, 2])"

    s.pop()
    assert s.top() == 1
    assert s.size() == 1

    s.emplace(4, 5, 6)
    assert s.top() == 6
    assert s.size() == 4

    s.swap(Stack[int]())
    try:
        s.top()
        raise AssertionError("top() should raise when stack is empty")

    except IndexError:
        pass

    assert s.size() == 0
    assert s.empty() is True

    assert s == Stack[int]()
    assert s != Stack[int]([1, 2, 3])
