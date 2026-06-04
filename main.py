
import threading


import scan.scan as scan
import codeReviewer.codeReviewer as codeReviewer

running_scans = 0
resource_lock = threading.Lock()




def review(scan: scan.Scan, max_scans):
    global running_scans
    with resource_lock:
        if running_scans >= max_scans:
            print("Maximum scans reached. try again later")
            return
        running_scans+=1
    try:
        code_reviewer = codeReviewer.CodeReviewer()
        print("Reviewing file!\n")
        code_reviewer.review()

    finally:
        with resource_lock:
            running_scans -= 1



def get_scan():
    print("Welcome to the ACR!\n")
    while True: 
        user_input = input("Would you like to fetch results or enter a new scan?\n" "Enter scan for new scan, results for fetching results, q to quit  \n")
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
                    current_scan.get_file_from_path(path)

                    #call thread with this scan
                    thread = threading.Thread(target=review, args=(current_scan, 5))
                    thread.start()
                    break

                
                elif user_input2 == "q":
                    return 0
                
                else:
                    print("Invalid input, try again\n")
        
        elif user_input == "results":
            pass
        
        elif user_input == "q":
            return 0
        else:
            print("Not a valid input")
        

    
        
if __name__ == "__main__":
    get_scan()