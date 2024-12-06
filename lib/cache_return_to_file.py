import os
import pickle
import hashlib


def file_cache(cache_dir="./cache"):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Generate a unique cache key based on function arguments
            key = hashlib.md5(pickle.dumps((args, kwargs))).hexdigest()
            cache_path = os.path.join(cache_dir, key)

            # Check if the cache exists and is valid
            if os.path.exists(cache_path):
                with open(cache_path, "rb") as f:
                    return pickle.load(f)

            # If not, call the function and cache the result
            result = func(*args, **kwargs)
            os.makedirs(cache_dir, exist_ok=True)
            with open(cache_path, "wb") as f:
                pickle.dump(result, f)

            return result

        return wrapper

    return decorator
