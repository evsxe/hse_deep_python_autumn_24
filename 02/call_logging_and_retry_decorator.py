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
                except Exception as err:
                    err_type = type(err)
                    logging.info("exception = %s", err_type.__name__)
                    if exceptions is not None and err_type not in exceptions:
                        return None
                    attempt += 1

            logging.info(
                "Reached maximum retries (%s) for %s.",
                retries, func.__name__)
            return None

        return wrapper

    return decorator
