# Internet Searcher for the GemEssayGenerator
# Author Sami Chemali

from bs4 import BeautifulSoup
from urllib.request import urlopen
from ContentGenerators.GlobalTools.Translator import translate
from ContentGenerators.GlobalTools.PDFResourceManager import ExtractText, CheckPDF
from googlesearch import search


BlackListed = ["bing.", "google.", ".txt", "medium.",
               "educationmiddleeast.", "quora.", "u.ae", "youtube.", "facebook.", ".jpg", "wikipedia."]


def approve(url):
    url = url.lower()
    result = "NOTHING"
    if CheckPDF(url):
        return "PDF"
    for i in BlackListed:
        if url.find(i) >= 0:
            result = "BLACKLISTED"
            return result
    return result


def FindUrl(searchstring, arlinks, lang):
    results = search(searchstring, lang=lang, num_results=20)
    if results:
        for url in results:
            print(url)
            if arlinks.find(url) >= 0 or approve(url) == "BLACKLISTED" or ScrapeInformation(url, 'en') == "ERROR":
                if approve(url) == "PDF" and arlinks.find(url) == -1:
                    return url
                else:
                    "LOOP AGAIN UNTIL NEW RESOURCE HAS BEEN FOUND"
            else:
                return url


def ScrapeInformation(url, lang, maxlength=4300):
    if approve(url) == "PDF":
        ccstring = ExtractText(url)
        if ccstring == "":
            ccstring = "ERROR"
        else:
            ccstring = translate(ccstring, 'en', lang)
    else:
        try:
            html = urlopen(url, timeout=10).read()
            soup = BeautifulSoup(html, features="html.parser")
            # kill all script and style elements
            for script in soup(["script", "style"]):
                script.extract()  # rip it out
            # get text
            text = soup.get_text()
            # break into lines and remove leading and trailing space on each
            lines = (line.strip() for line in text.splitlines())
            # break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in
                      line.split("  "))
            # drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)
            ccstring = text[0:maxlength]
            if ccstring == "":
                ccstring = "ERROR"
            else:
                ccstring = translate(ccstring, 'en', lang)
        except Exception as e:
            print(e)
            ccstring = "ERROR"
    return ccstring
