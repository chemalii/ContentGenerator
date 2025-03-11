# Requestor for the GemEssayGenerator
# Author Sami Chemali
# THIS IS WHERE WE PROMPT A LANGUAGE MODEL, IT'S PRONE TO CHANGE... SO HAVING IT REFACTORED IS A WISE CHOICE.

from openai import OpenAI
from ContentGenerators.GlobalTools.SettingsManager import Settings

settings = Settings().data

# This a replaceable module, in which you can easily replace the code to prompt another service or model,
# Further simplifying the process of editing which models are used for the essay generator.

if settings["LANGUAGE_MODEL"]["OPENAI"]:
    client = OpenAI(
        # This is the default and can be omitted
        api_key=settings["LANGUAGE_MODEL"]["API_KEY"],
    )
else:
    client = OpenAI(base_url=settings["LANGUAGE_MODEL"]["BASE_URL"], api_key=settings["LANGUAGE_MODEL"]["API_KEY"])
    Model = settings["LANGUAGE_MODEL"]["MODEL"]

def reply_to(message, context=False, info=False):
    try:
        if context:
            response = client.chat.completions.create(
                messages=message,
                model=Model,
            )
        else:
            message = [{"role": "system", "content": "Only provide the answer without explanation or submission, if some information isnt available, work around and try to manage to make a complete response."}, {"role": "user", "content": message}]
            response = client.chat.completions.create(
                messages=message,
                model=Model,
            )
        if settings["LANGUAGE_MODEL"]["OPENAI"]:
            tokens = response.usage.total_tokens
        else:
            tokens = 0
        response = response.choices[0].message.content
    except Exception as e:
        print(e)
        # We have to ensure that the model can handle large amounts of characters in the prompt, one intensive
        # feature can be generating citations and generating paragraphs, where a huge load of scraped information
        # is fed into the model to utilize authentic information from trusted sources on the internet.
        response = "OVERLOADED OR MODEL FAILED."
        tokens = 0
    response = response.replace("##", "").replace("(\"", "(").replace("\")", ")")
    if response[-1] == "\"" and response[0] == "\"":
        response = response[1:-1]
    if info:
        return response, tokens
    else:
        return response
