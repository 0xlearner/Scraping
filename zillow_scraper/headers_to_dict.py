def get_headers(s, sep=': ', strip_cookie=True, strip_cl=True, strip_headers: list = []) -> dict():
    d = dict()
    for kv in s.split('\n'):
        kv = kv.strip()
        if kv and sep in kv:
            v=''
            k = kv.split(sep)[0]
            if len(kv.split(sep)) == 1:
                v = ''
            else:
                v = kv.split(sep)[1]
            if v == '\'\'':
                v =''
            # v = kv.split(sep)[1]
            if strip_cookie and k.lower() == 'cookie': continue
            if strip_cl and k.lower() == 'content-length': continue
            if k in strip_headers: continue
            d[k] = v
    return d

h = '''
accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
accept-encoding: gzip, deflate, br
accept-language: en-US,en;q=0.9
cache-control: no-cache
cookie: zguid=23|%2424de1c44-3cce-49ae-8e2d-cfb76b05882a; zgsession=1|df7eeb41-b1f5-46f3-8bdf-79290f694f7b; JSESSIONID=6CEDDD27FAF7C5DF046F3CC285956918; search=6|1624180076880%7Cregion%3Dny%26rect%3D50.62214%252C-68.327143%252C23.705962%252C-125.374896%26disp%3Dmap%26mdm%3Dauto%26p%3D2%26pt%3Dpmf%252Cpf%26fs%3D1%26fr%3D0%26mmm%3D1%26rs%3D0%26ah%3D0%09%0943%09%09%09%09%09%09; AWSALB=HJXkpcOMkgGbc4Us8Ez6RX9jb9bThSAw4B11ng7BgOG/LYJr6U+kMA1FJtmjR4I6Tippk4oSTZmolmTRBcoISvyhd+N1Lof4FUrigdCf7qZ039mDlt39OhIrlc4J; AWSALBCORS=HJXkpcOMkgGbc4Us8Ez6RX9jb9bThSAw4B11ng7BgOG/LYJr6U+kMA1FJtmjR4I6Tippk4oSTZmolmTRBcoISvyhd+N1Lof4FUrigdCf7qZ039mDlt39OhIrlc4J
pragma: no-cache
sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"
sec-ch-ua-mobile: ?0
sec-fetch-dest: document
sec-fetch-mode: navigate
sec-fetch-site: same-origin
sec-fetch-user: ?1
upgrade-insecure-requests: 1
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36

'''

result = get_headers(h)
print(result)