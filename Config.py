import json



class Config:
    def __init__(self):
        try:
            with open("config.json", "r") as f:
                self.config = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError("config file not found")
        
        self.max_parallel_scans = self.config["max_parallel_scans"]
        self.scan_ttl_minutes = self.config["scan_ttl_minutes"]
        self.model_provider = self.config["model"]["provider"]
        self.model_name = self.config["model"]["name"]
        self.system_prompt = self.config["prompts"]["system_prompt"]
        self.user_prompt_template = self.config["prompts"]["user_prompt_template"]


    