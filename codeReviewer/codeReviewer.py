print("LOADING codeReviewer.py")

import scan.scan as scan
from codeReviewer.modelProvider import ModelProvider


class CodeReviewer:
    def __init__(self, model_provider: ModelProvider, system_prompt: str):
        self.model_provider = model_provider
        self.system_prompt = system_prompt

    def review(self, scan: scan.Scan):
        messages = [
            {
                "role": "system",
                "content": self.system_prompt
            },
            {
                "role": "user",
                "content": self._build_user_prompt(scan)
            }
        ]

        return self.model_provider.generate(messages)

    def _build_user_prompt(self, scan) -> str:
        rules_text = "\n".join(
            f"{index + 1}. {rule}"
            for index, rule in enumerate(scan.get_rules())
        )

        return f"""
Review the following Python code according to the rules.

Rules:
{rules_text}

Code:
{scan.get_content()}
"""
        
