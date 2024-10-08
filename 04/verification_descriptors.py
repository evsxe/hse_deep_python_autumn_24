class BaseDescriptor:
    def __set_name__(self, owner: type, name: str) -> None:
        self.owner = owner
        self.name = name

    def __set__(self, instance: object, value: any) -> None:
        if not self.validate(value):
            raise ValueError(f"Invalid value for {self.name}: {value}")
        instance.__dict__[self.name] = value

    def validate(self, value: any) -> bool:
        raise NotImplementedError("Subclasses must implement this method.")


class FloatDescriptor(BaseDescriptor):
    def validate(self, value: any) -> bool:
        return isinstance(value, float)


class NonEmptyStringDescriptor(BaseDescriptor):
    def validate(self, value: any) -> bool:
        return isinstance(value, str) and bool(value)


class RangeDescriptor(BaseDescriptor):
    def __init__(self, min_value: float, max_value: float) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: float) -> bool:
        return isinstance(value, (
        int, float)) and self.min_value <= value <= self.max_value


class Product:
    price: float = FloatDescriptor()
    name: str = NonEmptyStringDescriptor()
    quantity: int = RangeDescriptor(0, 100)

    def __init__(self, price: float, name: str, quantity: int) -> None:
        self.price = price
        self.name = name
        self.quantity = quantity
