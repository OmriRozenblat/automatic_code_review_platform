

import threading


import scan.scan as scan
import codeReviewer.codeReviewer as codeReviewer
import codeReviewer.ollamaProvider as ollamaProvider
import db.scan_db as scan_db
import Config

running_scans = 0
resource_lock = threading.Lock()




def review(scan: scan.Scan, db: scan_db.ScanDB, config: Config.Config):
    global running_scans
    with resource_lock:
        if running_scans >= config.max_parallel_scans:
            print(f"Maximum scans reached ({config.max_parallel_scans}). try again later\n")
            return
        running_scans+=1
    try:
        provider = ollamaProvider.OllamaProvider(config.model_name)
        code_reviewer = codeReviewer.CodeReviewer(provider, config)
        result = code_reviewer.review(scan)
        print(result)
        scan.add_result(result)
        db.update_scan(scan)

    finally:
        with resource_lock:
            running_scans -= 1
        



def get_scan():

    print("Welcome to the ACR!\n")
    db = scan_db.ScanDB()
    config = Config.Config()

    while True: 
        user_input = input("Would you like to fetch results or enter a new scan?\n" "Enter scan for new scan, fetch for fetching results, q to quit  \n")
        if user_input == "scan":
            current_scan = scan.Scan()
            while True:
                current_scan.print_rules()
                user_input2 = input("Enter 'a' to add a rule, 'r' to remove, Press Enter to continue:\n")
                
                if user_input2 == 'a':
                    new_rule = input("Enter a new rule: \n")
                    current_scan.add_rule(new_rule)
                
                elif user_input2 == 'r':
                    remove_index = int(input("Enter rule index to remove: \n"))
                    current_scan.remove_rule(remove_index)
                
                elif user_input2 == '':
                    #continue to scan
                    #maybe just add it to folder and cancel the path part
                    path = input("Enter path to python file, or add it to the folder, then press Enter: \n")
                    
                    try:
                        current_scan.get_file_from_path(path)
                    except FileNotFoundError as e:
                        print(e)
                        break

                        

                    #adding scan to DB
                    status, scan_id = db.insert_new_scan(current_scan)
                    if status == "exists":
                        print(f"Scan already exists with scan_id {scan_id}")
                        break
                    print(f"Your new scan id is {scan_id}. Keep it for future use")

                    #call thread with this scan
                    thread = threading.Thread(target=review, args=(current_scan, db, config))
                    thread.start()
                    break

                
                elif user_input2 == "q":
                    return 0
                
                else:
                    print("Invalid input, try again\n")
        
        elif user_input == "fetch":
            fetch_scan_id = input(f"Please enter scan id: \n")
            row = db.get_scan(fetch_scan_id)
            print(db.parse_row(row))
        
        elif user_input == "q":
            return 0
        else:
            print("Not a valid input\n")
        

    
        
if __name__ == "__main__":
    get_scan()