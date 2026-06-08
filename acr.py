import requests
from pathlib import Path
import argparse
import os
from Config import Config

config = Config()

API_BASE_URL = os.getenv("ACR_API_BASE_URL", config.API_BASE_URL)

DEFAULT_RULES_PATH = Path(__file__).resolve().parent / "scan" / "default_rules.txt"



def load_default_rules() -> list[str]:
    if not DEFAULT_RULES_PATH.exists():
        print("Default rules file not found:", DEFAULT_RULES_PATH)
        return []

    with open(DEFAULT_RULES_PATH, "r") as f:
        return [line.strip() for line in f if line.strip()]

def parse_generic(data):

    print("\n--------------")

    if "error" in data:
        print(data["error"])
        print("--------------\n")
        return

    if "message" in data:
        print(data["message"])

    if "scan_id" in data:
        print(f"Scan ID: {data['scan_id']}")

    if "file_name" in data:
        print(f"File name: {data['file_name']}")

    if "status" in data:
        print(f"Status: {data['status']}")

    if "result" in data and data["result"] is not None:
        print("\nResults:")
        for rule, passed in data["result"].items():
            print(f"- {rule}: {passed}")
    print("--------------\n")


def read_file(path: str):
    if not path:
        folder = Path(__file__).resolve().parent / "file_to_scan"
        file_path = next(folder.glob("*.py"), None)

        if file_path is None:
            raise FileNotFoundError("No .py file found in file_to_scan")
    else:
        file_path = Path(path.strip().strip('"'))

    try:
        content = file_path.read_text(encoding="utf-8")
        file_name = file_path.name
        return file_name, content

    except FileNotFoundError:
        raise FileNotFoundError("Can't find file in path.")


def main():
    parser = argparse.ArgumentParser(
        description="Automatic Code Review Platform"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    scan_parser = subparsers.add_parser(
        "scan",
        help="Submit a Python file for code review"
    )

    scan_parser.add_argument(
        "--path",
        required=False,
        default=None,
        help="Path to Python file. If not given, first .py file from file_to_scan is used."
    )

    scan_parser.add_argument(
    "--add-rules",
    nargs="+",
    default=[],
    help="Add extra rules for this scan only. Write each rule inside quotes."
)


    results_parser = subparsers.add_parser(
        "fetch",
        help="Fetch scan results by scan id"
    )

    results_parser.add_argument(
        "--id",
        required=True,
        type=int,
        help="Scan id returned from the scan command"
    )


    args = parser.parse_args()

    if args.command == "scan":
        try:
            file_name, content = read_file(args.path)
        except FileNotFoundError as e:
            print(e)
            return
        
        rules = load_default_rules()
        rules.extend(args.add_rules)
        
        data = {
            "file_name": file_name,
            "rules": rules,
            "content": content
            }
        response = requests.post(f"{API_BASE_URL}/scans", json=data)
        parse_generic(response.json())

    elif args.command == "fetch":
        response = requests.get(f"{API_BASE_URL}/scans/{args.id}")
        parse_generic(response.json())



    return

    


if __name__ == "__main__":
    main()



































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



def parse_json_result(data):

    print(f"\nScan ID: {data['id']}")
    print(f"File name: {data['file_name']}")
    print(f"Status: {data['status']}")
    print(f"Created at: {data['created_at']}")

    print("\nResults:")
    if data["result"]:
        for rule, passed in data["result"].items():
            print(f"- {rule}: {passed}")
    else:
        print("No results yet.")




def hello():
    


    while True: 
        user_input = input("Would you like to fetch results or enter a new scan?\n" "Enter scan for new scan, fetch for fetching results, q to quit  \n")
        
        if user_input == "scan":
            
            rules = load_default_rules()
            while True:
                
                print("\nCurrent rules:")
                for i, rule in enumerate(rules, start=1):
                    print(f"{i}. {rule}")

                user_input2 = input("Enter 'a' to add a rule, 'r' to remove, Press Enter to continue:\n")
                
                if user_input2 == 'a':
                    new_rule = input("Enter a new rule: \n")
                    rules.append(new_rule)
                
                elif user_input2 == 'r':
                    remove_index = int(input("Enter rule index to remove: \n"))
                    try:
                        rules.pop(remove_index)
                    except IndexError:
                        print("Invalid index\n") ##########
                        
                
                elif user_input2 == '':
                    #continue to scan
                    path = input("Enter path to python file, or add it to the folder, then press Enter: \n")
                    try:
                        file_name, content = read_file(path)
                    except FileNotFoundError as e:
                        print(e)
                        break
                    data = {
                        "file_name": file_name,
                        "rules": rules,
                        "content": content
                        }

                    response = requests.post(API_URL, json=data)
                    print("Status code:", response.status_code)
                    print("Raw response:", response.text)
                    parse_generic(response.json())
                    break
                
                elif user_input2 == "q":
                    return 0
                
                else:
                    print("Invalid input, try again\n")
    
        elif user_input == "fetch":

            scan_id = input("Enter scan_id: \n").strip()

            response = requests.get(f"{API_URL}/{scan_id}")

            parse_json_result(response.json())
            

            
        
        elif user_input == "q":
            return 0
        else:
            print("Not a valid input\n")



