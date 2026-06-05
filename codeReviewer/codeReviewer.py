
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

        model_result =  self.model_provider.generate(messages).strip().upper()
        print(model_result + "\n")
        if model_result == "YES":
            return "TRUE"
        if model_result == "NO":
            return "FALSE"
        return "INVALID_MODEL_OUTPUT"



    def _build_user_prompt(self, scan: scan.Scan) -> str:
        
        ##print("scan file content\n")
        ##print(scan.get_content())
        ##print("------------------")

        return f"""
            Check whether the following Python code complies with this rule.


            Rules:
            {scan.convert_rules_to_text()}

            Code:
            {scan.get_content()}
            """
                    
