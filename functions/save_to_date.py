import sqlite3
from datetime import datetime


def save_book(name):
    # 检查表是否已经存在
    check_table_exists_sql = (
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?;"
    )

    conn = sqlite3.connect("../book.db")
    c = conn.cursor()

    # 执行查询以检查表是否存在
    c.execute(check_table_exists_sql, (name,))
    table_exists = c.fetchone()

    if not table_exists:
        # 如果表不存在，则创建表
        create_table_sql = (
            f'CREATE TABLE "{name}" ('
            " id         INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,"
            " text       TEXT,"
            " note       TEXT,"
            " note_state TEXT,"
            " creat_time TEXT"
            ");"
        )
        c.execute(create_table_sql)
        print(f"Table '{name}' created successfully.")
    else:
        print(f"Table '{name}' already exists.")

    conn.commit()
    conn.close()


def insert_note(name, text, note):
    check_note_exists_sql = f"SELECT text FROM {name} WHERE text=? AND note=?;"
    sql = f"insert into {name} (text, note, note_state, creat_time) values (?, ?, ?, ?)"
    conn = sqlite3.connect("../book.db")
    c = conn.cursor()

    c.execute(check_note_exists_sql, (text, note))
    table_exists = c.fetchone()
    if not table_exists:
        c.execute(
            sql,
            (
                text,
                note,
                "no_send",
                str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            ),
        )
        conn.commit()
        print(f"{note} 插入成功")
    else:
        print("这个笔记已经记录过了。")
    conn.close()
