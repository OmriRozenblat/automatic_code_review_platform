
import scan.scan as scan
from codeReviewer.modelProvider import ModelProvider
import Config


class CodeReviewer:
    def __init__(self, model_provider: ModelProvider, config: Config.Config):
        self.model_provider = model_provider
        self.config = config

    def review(self, scan: scan.Scan):
        messages = [
            {
                "role": "system",
                "content": self.config.system_prompt
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
        return self.config.user_prompt_template.format(rules=scan.convert_rules_to_text(),
                                                        code=scan.get_content())
        
        #return f"""
         #   Check whether the following Python code complies with this rules.


          #  Rules:
           # {scan.convert_rules_to_text()}

            #Code:
            #{scan.get_content()}
            #"""
                    
