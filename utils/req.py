import re
from urllib.parse import urlparse
from logSetup import logSetup as CL
import requests
from bs4 import BeautifulSoup

def verify_Urls(newReq, oldReq):
    """verifies the new and old vendor url"""
    req1 = urlparse(newReq.headers['Location'])
    # req2 = urlparse(oldReq.headers['Location'])

    # strips the www. from new url like www.google.com will become google.com for new vendors
    newUrl = re.sub('^www(\d+)?.|:(\d+)$', '', req1[1])

    if newUrl == oldReq:
        return 1, ''
    nUrl = newUrl

    return 0, nUrl


def verify_Product_Name(data, name):
    """Verifies if the given product is listed by current vendor"""
    soup = BeautifulSoup(data, 'html.parser')
    if re.search(name, soup.text):
        return 1
    return 0


def fetch(reqUrl, prodName, dataDict):
    """fetches the required data """
    url = 'http://' + reqUrl
    # print("Queried URL: " + url)
    # initializing default values for variables
    isUrlIdentical = 1
    newUrl = ''
    isProdNamePresent = 0
    statusCode = 200

    # if the data is present in the dict then it will not request vendor for data instead uses the existing the data
    if reqUrl in dataDict:
        text = dataDict[reqUrl]['text']
        rUrl = dataDict[reqUrl]['rUrl']
        statusCode = dataDict[reqUrl]['st']

        if rUrl:
            isUrlIdentical = 0
        # checks if the product is listed on vendor website
        isProdNamePresent = verify_Product_Name(text, prodName)

        return isUrlIdentical, newUrl, isProdNamePresent, statusCode
    else:

        res = None

        # noinspection PyBroadException
        try:
            res = requests.get(url, timeout=10)

            # gets the new and old vendor based on the data received and compares if there is a new vendor
            if res.status_code == 200:
                if len(res.history) >= 2:
                    newReq = res.history[-1]
                    oldReq = res.history[-2]
                    # checks if the new and current vendors are same
                    isUrlIdentical, newUrl = verify_Urls(newReq, reqUrl)

                else:
                    statusCode = res.status_code

                # if the data is not present in the dict then it will request vendor for data and adds it to the dict for later use
                if not reqUrl in dataDict:
                    dataDict[reqUrl] = {}
                    dataDict[reqUrl]['text'] = res.text
                    dataDict[reqUrl]['rUrl'] = newUrl
                    dataDict[reqUrl]['st'] = statusCode
                # checks if the product is listed on vendor website
                isProdNamePresent = verify_Product_Name(res.text, prodName)
        except:
            pass
        if res and res.status_code:
            statusCode = res.status_code
    return isUrlIdentical, newUrl, isProdNamePresent, statusCode
