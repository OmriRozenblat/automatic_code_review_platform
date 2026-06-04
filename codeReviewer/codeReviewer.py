import ollama
import time

client = ollama.Client()

class CodeReviewer:
    

    def review(self):
        print("started working!\n")
        time.sleep(60)
        print("finished working!\n")
