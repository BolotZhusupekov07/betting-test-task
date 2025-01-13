from functools import wraps
from typing import Callable, Type


def raise_one_exception(exception: Type[Exception]):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception:
                raise exception

        return wrapper

    return decorator
