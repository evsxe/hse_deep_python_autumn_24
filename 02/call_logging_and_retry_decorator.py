import logging

from typing import (
    Callable,
    Type,
    Any,
    Optional,
    List
)

logging.basicConfig(level=logging.INFO)


def retry_deco(retries: int = 3,
               exceptions: Optional[List[Type[Exception]]] = None) -> Callable:
    """
    :param retries: number of restarts of the function being decorated
    :param exceptions: a list of expected exception classes
    :return: decorated feature
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            attempt = 1
            while attempt <= retries:
                logging.info(
                    "run \"%s\" with positional args = %s,"
                    " keyword kwargs = %s, attempt = %s",
                    func.__name__, args, kwargs, attempt)

                try:
                    result = func(*args, **kwargs)
                    logging.info("result = %s", result)
                    return result
                except tuple(exceptions) \
                        if exceptions else (ValueError, TypeError) as err:
                    err_type = type(err)
                    logging.info("exception = %s",
                                 err_type.__name__)
                    if exceptions is not None:
                        return None
                    attempt += 1

            logging.info(
                "Reached maximum retries (%s) for %s.",
                retries, func.__name__)
            return None

        return wrapper

    return decorator

@retry_deco(3)
def add(a, b):
    return a + b


add(4, 2)
# run "add" with positional args = (4, 2), attempt = 1, result = 6

add(4, b=3)
# run "add" with positional args = (4,), keyword kwargs = {"b": 3}, attempt = 1, result = 7


@retry_deco(3)
def check_str(value=None):
    if value is None:
        raise ValueError()

    return isinstance(value, str)


check_str(value="123")
# run "check_str" with keyword kwargs = {"value": "123"}, attempt = 1, result = True

check_str(value=1)
# run "check_str" with keyword kwargs = {"value": 1}, attempt = 1, result = False

check_str(value=None)
# run "check_str" with keyword kwargs = {"value": None}, attempt = 1, exception = ValueError
# run "check_str" with keyword kwargs = {"value": None}, attempt = 2, exception = ValueError
# run "check_str" with keyword kwargs = {"value": None}, attempt = 3, exception = ValueError


@retry_deco(2, [ValueError])
def check_int(value=None):
    if value is None:
        raise ValueError()

    return isinstance(value, int)

check_int(value=1)
# run "check_int" with keyword kwargs = {"value": 1}, attempt = 1, result = True

check_int(value=None)
# run "check_int" with keyword kwargs = {"value": None}, attempt = 1, exception = ValueError # нет перезапуска