class CustomList(list):
    def __init__(self, *args):
        super().__init__(*args)

    def __add__(self, other):
        if isinstance(other, (list, CustomList)):
            result = [a + b for a, b in zip(self, other)]
            result.extend(self[len(other):])
            result.extend(other[len(self):])
            return CustomList(result)
        if isinstance(other, int):
            return CustomList([x + other for x in self])
        return NotImplemented

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if isinstance(other, (list, CustomList)):
            result = [a - b for a, b in zip(self, other)]
            result.extend(self[len(other):])
            result.extend([-b for b in other[len(self):]])
            return CustomList(result)
        if isinstance(other, int):
            return CustomList([x - other for x in self])
        return NotImplemented

    def __rsub__(self, other):
        if isinstance(other, (list, CustomList)):
            result = [a - b for a, b in zip(other, self)]
            result.extend(other[len(self):])
            return CustomList(result)
        if isinstance(other, int):
            return CustomList([other - x for x in self])
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, (list, CustomList)):
            return sum(self) == sum(other)
        return False

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        if isinstance(other, (list, CustomList)):
            return sum(self) < sum(other)
        return False

    def __le__(self, other):
        if isinstance(other, (list, CustomList)):
            return sum(self) <= sum(other)
        return False

    def __gt__(self, other):
        if isinstance(other, (list, CustomList)):
            return sum(self) > sum(other)
        return False

    def __ge__(self, other):
        if isinstance(other, (list, CustomList)):
            return sum(self) >= sum(other)
        return False

    def __str__(self):
        return f"CustomList({super().__str__()}), сумма элементов: {sum(self)}"
