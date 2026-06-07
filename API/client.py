import requests
from pathlib import Path


API_URL = "http://127.0.0.1:8000/scans"

DEFAULT_RULES_PATH = Path(__file__).resolve().parent.parent / "scan" / "default_rules.txt"


def load_default_rules() -> list[str]:
    if not DEFAULT_RULES_PATH.exists():
        print("Default rules file not found:", DEFAULT_RULES_PATH)
        return []

    with open(DEFAULT_RULES_PATH, "r") as f:
        return [line.strip() for line in f if line.strip()]

def read_multiline(prompt: str, stop_word: str = "") -> str:
    print(prompt)
    print(f"Paste the full content below.")
    print(f"When finished, type {stop_word} on a new line and press Enter.")

    lines = []

    while True:
        line = input()
        if line == stop_word:
            break
        lines.append(line)

    return "\n".join(lines)

def main():


    while True: 
        user_input = input("Would you like to fetch results or enter a new scan?\n" "Enter scan for new scan, fetch for fetching results, q to quit  \n")
        
        if user_input == "scan":
            file_name = input("Enter file name: ").strip()
            
            while True:
                rules = load_default_rules()

                print("\nCurrent rules:")
                for i, rule in enumerate(rules, start=1):
                    print(f"{i}. {rule}")

                while True:
                    user_input2 = input("Enter 'a' to add a rule, 'r' to remove, Press Enter to continue:\n")
                    
                    if user_input2 == 'a':
                        new_rule = input("Enter a new rule: \n")
                        rules.append(new_rule)
                    
                    elif user_input2 == 'r':
                        remove_index = int(input("Enter rule index to remove: \n"))
                        try:
                            rules.pop(remove_index)
                        except IndexError:
                            print("Invalid index") ##########
                            break
                    
                    elif user_input2 == '':
                        #continue to scan
                        
                        content = read_multiline("Enter Python code content:")                    
                        
                        data=data = {
                            "file_name": file_name,
                            "rules": rules,
                            "content": content
                            }

                        response = requests.post(API_URL, json=data)

                        print("Response:")
                        print(response.json())
                        break
                    
                    elif user_input2 == "q":
                        return 0
                    
                    else:
                        print("Invalid input, try again\n")
        
        elif user_input == "fetch":

            scan_id = input("Enter scan_id: \n").strip()

            response = requests.get(f"{API_URL}/{scan_id}")

            print("Response:")
            print(response.json())
            break

            
        
        elif user_input == "q":
            return 0
        else:
            print("Not a valid input\n")



if __name__ == "__main__":
    main()