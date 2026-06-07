
import scan.scan as scan
from codeReviewer.modelProvider import ModelProvider
import Config


class CodeReviewer:
    def __init__(self, model_provider: ModelProvider, config: Config.Config):
        self.model_provider = model_provider
        self.config = config

    def review(self, scan: scan.Scan):
        rules = scan.get_rules()
        model_result_list = []
        for index, rule in enumerate(rules):

            messages = [
                {
                    "role": "system",
                    "content": self.config.system_prompt
                },
                {
                    "role": "user",
                    "content": self._build_user_prompt(scan, f"{index}. {rule}")
                }
            ]

            model_result_list.append(self.model_provider.generate(messages).strip().upper())

        if len(model_result_list) != len(scan.get_rules()):
            return "INVALID_MODEL_OUTPUT"
        for res in model_result_list:
            if res.split()[1] not in ["TRUE", "FALSE"]:
                return "INVALID_MODEL_OUTPUT"
        
        
        return "\n".join(model_result_list)
        


    def _build_user_prompt(self, scan: scan.Scan, rules: str) -> str:
        
        return self.config.user_prompt_template.format(rules=rules,
                                                        code=scan.get_content())
        

        
        
