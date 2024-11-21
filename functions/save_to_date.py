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
            return "have_note"

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

    def rm_note(self, text, note):
        print("我要发一些东西", text, note)
        sql_rm_note = f"delete from {self.form_name} where text=? and note=?"

        self.c.execute(sql_rm_note, (text, note))
        self.conn.commit()

    def update_note(
        self, old_text=None, old_note=None, new_text=None, new_note=None, state=None
    ):

        if new_text is None:
            new_text = old_text
        if new_note is None:
            new_note = old_note
        if state is None:
            state = "no_send"
        sql_update_note = (
            f"update {self.form_name} set text=?,note=?,note_state=?"
            f"where text=? and note=?"
        )
        print(old_text, old_note)
        self.c.execute(sql_update_note, (new_text, new_note, state, old_text, old_note))
        self.conn.commit()

    def get_settings(self):
        sql_get_last_ip = "select * from settings"
        # [('last_ip', '192.168.1.12'), ('author_info', 'true')]
        settings = self.c.execute(sql_get_last_ip).fetchall()
        return settings

    def save_ip(self, new_ip):
        sql_save_ip = (
            f"update settings set setting_value=? where setting_name='last_ip'"
        )

        self.c.execute(sql_save_ip, (str(new_ip),))
        self.conn.commit()

    def update_settings(self, new_ip=None, author_info=None, submit_state=None):
        if new_ip:
            sql = f"update settings set setting_value=? where setting_name='last_ip'"
            parameters = new_ip

        elif author_info:
            sql = (
                f"update settings set setting_value=? where setting_name='author_info'"
            )
            parameters = author_info
        elif submit_state:
            sql = (
                f"update settings set setting_value=? where setting_name='submit_state'"
            )
            parameters = submit_state
        else:
            return
        self.c.execute(sql, (parameters,))
        self.conn.commit()
