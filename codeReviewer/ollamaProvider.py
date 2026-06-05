
import ollama
from codeReviewer.modelProvider import ModelProvider

class OllamaProvider(ModelProvider):
    def __init__(self, model_name):
        self.model_name = model_name
    
    def generate(self, messages: list[dict]) -> str:
        print("DEBUG: generate called with model:", self.model_name)
        response = ollama.chat(
            model=self.model_name,
            messages=messages
        )

        return response["message"]["content"]
