

def parse_cookie(response: object):
    # Extract cookies from the initial response
    cookies = response.headers.getlist('Set-Cookie')
    cookies_dict = {}
    for cookie in cookies:
        cookie_str = cookie.decode('utf-8')
        for part in cookie_str.split(';'):
            if '=' in part:
                key, value = part.split('=', 1)
                cookies_dict[key.strip()] = value.strip()

    # Store the cookies dictionary in the spider's state
    return cookies_dict

    # Make the next request with the extracted cookies
