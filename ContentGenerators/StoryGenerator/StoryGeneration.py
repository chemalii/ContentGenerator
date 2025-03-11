import datetime
from os import remove
from GlobalTools.FileInspector import get_file_size
from GlobalTools.FlowManager import startinfo, addinfo, readinfo
from GlobalTools.Requestor import reply_to
from GlobalTools.DocumentBuilder import BuildDocument
from GlobalTools.Translator import translate


def Generate_Story(hashstring, path, intpov, end, characters, premium: bool, title: str, about: str,
                   chapters: int,
                   lang: str, filetype: str, filename: str):
    pov = ""

    listfile = f'UserTempInfo/{hashstring}.pickle'
    data = {'chapters': {}}
    startinfo(hashstring, data)

    if intpov == 1:
        pov = "first"
    elif intpov == 2:
        pov = "second"
    elif intpov == 3:
        pov = "third"

    chaptertext = ""
    storyinformation = ''

    for i in range(1, 10):
        try:
            storyinformation = reply_to([{"role": "user", "content": (
                    "There is a " + pov + " person point of view story with the title '" + title + "', it talks about '" + about + "'... Using this information, create all the important characters according to this: '" + characters + "', and describe events happening in the story and make the story clear (IF THERE ISNT ENOUGH INFORMATION, GENERATE YOUR OWN STORY LINE AND PASTE IT IN THE LIST). Provide a python dictionary with " + str(
                chapters) + " chapters, each of them having an event of its own.. ONLY PROVIDE A PYTHON dictionary AND NOTHING ELSE! (EXAMPLE(STRICTLY FOLLOW THIS METHOD!!!): {0: \"CHARACTER 1(IMPORTANCE) + CHARACTER 2(IMPORTANCE) + etc...\", 1:\"CHAPTER 1 SUMMARY\", 2:\"CHAPTER 2 SUMMARY\", ...}) NOTE IN LIST[0] ENTER ALL THE CHARACTERS BY THEIR NAMES IN THE STORY AND THEIR IMPORTANCE!!! MAKE EACH CHAPTER SUMMARY VERY EXPLAINED WITH DETAIL AND EXPLAIN WHAT HAPPENS!(MAKE SURE EACH CHAPTER PART IS MORE THAN 7 WORDS BUT NOT MORE THAN 15!) AND ONLY USE \" TO CREATE THE CHAPTER STRINGS! MAKE SURE THE LIST HAS ALL 0 to " + str(
                chapters) + " chapters STRICTLY MAKE THE LIST HAVE " + str(
                chapters + 1) + " PARTS !!(STRICTLY MAKE THE END OF THE STORY BE THE SAME AS THIS DESCRIPTION:'" + end + "'): ")}],
                                        context=True).replace("\n", "").replace(",", ", ").replace("```python", "").replace("```", "")
            print(storyinformation)
            storyinformation = eval(storyinformation)
            if len(storyinformation) == chapters + 1:
                break
        except:
            print('Recreating the storyline')

    for i in range(1, chapters + 1):
        print("Chapter: " + str(i))
        currentchapter = i
        if currentchapter == 1:
            print("STARTING")
            prompt = "(ALWAYS START WITH MENTIONING THE CHAPTER AND A CUSTOM TITLE(NEVER USE '" + str(
                title) + "'!!!) OF YOUR OWN CHOICE ACCORDING TO THIS (EX: CHAPTER #: 'BASIC 3 WORD SUMMARY OF " + str(
                storyinformation[i]) + "') This is the first chapter in a story, with the title: '" + str(
                title) + "' and the characters: (" + str(
                storyinformation[0]) + "), This chapter should talk about: '" + str(storyinformation[
                                                                                        i]) + "'... Write A NOT VERY LONG AND TALL first chapter... ONLY PROVIDE THE TEXT ASKED FOR AND NOTHING ELSE, WRITE IT LIKE A STORY AND NOT A SUMMARY AND DO NOT CONCLUDE, BE DESCRIPTIVE AND ENTERTAINING AND CREATIVE!!!)(MAKE SURE TO NEVER SUMMARIZE AT THE END OF THE CHAPTER!)[STRICTLY MAKE IT IN " + pov + " PERSON POINT OF VIEW AND DIRECTLY DIVE INTO THE CHAPTER AND ITS EVENTS!!!](START BY MENTIONING CHAPTER " + str(
                i) + ", AND MAKE IT LONG AS POSSIBLE! (PREFERABLY 450 TO 600 WORDS!!!)(MAKE SURE ITS AS UNIQUE AS POSSIBLE AND NOT SIMILAR TO ANYTHING!))"
            context = [{"role": "assistant", "content": chaptertext}, {"role": "user", "content": prompt}]
        elif currentchapter == chapters:
            print("ENDING")
            prompt = "This is chapter " + str(i) + ", it should talk about: '" + str(storyinformation[
                                                                                         i]) + "' AND NOTHING ELSE, ADD DETAIL!!... ONLY PROVIDE THE TEXT ASKED FOR AND NOTHING ELSE, WRITE IT LIKE A STORY AND NOT A SUMMARY AND DO NOT CONCLUDE, BE DESCRIPTIVE AND ENTERTAINING AND CREATIVE!!!) THIS CHAPTER IS A CONTINUATION FROM THE PREVIOUS CHAPTER WHICH WAS ABOUT: '" + str(
                storyinformation[
                    i - 1]) + "' CONTINUE DIRECTLY AFTER THIS! (HERE IS A DESCRIPTION OF HOW THE END SHOULD GO: '" + str(
                end) + "')[STRICTLY MAKE IT IN " + str(
                pov) + " PERSON POINT OF VIEW AND DIRECTLY DIVE INTO THE CHAPTER AND ITS EVENTS!!!](START BY MENTIONING CHAPTER " + str(
                i) + ", AND MAKE IT LONG AS POSSIBLE! (PREFERABLY 450 TO 600 WORDS!!!)):"
            context = [{"role": "assistant", "content": chaptertext}, {"role": "user", "content": prompt}]
        else:
            prompt = "This is chapter " + str(i) + ", it should talk about: '" + str(storyinformation[
                                                                                         i]) + "' AND NOTHING ELSE, ADD DETAIL!!... (ONLY PROVIDE THE TEXT ASKED FOR AND NOTHING ELSE, WRITE IT LIKE A STORY AND NOT A SUMMARY AND DO NOT CONCLUDE, BE DESCRIPTIVE AND ENTERTAINING AND CREATIVE START DIRECTLY WITH NO INTRODUCTION INTO THE STORY AND ITS CONTENT ALWAYS BE ORIGINAL AND ADD NEW EVENTS AND DETAILS!!!)(MAKE SURE TO NEVER SUMMARIZE AT THE END OF THE CHAPTER!)[STRICTLY MAKE IT IN " + str(
                pov) + " PERSON POINT OF VIEW AND DIRECTLY DIVE INTO THE CHAPTER AND ITS EVENTS!!!](START BY MENTIONING CHAPTER " + str(
                i) + ", AND MAKE IT LONG AS POSSIBLE BUT NOT TOO LONG! (PREFERABLY 450 TO 600 WORDS!!!))"
            context = [{"role": "assistant", "content": chaptertext}, {"role": "user", "content": prompt}]
        chaptertext = reply_to(context, context=True)
        addinfo(listfile, "chapters", i-1, str(translate(chaptertext, lang, lang)))
    data = readinfo(listfile)
    pads = data["chapters"]
    BuildDocument(path, premium, chapters, False, None, None, filename, pads, lang, title, filetype, False)
    now = datetime.datetime.now()
    filesize = get_file_size(f"{path}/{filename}.{filetype}")
    remove(f"{path}/{filename}.{filetype}")
    remove(listfile)
