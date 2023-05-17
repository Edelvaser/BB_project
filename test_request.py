import requests
data = {"login":"bbb@bbb.ru", "password":"Zaq1xsw@", "rep_pass":"Zaq1xsw@"}
headers = {'Content-type': 'application/json'}

response = requests.post("https://31.31.196.183:5000/reg",data=data, headers=headers)
print(response.text)