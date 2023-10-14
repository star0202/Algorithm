from __future__ import annotations

from typing import Generic, Iterable, Iterator, TypeVar

T = TypeVar("T")


class Queue(Generic[T], Iterable[T]):
    """
    Python implementation of a C++20 std::queue.
    """

    def __init__(self, iterable: Iterable[T] = ()) -> None:
        self._list: list[T] = list(iterable)

    def __iter__(self) -> Iterator[T]:
        return iter(self._list)

    def __len__(self) -> int:
        return len(self._list)

    def __str__(self) -> str:
        return f"Queue({self._list})"

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
        if isinstance(other, Queue):
            return self._list == other._list  # type: ignore

        return NotImplemented

    def front(self) -> T:
        return self._list[0]

    def back(self) -> T:
        return self._list[-1]

    def empty(self) -> bool:
        return len(self._list) == 0

    def size(self) -> int:
        return len(self._list)

    def push(self, value: T) -> None:
        self._list.append(value)

    def emplace(self, *args: T) -> None:
        self._list += args

    def pop(self) -> None:
        self._list.pop(0)

    def swap(self, other: Queue[T]) -> None:
        self._list, other._list = other._list, self._list


if __name__ == "__main__":
    q = Queue[int]()

    q.push(1)
    q.push(2)

    assert q.front() == 1
    assert q.back() == 2
    assert q.size() == 2
    assert q.empty() is False
    assert str(q) == "Queue([1, 2])"

    q.pop()
    assert q.front() == 2
    assert q.back() == 2
    assert q.size() == 1

    q.emplace(4, 5, 6)
    assert q.front() == 2
    assert q.back() == 6
    assert q.size() == 4

    q.swap(Queue[int]())
    try:
        q.front()

        raise AssertionError("front() should raise when stack is empty")

    except IndexError:
        pass

    try:
        q.back()

        raise AssertionError("back() should raise when stack is empty")

    except IndexError:
        pass

    assert q.size() == 0
    assert q.empty() is True

    assert q == Queue[int]()
    assert q != Queue[int]([1, 2, 3])
