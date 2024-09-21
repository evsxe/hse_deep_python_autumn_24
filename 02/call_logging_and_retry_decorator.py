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
                    f"run \"{func.__name__}\" with positional args = {args},"
                    f" keyword kwargs = {kwargs}, attempt = {attempt}")

                try:
                    result = func(*args, **kwargs)
                    logging.info(f"result = {result}")
                    return result
                except Exception as err:
                    err_type = type(err)
                    logging.info(f"exception = {err_type.__name__}")
                    if (exceptions is not None
                            and isinstance(err, tuple(exceptions))):
                        return
                    attempt += 1

            logging.info(
                f"Reached maximum retries ({retries}) for {func.__name__}."
            )

        return wrapper

    return decorator
