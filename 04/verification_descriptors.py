class BaseDescriptor:
    def __init__(self) -> None:
        self.owner = None
        self.name = None

    def __set_name__(self, owner: type, name: str) -> None:
        self.owner = owner
        self.name = name

    def __set__(self, instance: object, value: any) -> None:
        if not self.validate(value):
            raise ValueError(f"Invalid value for {self.name}: {value}")
        instance.__dict__[self.name] = value

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)

    def validate(self, value: any) -> bool:
        raise NotImplementedError("Subclasses must implement this method.")


class IntegerDescriptor(BaseDescriptor):
    def validate(self, value: any) -> bool:
        return isinstance(value, int)

    def __repr__(self):
        return "IntegerDescriptor"


class StringDescriptor(BaseDescriptor):
    def validate(self, value: any) -> bool:
        return isinstance(value, str) and bool(value)

    def __repr__(self):
        return "StringDescriptor"


class PositiveIntegerDescriptor(BaseDescriptor):
    def validate(self, value: any) -> bool:
        return isinstance(value, int) and value > 0

    def __repr__(self):
        return "PositiveIntegerDescriptor"


class Data:
    num = IntegerDescriptor()
    name = StringDescriptor()
    price = PositiveIntegerDescriptor()

    def __init__(self, num: int, name: str, price: int) -> None:
        self.num = num
        self.name = name
        self.price = price

    def __repr__(self):
        return (f"Data(num={self.num},"
                f" name='{self.name}',"
                f" price={self.price})")

    def update_price(self, new_price: int) -> None:
        self.price = new_price

    def display_info(self) -> str:
        return (f"Data Info - Num: {self.num},"
                f" Name: {self.name},"
                f" Price: {self.price}")
