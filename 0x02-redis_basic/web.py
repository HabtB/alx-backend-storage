#!/usr/bin/python3

import requests
import redis
import time
from functools import wraps


""" Initialize Redis client """
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


def count_accesses(method):
    """ counts the accesses"""
    @wraps(method)
    def wrapper(url):
        """This is a wrapper
        """
        # Increment the count for the accessed URL
        url_key = f"count:{url}"
        redis_client.incr(url_key)

        # Call the original method
        result = method(url)

        # Set the cache with a 10-second expiration
        cache_key = f"cache:{url}"
        redis_client.setex(cache_key, 10, result)

        return result

    return wrapper


@count_accesses
def get_page(url):
    """ Check if the content is cached
    """
    cache_key = f"cache:{url}"
    cached_content = redis_client.get(cache_key)

    if cached_content:
        return cached_content.decode('utf-8')

    # If not cached, fetch the content from the URL
    response = requests.get(url)
    content = response.text

    return content


if __name__ == "__main__":
    # Example usage of get_page function
    url = "http://slowwly.robertomurray.co.uk/delay/1000/url/https:
        //www.example.com"
    html_content = get_page(url)
    print(f"HTML content for {url}(accessed {redis_client.
        get(f'count:{url}').decode('utf-8')} times):\n{html_content}")

