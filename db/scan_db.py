import sqlite3

import scan.scan as scan



class ScanDB:

    def __init__(self):

        conn = sqlite3.connect("scan_results.db")
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


    def insert(self, scan: scan.Scan):
        conn = sqlite3.connect("scan_results.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO scans (
            file_name,
            rules,
            result,
            created_at
        )
        VALUES (?, ?, ?, datetime('now'));
        """, (scan.file_name, scan.convert_rules_to_text(), scan.get_result(), ))

        scan_id = cursor.lastrowid

        conn.commit()
        conn.close()
        return scan_id
                

    def get_scan(self, scan_id: int):
        pass

    def remove_scan(self, scan_id: int):
        pass


def insert_to_db(scan: scan.Scan):
    conn = sqlite3.connect("example.db")
    cursor = conn.cursor()

    pass