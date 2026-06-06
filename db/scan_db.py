import sqlite3
import hashlib

import scan.scan as scan
import Config



class ScanDB:

    def __init__(self):
    
        self.path = "scan_results.db"

        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT NOT NULL,
            rules_hash TEXT,
            content_hash TEXT,        
            rules TEXT NOT NULL,
            content TEXT NOT NULL,
            result TEXT,
            created_at TEXT NOT NULL 
        );
        """)

        conn.commit()
        conn.close()


    def insert_new_scan(self, scan: scan.Scan):
        conn = sqlite3.connect(self.path)
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
                return "exists", row["id"]


        cursor.execute("""
        INSERT INTO scans (
            file_name,
            rules,
            content_hash,
            rules_hash,
            content,
            created_at
        )
        VALUES (?, ?, ?, ?, ?,datetime('now'));
        """, (scan.file_name, scan.convert_rules_to_text(), content_hash, rules_hash,scan.get_content(),))

        scan_id = cursor.lastrowid
        scan.update_id(scan_id)

        conn.commit()
        conn.close()
        return "new", scan_id
                
    def update_scan(self, scan: scan.Scan):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE scans
        SET result = ?
        WHERE id = ?;
        """, (scan.get_result(), scan.get_id()))

        conn.commit()
        conn.close()

    def get_scan(self, scan_id: int, config_data: Config.Config):
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        

        cursor.execute(f""" DELETE FROM scans WHERE created_at < datetime('now', '-{config_data.scan_ttl_hours} hours')
                        AND id = ?; """,(scan_id,)) 
        
        cursor.execute(""" SELECT id, file_name, rules, result,
                        created_at FROM scans WHERE id = ?; """, (scan_id,))

        row = cursor.fetchone()

        conn.close()
        #may return None, depanding if row exist\expired
        return row
    
    def parse_row(self, row):
        if row is None:
            return "Scan not found or expired" 
            
        else:

            return (f"Scan ID: {row['id']}\n"
                    f"File name: {row['file_name']}\n"
                    f"Rules:\n{row['rules']}\n\n"
                    f"Result: {row['result']}\n"
                    f"Created at: {row['created_at']}\n"
                    )




