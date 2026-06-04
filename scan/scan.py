from pathlib import Path


class Scan:
    def __init__(self, rules: list, path: str):
        self.path = path
        default_rules_path = Path(__file__).parent / "default_rules.txt"
        with open(default_rules_path, 'r') as f:
            self.rules = f.read().splitlines() 
        self.rules += rules
    
    def get_rules(self):
        return self.rules
    
    def get_file_path(self):
        return self.path
    
    def add_rule(self, rule: str):
        self.rules.append(rule)
        print("Rule added to scan\n")
    def remove_rule(self, index: int):
        try:
            self.rules.pop(index)
        except IndexError:
            print("Invalid index\n")
    
    def print_rules(self):
        print("----------------------\nCurrent rules:\n")
        for i, rule in enumerate(self.rules):
            print(f"{i}:    {rule}")
        print("\n----------------------\n")

