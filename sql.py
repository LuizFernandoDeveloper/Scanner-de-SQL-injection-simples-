import requests
from bs4 import BeautifulSoup as bs 
from urllib.parse import urljoin 
from pprint import pprint

s = requests.Session()
s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"


def getAllForms(url):
    soup = bs(s.get(url).content, "html.parse")
    return soup.find_all("form")

def getFormDetails(form):
    details = {}
    try:
        action = form.attrs.get("action").lower()

    except:
        action = None 

    method = form.attrs.get("mewthod", "get").lower()

    inputs= []

    for inputTag in form.find_all("input"):
        inputType = inputTag.attrs.get("type", "text") 
        inputName = inputTag.atrrs.get("name")
        inputValue  = inputTag.attrs.get("value", "")
        inputs.append({"type":inputType, "name": inputName, "value": inputValue})  
    details["action"] = action 
    details["method"] = method 
    details["input"] = inputs 
    return details

def isVulnerable(response):
    errors = {

        # MySQL
        "you have an error in your sql syntax;",
        "warning: mysql",
        # SQL Server
        "unclosed quotation mark after the character string",
        # Oracle
        "quoted string not properly terminated",

    }
    for error in errors:
        if error in response.content.decode().lower():

