import sqlite3

import scan.scan as scan



class ScanDB:

    def __init__(self):
    
        self.path = "scan_results.db"

        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT NOT NULL,
            rules TEXT NOT NULL,
            result TEXT,
            created_at TEXT NOT NULL 
        );
        """)

        conn.commit()
        conn.close()


    def insert_new_scan(self, scan: scan.Scan):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO scans (
            file_name,
            rules,
            created_at
        )
        VALUES (?, ?, datetime('now'));
        """, (scan.file_name, scan.convert_rules_to_text(), ))

        scan_id = cursor.lastrowid

        conn.commit()
        conn.close()
        return scan_id
                
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

    def get_scan(self, scan_id: int):
        conn = sqlite3.connect(self.path)
        cursor = conn.cursor()

        

        cursor.execute(""" DELETE FROM scans WHERE created_at < datetime('now', '-24 hours')
                        AND id = ?; """,(scan_id,)) 
        
        cursor.execute(""" SELECT id, file_name, result,
                        created_at FROM scans WHERE id = ?; """, (scan_id,))

        row = cursor.fetchone()

        conn.close()
        #may return None, depanding if row exist\expired
        return row



