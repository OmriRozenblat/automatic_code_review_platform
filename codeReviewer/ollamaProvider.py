
import ollama
from codeReviewer.modelProvider import ModelProvider
import Config

class OllamaProvider(ModelProvider):
    def __init__(self, config: Config.Config):
        self.model_name = config.model_name
        self.temp = config.temperature
        self.predict = config.num_predict
    
    def generate(self, messages: list[dict]) -> str:
        response = ollama.chat(
            model=self.model_name,
            messages=messages,
            options={
                "temperature": self.temp,
                "num_predict": self.predict
            }
        )

        return response["message"]["content"]
