
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
        model_result_list = model_result.splitlines()
        print(model_result + "\n")
        print(model_result_list)
        print("\n")
        print(scan.get_rules())
        if len(model_result_list) != len(scan.get_rules()):
            return "INVALID_MODEL_OUTPUT"
        for res in model_result_list:
            if res.split()[1] not in ["TRUE", "FALSE"]:
                return "INVALID_MODEL_OUTPUT"
        
        
        print(model_result + "\n")
        return model_result
        



    def _build_user_prompt(self, scan: scan.Scan) -> str:
        
        
        return self.config.user_prompt_template.format(rules=scan.convert_rules_to_text(),
                                                        code=scan.get_content())
        
        
