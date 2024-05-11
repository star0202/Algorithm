from __future__ import annotations
from typing import TypeVar, overload, Callable

T = TypeVar("T")


class AutoSizedList(list[T]):
    """
    A list that automatically resizes itself when the accessed index is out of range.

    Parameters
    ----------
    default : Callable[[], T]
        A function that returns the default value for the list.

    Methods
    -------
    resize(size: int) -> None
        Resizes the list to the specified size.
    """

    def __init__(self, default: Callable[[], T]) -> None:
        self.default = default

    def resize(self, size: int, allocator: Callable[[], T] | None = None) -> None:
        allocator = allocator or self.default

        if len(self) >= size:
            return

        self.extend([allocator() for _ in range(size - len(self))])

    @overload
    def __setitem__(self, index: int, value: T) -> None: ...

    @overload
    def __setitem__(self, index: slice, value: list[T]) -> None: ...

    def __setitem__(self, index: int | slice, value: T | list[T]) -> None:
        is_slice = isinstance(index, slice)
        is_list = isinstance(value, list)

        if (is_slice and not is_list) or (not is_slice and is_list):
            raise ValueError("Incompatible types")

        self.resize(index.stop if is_slice else index + 1)

        super().__setitem__(index, value)  # type: ignore

    @overload
    def __getitem__(self, index: int) -> T: ...

    @overload
    def __getitem__(self, index: slice) -> AutoSizedList[T]: ...

    def __getitem__(self, index: int | slice) -> T | AutoSizedList[T]:
        self.resize(index.stop if isinstance(index, slice) else index + 1)

        return super().__getitem__(index)  # type: ignore


if __name__ == "__main__":
    li = AutoSizedList(lambda: AutoSizedList(int))
    li[0][0] = 1
    li[0][1] = 2
    li[1][0] = 3
    li[1][1] = 4

    print(li)

    print([id(x) for x in li])
