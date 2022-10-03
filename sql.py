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
            return True

    return False

def scannSqlInjection(url):

    for c in "\"'": 
        newUrl = f"{url}{c}"
        print("[!]tentando", newUrl)
        res = s.get(newUrl)
        if(isVulnerable(res)):
            print("[+] SQL Injection Vulneravel")
            return
    forms = getAllForms(url)
    print(f"[+] Detectado {len(forms)} forms na url {url}")    
    for form in forms:
        formDetails = getFormDetails(form)
        for c in "\"'":
            data = {}
            for inputTag in formDetails["inputs"]:
                if inputTag["type"] == "hidden" or inputTag["value"]:
                    try:
                        data[inputTag["name"]] = inputTag["value"] + c
                    
                    except:
                        pass
                elif inputTag["type"] != "submit": 
                    data[inputTag["name"]] = f"teste{c}"
            
            url = urljoin(url, formDetails["action"])

            if formDetails["method"] == "post":
                res = s.post(url, data = data)

            elif formDetails["method"] == "get":

                res = s.get(url, params=data)
            
            if isVulnerable(res):

                print("[!] SQL Injection vulneravel para a url", url)
                print("[+] Forms")
                pprint(formDetails)
                break


if __name__ == "__main__":

    url = "http://testphp.vulnweb.com/search.php?test=query"
    scannSqlInjection(url)


