from ContentGenerators.EssayGenerator.EssayThinker import WriteParagraph, GenerateCitation
from ContentGenerators.GlobalTools.Translator import translate
from random import randint
from ContentGenerators.GlobalTools.ImageDownloader import download
from ContentGenerators.GlobalTools.InternetSearcher import FindUrl, ScrapeInformation
from ContentGenerators.GlobalTools.Requestor import reply_to
from ContentGenerators.Prompts import PromptAssembler

prompt = PromptAssembler()

def GeneratePictures(idealist, topic, searchlang, lang, previousimagelinks):
    idealist = idealist[1:-1]
    print(idealist)
    piclist = {}
    for idea in idealist:
        filename = str(randint(1, 99999999999999999999999999999999999999999999999999))
        for i in range(0, 10):
            picdescription = reply_to(prompt.Create("essay", "picture_description", {
                "idea": idea,
                "topic": topic
            }))

            picdescription = str(translate(picdescription, searchlang, lang))
            # IF THE USER CHOSE 'YES' TO HAVE PICTURES IN THE ESSAY, EACH PARAGRAPH'S IDEA WILL BE CONVERTED TO
            # A SMALL SEARCH STRING, AND SEARCHED ON BING... THEN IS DOWNLOADED AND PASTED IN THE WORD DOCUMENT.
            # THIS HELPS MAKE THE PICTURE FOR EACH PARAGRAPH RELATED TO WHAT IT'S TALKING ABOUT...
            try:
                picture = download(previousimagelinks, filename, picdescription, limit=1, output_dir='',
                                   adult_filter_off=False,
                                   force_replace=False, timeout=5, verbose=True)
                if picture != "INVALID SEARCH!":
                    previousimagelinks = previousimagelinks + picture
                    piclist[idealist.index(idea)+1] = filename
                    break
            except Exception as e:
                print(e)
    return piclist


def GenerateParagraph(searchlang, lang, topic, originaltopic, citationformat, idea, oldidea, wordpp):
    citationtries = 0
    arlinks = ""
    url = ""
    previousimagelinks = ""
    resourcelang = searchlang
    while True:
        if citationtries == 4 and lang != "en":
            resourcelang = "en"
            print("TROUBLE FINDING RESOURCES IN (" + lang + ") LANGUAGE, SWITCHING TO (en)")
        if citationtries == 10:
            break
        searchstring = reply_to(
            prompt.Create("essay", "search_question", {
            "idea": idea
        }))
        searchstring = f"{originaltopic} | {str(translate(searchstring, resourcelang, lang))}"
        searchstring = searchstring.replace(".", "").replace("!", "").replace("'", "").replace("?",
                                                                                               "").replace(
            ",",
            "").lower()
        # FORMAT THE SEARCH QUERY AND THEN PROMPT IT TO A SEARCH ENGINE, IF ONE FAILS WE PROCEED TO THE OTHER
        # SEARCH ENGINE, Google -> Bing -> Yahoo. FOR ULTIMATE STABILITY.
        citation = ""
        tries = 0
        while citation == "" or citation == "RESOURCE INVALID":
            print("searching internet")
            try:
                # IT WILL CRASH ON FIRST GENERATION ATTEMPT, SO WE HAVE TO QUARANTINE THAT ERROR.
                arlinks = arlinks + url
            except:
                arlinks = arlinks
            try:
                url = FindUrl(searchstring, arlinks, searchlang)
                print(url)
                ccstring = ScrapeInformation(url, lang)
                arlinks = arlinks + url
                toaddproc = " AND USE AS MUCH INFORMATION AS YOU CAN FROM THIS RESOURCE: '" + ccstring[
                                                                                              0:10000] + "' MAKE SURE TO **ONLY** INCLUDE THE NAME OF THE SOURCE WITH THE DATE OF PUBLISHING IN PARENTHESIS **ONLY ONCE** AT THE END OF THE PARAGRAPH AND NEVER EVER INCLUDE IT INSIDE OF THE TEXT ONLY AT THE END!!!"
                citation = GenerateCitation(searchlang, lang, ccstring, citationformat, url)
            except Exception as e:
                print(e)
                citation = " "
                toaddproc = ""
                gresults = ""
        if citation != "RESOURCE INVALID" and citation != " ":
            break
        citationtries = citationtries + 1
    # AFTER WE HAVE SCRAPED THE INFORMATION, WE FEED THE HUGE LOAD OF INFORMATION TO THE CITATION
    # GENERATOR, IF THIS PART SUCCEEDS IT DECIDES IF WRITING THE PARAGRAPH WILL PROCEED OR NOT.
    citation = citation.replace("**", "").replace("\n\n", "\n")
    if citation.find(r"\u") >= 0:
        citation = citation.encode('utf-8').decode('unicode_escape')

    # AFTER WE HAVE FOUND A RESOURCE AND CITED IT, THE PARAGRAPH GENERATOR WILL WORK AND USE ALL THE PREVIOUS
    # PROCESSES TO GENERATE A CONCISE AND ACCURATE PARAGRAPH.
    # IT WILL USE:
    # 1- Ideas Generated
    # 2- Resource Provided
    # 3- Topic
    # 4- Previous Paragraph
    paragraph = WriteParagraph(oldidea, idea, toaddproc, topic, wordpp)
    paragraph = paragraph.replace("\n", " ").encode('utf-8').decode('unicode_escape').replace("**", "")
    return paragraph, citation