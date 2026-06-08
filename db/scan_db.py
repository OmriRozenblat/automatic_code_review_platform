import sqlite3
import hashlib
import json
from datetime import datetime, timedelta
import scan.scan as scan
import Config



class ScanDB:

    def __init__(self):
    
        self.path = "scan_results.db"

        conn = sqlite3.connect(self.path, timeout=10)
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS metadata (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );
    """)

        


        #create db if not exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            scan_id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT NOT NULL,
            rules_hash TEXT,
            content_hash TEXT,        
            rules TEXT NOT NULL,
            content TEXT NOT NULL,
            status TEXT NOT NULL,
            result TEXT,
            created_at TEXT NOT NULL 
        );
        """)

        conn.commit()
        conn.close()

    def cleanup_if_needed(self, config_data: Config.Config):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT value
            FROM metadata
            WHERE key = 'last_cleanup_at';
        """)

        row = cursor.fetchone()

        now = datetime.now()

        should_cleanup = False

        if row is None:
            should_cleanup = True
        else:
            last_cleanup = datetime.fromisoformat(row[0])
            if now - last_cleanup >= timedelta(minutes=config_data.delete_interval):
                should_cleanup = True

        if should_cleanup:
            cursor.execute("""
                DELETE FROM scans
                WHERE created_at < ?;
            """, ((now - timedelta(minutes=config_data.scan_ttl_minutes)).isoformat(),))
            
            cursor.execute("""
                INSERT OR REPLACE INTO metadata (key, value)
                VALUES ('last_cleanup_at', ?);
            """, (now.isoformat(),))

        conn.commit()
        conn.close()

    def insert_new_scan(self, scan: scan.Scan, config_data: Config.Config):
        conn = sqlite3.connect(self.path, timeout=10)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        hash_obj_rules = hashlib.sha256(scan.convert_rules_to_text().encode('utf-8'))
        hash_obj_content = hashlib.sha256(scan.get_content().encode('utf-8'))

        rules_hash = hash_obj_rules.hexdigest()
        content_hash = hash_obj_content.hexdigest()
        
        #check if db exists

        #check by hash to see if already exist in db
        query = "SELECT * FROM scans WHERE rules_hash == ? AND content_hash == ?"
        cursor.execute(query, (rules_hash, content_hash))

        results = cursor.fetchall()
        for row in results:
            if row['content'] == scan.content and row["rules"] == scan.convert_rules_to_text():
                #check if row is expired
                cursor.execute(f""" DELETE FROM scans WHERE created_at < datetime('now', '-{config_data.scan_ttl_minutes} minutes')
                        AND scan_id = ?; """,(row["scan_id"],))
                if cursor.rowcount > 0:
                    conn.commit()
                    continue


                conn.close()
                return {
                    "message": "Scan already exists",
                    "scan_id": row["scan_id"],
                    "created": False
                }


        cursor.execute("""
        INSERT INTO scans (
            file_name,
            rules,
            content_hash,
            rules_hash,
            content,
            status,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?,datetime('now'));
        """, (scan.file_name, scan.convert_rules_to_text(), content_hash, rules_hash, scan.get_content(),"running",))

        scan_id = cursor.lastrowid
        scan.update_id(scan_id)

        conn.commit()
        conn.close()
        return {
                    "message": "Scan submitted",
                    "scan_id": scan_id,
                    "created": True
        }
                
    def update_scan(self, scan: scan.Scan):
        conn = sqlite3.connect(self.path, timeout=10)
        cursor = conn.cursor()
        result_json = json.dumps(scan.get_result())

        cursor.execute("""
        UPDATE scans
        SET result = ?, status = ?
        WHERE scan_id = ?;
        """, (result_json, "done", scan.get_id()))

        conn.commit()
        conn.close()

    def get_scan(self, scan_id: int, config_data: Config.Config):
        conn = sqlite3.connect(self.path, timeout=10)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        

        cursor.execute(f""" DELETE FROM scans WHERE created_at < datetime('now', '-{config_data.scan_ttl_minutes} minutes')
                        AND scan_id = ?; """,(scan_id,)) 
        
        conn.commit()

        cursor.execute(""" SELECT scan_id, file_name, rules, result, status,
                        created_at FROM scans WHERE scan_id = ?; """, (scan_id,))

        row = cursor.fetchone()
        
        conn.commit()
        conn.close()
        #may return None, depanding if row exist\expired
        if row is None:
            return {"error": "Scan not found"}

        return {
            "scan_id": row["scan_id"],
            "file_name": row["file_name"],
            "status": row["status"],
            "result": json.loads(row["result"]) if row["result"] is not None else None,
            "created_at": row["created_at"]
            }
    
    def parse_row(self, row):
        if row is None:
            return "Scan not found or expired" 
            
        else:

            return ("\n--------------------------"
                    f"\nScan ID: {row['scan_id']}\n\n"
                    f"File name: {row['file_name']}\n\n"
                    f"Rules:\n{row['rules']}\n\n"
                    f"Results:\n{row['result']}\n\n"
                    f"Created at: {row['created_at']}\n"
                    "--------------------------\n"
                    )




