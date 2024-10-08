from typing import Any


class CustomMeta(type):
    def __new__(cls, name, bases, class_dict, **kwargs):
        custom_dict = {
            f'custom_{attr}' if not attr.startswith('__') else attr: value
            for attr, value in class_dict.items()
        }

        new_class = super().__new__(cls, name, bases, custom_dict)

        def custom_setattr(self, key: str, value: Any):
            if not key.startswith('__'):
                object.__setattr__(self, f'custom_{key}', value)
            else:
                object.__setattr__(self, key, value)

        def custom_getattribute(self, key: str):
            if not key.startswith('__') and not key.startswith('custom_'):
                raise AttributeError(f"{key} is not defined")
            return object.__getattribute__(self, key)

        new_class.__setattr__ = custom_setattr
        new_class.__getattribute__ = custom_getattribute

        return new_class
