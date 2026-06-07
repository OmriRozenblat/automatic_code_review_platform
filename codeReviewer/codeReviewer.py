
import scan.scan as scan
from codeReviewer.modelProvider import ModelProvider
import Config


class CodeReviewer:
    def __init__(self, model_provider: ModelProvider, config: Config.Config):
        self.model_provider = model_provider
        self.config = config

    def review(self, scan: scan.Scan, rule: str):
        

        messages = [
            {
                "role": "system",
                "content": self.config.system_prompt
            },
            {
                "role": "user",
                "content": self._build_user_prompt(scan, rule)
            }
        ]

        model_result = self.model_provider.generate(messages).strip().upper()

        #validate model output
        
        if model_result not in ["TRUE", "FALSE"]:
            return "INVALID_MODEL_OUTPUT"
        
        
        return model_result
        


    def _build_user_prompt(self, scan: scan.Scan, rule: str) -> str:
        
        return self.config.user_prompt_template.format(rule=rule,
                                                        code=scan.get_content())
        

        
        
