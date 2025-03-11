from ContentGenerators.GlobalTools.Requestor import reply_to
from ContentGenerators.GlobalTools.Translator import translate
from random import randint
from datetime import date

from ContentGenerators.Prompts import PromptAssembler

prompt = PromptAssembler()

def WriteParagraph(oldidea, idea, toaddproc, topic, wordpp):
    paragraph = ""
    tries = 0
    while (paragraph == "" or paragraph == "I'm sorry, I can't fulfill this request.") and tries < 10:
            if oldidea == "":
                paragraph = reply_to(prompt.Create("essay", "old_idea_paragraph", {
                    "wordpp": str(wordpp),
                    "idea": idea,
                    "toaddproc": toaddproc,
                    "topic": topic
                }))
            else:
                paragraph = reply_to(prompt.Create("essay", "paragraph", {
                    "wordpp": str(wordpp),
                    "idea": idea,
                    "oldidea": oldidea,
                    "toaddproc": toaddproc,
                    "topic": topic
                }))
            tries = tries + 1
    paragraph = paragraph.replace("##", "")
    paragraph = paragraph.replace("â", "")
    return paragraph


def GenerateBodyParagraphIdea(count, topic, adins):
    error = ""
    for i in range(0, 10):
        try:
            idea = reply_to(prompt.Create("essay", "idea", {
                "count": str(count),
                "topic": topic,
                "adins": adins,
                "error": error
            }))
            print(idea)
            idea = eval(idea)
            if len(idea) == count:
                print("RE-CREATING LIST DUE TO LOW NUMBER OF IDEAS GENERATED")
            return idea
        except Exception as e:
            print(e)
            print("RE-CREATING LIST")
            error = f"[Avoid Such Errors: '{e}']"


def GenerateCitation(searchlang, lang, ccstring, citationformat, url):
    citation = ""
    retries = 0
    today = date.today()
    while citation == "" or len(citation) > 420 >= 0:
        retries = retries + 1
        citation = reply_to(prompt.Create("essay", "citation", {
            "ccstring": ccstring[:2500],  # Sliced to fit length
            "citationformat": citationformat,
            "url": url,
            "today": str(today)
        }))

        urlcode = randint(0, 9999999999999999999999999999999999999999999999999999)
        citation = translate(citation.replace(url, "["+str(urlcode)+"]"), searchlang, lang).replace("["+str(urlcode)+"]", url)
        citation = citation.replace("[URL]", url)
        if retries == 3:
            citation = "RESOURCE INVALID"
            return citation
    return citation