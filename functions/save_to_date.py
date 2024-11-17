import sqlite3
from datetime import datetime


class ReadAndWriteDate:
    def __init__(self):
        self.form_name = None
        self.conn = sqlite3.connect("book.db")
        self.c = self.conn.cursor()

    def save_book(
        self,
        name,
        author="",
        translator="",
        publisher="",
        isbn="",
        book_introduction="",
    ):
        """

        :param name:
        :param author:
        :param translator:
        :param publisher:
        :param isbn:
        :param book_introduction: 书籍简介
        :return:
        """
        # 检查表是否已经存在
        check_table_exists_sql = "SELECT book_name FROM book_list WHERE book_name=?;"

        update_book_list_sql = f"insert into book_list (book_name, ct, author, translator, publisher, isbn, book_introduction) values (?,?, ?,?,?,?,?)"
        c = self.conn.cursor()

        # 执行查询以检查表是否存在
        c.execute(check_table_exists_sql, (name,))
        table_exists = c.fetchone()

        if not table_exists:
            # 如果表不存在，则在book_list创建这本书，查找其id作为表名的一部分，创建表
            c.execute(
                update_book_list_sql,
                (
                    name,
                    str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                    author,
                    translator,
                    publisher,
                    isbn,
                    book_introduction,
                ),
            )
            self.conn.commit()
            sql_select_book_form_name = "select id from book_list where book_name=?"
            c.execute(sql_select_book_form_name, (name,))
            book_id = c.fetchone()
            create_table_sql = (
                f'CREATE TABLE "{'book_form_' + str(book_id[0])}" ('
                " id         INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,"
                " text       TEXT,"
                " note       TEXT,"
                " note_state TEXT,"
                " create_time TEXT"
                ");"
            )
            c.execute(create_table_sql)
            self.conn.commit()

            print(f"Table '{name}' created successfully.")
        else:
            print(f"Table '{name}' already exists.")

    def insert_note(self, text, note, note_state=False):
        """

        :param name:
        :param text:
        :param note:
        :param note_state:
        :return:
        """
        if note_state:
            note_state = "have_send"
        else:
            note_state = "no_send"
        print(self.form_name)
        check_note_exists_sql = (
            f"SELECT text FROM {self.form_name} WHERE text=? AND note=?;"
        )
        sql = f"insert into {self.form_name} (text, note, note_state, create_time) values (?, ?, ?, ?)"
        c = self.conn.cursor()

        c.execute(check_note_exists_sql, (text, note))
        table_exists = c.fetchone()
        if not table_exists:
            c.execute(
                sql,
                (
                    text,
                    note,
                    note_state,
                    str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                ),
            )
            self.conn.commit()
            print(f"{note} 插入成功")
        else:
            print("这个笔记已经记录过了。")

    def get_note_list(self):
        sql_select_note = f"SELECT * FROM {self.form_name}"
        c = self.conn.cursor()
        c.execute(sql_select_note)
        note_list = c.fetchall()
        return note_list

    def get_book_id(self, book_name):
        c = self.conn.cursor()
        sql_get_id = "select id from book_list where book_name=?"
        c.execute(sql_get_id, (book_name,))
        book_id = c.fetchall()[0]
        self.form_name = "book_form_" + str(book_id[0])

    def get_notes(self):
        sql_get_id = f"select * from {self.form_name} where note_state=?"

        self.c.execute(sql_get_id, ("no_send",))
        notes = self.c.fetchall()
        print(notes)
        # [(1, 'xn的测试', '', 'no_send', '2024-11-17 21:30:00'), (2, '', '', 'no_send', '2024-11-17 21:32:46')]

        return notes
