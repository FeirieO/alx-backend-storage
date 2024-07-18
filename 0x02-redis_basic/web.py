#!/usr/bin/env python3
""" Implementing an expiring web cache and tracker
    obtain the HTML content of a particular URL and returns it """
import redis
import requests

r = redis.Redis()

def get_page(url: str) -> str:
    """ track how many times a particular URL was accessed in the key
        "count:{url}"
        and cache the result with an expiration time of 10 seconds """
    
    # Increment the access count
    r.incr(f"count:{url}")
    
    cached_content = r.get(f"cached:{url}")
    
    if cached_content:
        return cached_content.decode('utf-8')
    
    resp = requests.get(url)
    r.setex(f"cached:{url}", 10, resp.text)
    
    return resp.text

if __name__ == "__main__":
    print(get_page('http://slowwly.robertomurray.co.uk'))