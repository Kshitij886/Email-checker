import yara

rule = yara.compile(filepath = 'rule.yar')


with open ('text.txt', 'rb') as f:
    file_data = f.read()


matches = rule.match(data = file_data)

if matches == []:
    print("malware")
else :
    print(matches)

