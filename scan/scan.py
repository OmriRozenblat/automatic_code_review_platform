from pathlib import Path



class Scan:
    def __init__(self):
        default_rules_path = Path(__file__).parent / "default_rules.txt"
        with open(default_rules_path, 'r') as f:
            self.rules = f.read().splitlines() 
    
    def get_file_from_path(self, path: str):
        if not path:
            folder = Path(__file__).parent.parent / "file_to_scan"
            self.path = next(folder.glob("*.*"), None)
            print(self.path)
            if self.path is None:
                raise FileNotFoundError("No .py file found in file_to_scan")
        else:
            self.path = Path(path)
            print(self.path)
        #check given path
        try:
            with open(self.path, "r") as f:
                self.content = f.read()
        except FileNotFoundError:
            print("File was not dound in given path. try again\n")
            return


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

