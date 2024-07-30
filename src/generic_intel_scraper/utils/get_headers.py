def get_headers(s, sep=': ', strip_cookie=True, strip_cl=True, strip_headers: list = []) -> dict():
    d = dict()
    for kv in s.split('\n'):
        kv = kv.strip()
        if kv and sep in kv:
            v = ''
            k = kv.split(sep)[0]
            if len(kv.split(sep)) == 1:
                v = ''
            else:
                v = kv.split(sep)[1]
            if v == '\'\'':
                v = ''
            # v = kv.split(sep)[1]
            if strip_cookie and k.lower() == 'cookie':
                continue
            if strip_cl and k.lower() == 'content-length':
                continue
            if k in strip_headers:
                continue
            d[k] = v
    return d


print(get_headers(
    '''
sec-ch-ua:"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"
sec-ch-ua-mobile:?0
sec-ch-ua-platform:
"Windows"
sec-fetch-dest:document
sec-fetch-mode:navigate
sec-fetch-site:same-origin
sec-fetch-user:?1
upgrade-insecure-requests:1
user-agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36



    '''
))
