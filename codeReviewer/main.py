




def main():
    res = ""
    while res not in  ["scan", "results"]: 
        res = input("would you like to fetch results or enter a new scan?\n" \
        "enter scan for new scan, esults for fetching results or q to quit  \n")
        if res == "scan":
            pass
        elif res == "results":
            pass
        elif res == "q":
            return 0
        

main()