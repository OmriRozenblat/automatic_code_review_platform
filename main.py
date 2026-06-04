
import scan.scan as scan

import codeReviewer.codeReviewer as codeReviewer




def main():
    print("Welcome to the ACR!\n")
    while True: 
        user_input = input("Would you like to fetch results or enter a new scan?\n" \
        "Enter scan for new scan, results for fetching results, q to quit  \n")
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

                    #need to add the scan to some queue
                    code_reviewer = codeReviewer.CodeReviewer(current_scan)
                    print("Reviewing file!\n")
                    codeReviewer.review()

                    
                
                elif user_input2 == "q":
                    return 0
                
                else:
                    print("Invalid input, try again\n")
        
        elif user_input == "results":
            pass
        
        elif user_input == "q":
            return 0
        

main()