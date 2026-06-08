from fastapi import FastAPI
from pydantic import BaseModel, Field
import scan.scan as scan
import Config
import db.scan_db as scan_db
import threading
import codeReviewer.ollamaProvider as ollamaProvider
from codeReviewer import codeReviewer


running_scans = 0
resource_lock = threading.Lock()

def review(review_scan: scan.Scan, db: scan_db.ScanDB, config: Config.Config):
    #using locks to prevent rece conditions
    global running_scans
    
    try:
        print("Review started for scan:")

        provider = ollamaProvider.OllamaProvider(config)
        code_reviewer = codeReviewer.CodeReviewer(provider, config)

        results = {}
        for rule in review_scan.get_rules():
            results[rule] = code_reviewer.review(review_scan, rule)

        print("Review result:", results)
        review_scan.add_result(results)
        db.update_scan(review_scan)
        print("DB updated for scan:")

    finally:
        with resource_lock:
            running_scans -= 1
        

app = FastAPI(
    title="Automatic Code Review Platform",
    description="API for submitting Python code scans and fetching scan results."
)

db = scan_db.ScanDB()
config = Config.Config()
DB_PATH = "scans.db"

class ScanCreateRequest(BaseModel):

    file_name: str = Field(description="Name of the Python file being scanned")

    rules: list[str] = Field(default_factory=lambda: [
        "All variables have meaningful names",
        "docstring of function reflects the actual code logic"],
        description="List of rules to check against the code"
    )
    content: str = Field(description="The Python source code to scan")

    model_config = {
        "json_schema_extra": {
            "example": {
                "file_name": "hello.py",
                "rules": [
                    "Variable names should be meaningful",
                    "Do not use global variables",
                    "Functions should be short"
                ],
                "content": "def hello():\n    print(\"hello world\")"
            }
        }
    }







@app.post("/scans")
def create_scan(request: ScanCreateRequest):
    db.cleanup_if_needed(config)
    
    global running_scans
    with resource_lock:
        if running_scans >= config.max_parallel_scans:
            # maybe update DB to failed/rejected
            #raise HTTPException(status_code=429, detail="Maximum scans reached")
            return {"error": "Maximum scans reached"}
        running_scans+=1
    try:
        new_scan  = scan.Scan(request.file_name, request.rules, request.content)
        insert_result =  db.insert_new_scan(new_scan , config)
        
        if insert_result["created"] is False:
            with resource_lock:
                running_scans-=1
            return insert_result
            
        thread = threading.Thread(target=review, args=(new_scan, db, config))
        thread.start()

        return insert_result
    
    except Exception:
        with resource_lock:
            running_scans -= 1
        raise

@app.get("/scans/{scan_id}")
def get_scan(scan_id: int):
    db.cleanup_if_needed(config)
    return db.get_scan(scan_id, config)
