import os
import sqlite3
import re
import sys

if __name__ == '__main__':

    if len(sys.argv) == 3:
        db_path = sys.argv[2]
    else:
        db_path = os.path.join(os.getcwd(), '.coverage')
        if not os.path.exists(db_path):
            print("Error: .coverage file not found in current directory, " + db_path)
            sys.exit(-1)

    if len(sys.argv) == 2:
        root_path = sys.argv[1]
        current_path = "$PROJECT_ROOT$"
    else:
        root_path = "$PROJECT_ROOT$"
        current_path = os.getcwd()


    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT id, path FROM file")
    rows = cur.fetchall()

    for row in rows:
        original_path = row[1]
        converted_path = re.sub(r'^[a-zA-Z]:\\', '/', original_path.replace('\\', '/'))
        new_path = converted_path.replace(current_path, root_path)
        if '\\' in original_path:
            new_path = new_path.lstrip('/')
        cur.execute("UPDATE file SET path = ? WHERE id = ?", (new_path, row[0]))
    conn.commit()
    conn.close()
