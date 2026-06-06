from pathlib import Path



class Scan:
    def __init__(self):
        default_rules_path = Path(__file__).parent / "default_rules.txt"
        with open(default_rules_path, 'r') as f:
            self.rules = f.read().splitlines() 
        self.id = 0
    
    def get_file_from_path(self, path: str):
        if not path:
            folder = Path(__file__).parent.parent / "file_to_scan"
            self.path = next(folder.glob("*.*"), None)
            print(self.path)
            if self.path is None:
                raise FileNotFoundError("No .py file found in file_to_scan")
        else:
            path = path.strip('"')
            self.path = Path(path)
            print(self.path)
        #check given path
        self.file_name = self.path.name
        try:
            with open(self.path, "r") as f:
                self.content = f.read()
        except FileNotFoundError:
            print("File was not dound in given path. try again\n")
            return


    def get_rules(self):
        return self.rules
    
    def convert_rules_to_text(self):
        rules_text = "\n".join(
            f"{index + 1}. {rule}"
            for index, rule in enumerate(self.get_rules())
        )
        return rules_text
    
    def get_content(self):
        return self.content

    def get_id(self):
        return self.id

    def update_id(self, id):
        self.id = id
    
    def get_file_path(self):
        return self.path
    
    def add_rule(self, rule: str):
        self.rules.append(rule)
        print("Rule added to scan\n")

    def add_result(self, result: str):
        self.result = result

    def get_result(self):
        return self.result
    
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

