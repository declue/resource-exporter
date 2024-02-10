import os
import sqlite3
import sys

if __name__ == '__main__':

    if len(sys.argv) == 3:
        db_path = sys.argv[2]
    else:
        db_path = os.path.join(os.getcwd(), '.coverage')
        if not os.path.exists(db_path):
            print("Error: .coverage file not found in current directory, " + db_path)
            sys.exit(-1)

    print("db_path: " + db_path)
    if len(sys.argv) == 2 or len(sys.argv) == 3:
        TARGET_PATH = sys.argv[1]
        CURRENT_PATH = "$PROJECT_ROOT$"
    else:
        TARGET_PATH = "$PROJECT_ROOT$"
        CURRENT_PATH = os.getcwd()

    print("root_path: " + TARGET_PATH)
    print("current_path: " + CURRENT_PATH)

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT id, path FROM file")
    rows = cur.fetchall()

    for row in rows:
        original_path = row[1]

        if '\\' in CURRENT_PATH:
            converted_path = original_path.replace('/', '\\')
        else:
            converted_path = original_path

        new_path = converted_path.replace(CURRENT_PATH, TARGET_PATH)
        new_path = new_path.replace('\\', '/')
        print(f"{row[1]} => {new_path}")
        cur.execute("UPDATE file SET path = ? WHERE id = ?", (new_path, row[0]))
    conn.commit()
    conn.close()
