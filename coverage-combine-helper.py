import os
import sqlite3
import re

# 현재 작업 디렉토리 경로를 동적으로 얻음
current_path = os.getcwd()

# .coverage 파일 경로
db_path = os.path.join(current_path, '.coverage')

# 데이터베이스 연결
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# file 테이블의 모든 path 레코드를 검색
cur.execute("SELECT id, path FROM file")
rows = cur.fetchall()

for row in rows:
    original_path = row[1]

    # 윈도우 경로 스타일을 리눅스 스타일로 변환 (예: C:\runner\work -> /runner/work)
    converted_path = re.sub(r'^[a-zA-Z]:\\', '/', original_path.replace('\\', '/'))

    # 동적으로 얻은 현재 경로를 제거
    # 예: '/home/runner/work/resource-exporter/resource-exporter/'에서
    # '/home/runner/work' 부분을 제거
    new_path = converted_path.replace(current_path, '')

    # 윈도우 스타일 경로일 경우 추가 처리
    if original_path.startswith('C:'):
        # 윈도우 경로의 경우, 절대 경로 앞에 추가적인 '/'가 필요 없음
        new_path = new_path.lstrip('/')

    # 경로 업데이트
    cur.execute("UPDATE file SET path = ? WHERE id = ?", (new_path, row[0]))

# 변경 사항 저장
conn.commit()

# 데이터베이스 연결 닫기
conn.close()