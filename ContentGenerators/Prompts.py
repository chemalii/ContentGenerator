"""
    Autor: Chemalii - GitHub
    Date: 2023/04/12
    Explanation: This is the Prompt Assembler, created to decrease the bloat of prompt-texts in py files.
"""

import os
import json


current_file_path = os.path.dirname(__file__)


class PromptAssembler:
    def __init__(self,):
        self.content_type = ""
        self.prompt_type = ""
        self.info = {}

    def LoadJsonFile(self):
        full_path = os.path.join(current_file_path, "PromptSet", f"{self.content_type}.json")
        with open(full_path, 'r') as f:
            data = json.load(f)
        return data

    def Create(self, content_type, prompt_type, info):
        self.content_type = content_type
        self.prompt_type = prompt_type
        self.info = info

        prompt = self.LoadJsonFile()[prompt_type]

        for infotype in info:
            prompt = prompt.replace(f"[{infotype}]", info[infotype])
        return prompt


