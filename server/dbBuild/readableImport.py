import os
from DBConfig import conn, READABLE_PATH
from tqdm import tqdm

def importReadable():
    cursor = conn.cursor()
    sql = "insert or replace into readable(fileName, lang, content) values (?,?,?)"
    
    if not os.path.exists(READABLE_PATH):
        print(f"Readable path not found: {READABLE_PATH}")
        return

    langs = os.listdir(READABLE_PATH)
    for lang in langs:
        langPath = os.path.join(READABLE_PATH, lang)
        if not os.path.isdir(langPath):
            continue
            
        files = os.listdir(langPath)
        print(f"Importing readable for {lang}...")
        for fileName in tqdm(files):
            filePath = os.path.join(langPath, fileName)
            if not os.path.isfile(filePath):
                continue
                
            try:
                with open(filePath, 'r', encoding='utf-8') as f:
                    content = f.read()
                cursor.execute(sql, (fileName, lang, content))
            except Exception as e:
                print(f"Error reading {fileName}: {e}")
                
    cursor.close()
    conn.commit()
