import re
from kivy.network.urlrequest import UrlRequest
import json
import requests
import pickle


def check_email(email):
    # "test_123@test.test"
    template = '[A-Za-z0-9_]+@[A-Za-z]+[.][A-Za-z]+'
    if re.fullmatch(template, email) is not None:
        return True
    else:
        return False

def check_password(password):
    template = '[A-Za-z0-9@#$%^&+=]{8,}'
    if re.fullmatch(template, password) is not None:
        return True
    else:
        return False

def got_json(req, result):
    pass
    # for key, value in req.resp_headers.items():
    #     print('{}: {}'.format(key, value))
# token = "9535dce2b4e4dd726ec9419232750f5a6cdf3214ee4ee88abba36bc3b25e2517"
# def send_request(route="", js_obj = {}):
#     url_base = "http://127.0.0.1:5000/" + route
#     # headers = {'Content-type': 'application/json',
#     #         'Authorization': token}
#     if js_obj:
#         response =  UrlRequest(url_base, req_body=json.dumps(js_obj), req_headers=headers)
#     else:
#         response =  UrlRequest(url_base)
#     response.wait()
#     return response.result

def write_token(json_obj, file="infoData"):
    with open(file, "wb") as fp:
        # json.dump(json_obj, fp)
        pickle.dump(json.dumps(json_obj), fp)

def read_token(file="infoData"):
    try:
        with open(file, "rb") as fp:
            # token = json.load(fp)
            token = pickle.load(fp)
            return token["token"]
    except:
        return None
# https://supremeoverseer.ru/
# def send_request(url_base = "http://127.0.0.1:5000", route="", js_obj = {}, headers={}):
# 31.31.196.183:5000
# https://supremeoverseer.ru
def send_request(url_base = "https://supremeoverseer.ru", route="", js_obj = {}, headers={}):
    if js_obj:
        response =  UrlRequest(url_base + route, req_body=json.dumps(js_obj), req_headers=headers)
    else:
        response =  UrlRequest(url_base)
    response.wait()
    print(response.result)
    return response.result

# print(send_request("https://supremeoverseer.ru/"))
# print(send_request("auth/", {"login":"vvvv","password":"vcvc"}))

def txt_end_word(num):
    if num%10 == 1 and num != 11:
        return "балл"
    if num%10 in (2, 3, 4) and num not in (12, 13, 14):
        return "балла"
    return "баллов"