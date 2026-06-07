from fastapi import FastAPI
from pydantic import BaseModel, Field
import sqlite3
import hashlib
import scan.scan as scan
import Config
import db.scan_db as scan_db
import threading
import codeReviewer.ollamaProvider as ollamaProvider
import codeReviewer


running_scans = 0
resource_lock = threading.Lock()

def review(scan: scan.Scan, db: scan_db.ScanDB, config: Config.Config):
    #using locks to prevent rece conditions
    global running_scans
    
    try:
        provider = ollamaProvider.OllamaProvider(config)
        code_reviewer = codeReviewer.CodeReviewer(provider, config)
        result = code_reviewer.review(scan)
        scan.add_result(result)
        db.update_scan(scan)

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

    file_name: str = Field(
        description="Name of the Python file being scanned"
    )

    rules: list[str] = Field(default_factory=lambda: [
        "All variables have meaningful names",
        "docstring of function reflects the actual code’s logic"
    ],
        description="List of rules to check against the code"
    )
    content: str = Field(
        description="The Python source code to scan"
    )




@app.post("/scans")
def create_scan(request: ScanCreateRequest):
    scan = scan.Scan(request.file_name, request.rules, request.content)
    insert_result =  db.insert_new_scan(scan, config)
    
    if insert_result["created"] is False:
        return insert_result
        

    global running_scans
    with resource_lock:
        if running_scans >= config.max_parallel_scans:
            # maybe update DB to failed/rejected
            return {"error": "Maximum scans reached"}
        running_scans+=1

    thread = threading.Thread(target=review, args=(scan, db, config))
    thread.start()

    return insert_result

@app.get("/scans/{scan_id}")
def get_scan(scan_id: int):
    return db.get_scan(scan_id, config)
