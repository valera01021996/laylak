from database.tools.base_tools import BaseTools


class UserTools(BaseTools):
    def register_user(self, full_name:str, chat_id):
        try:
            self.cursor.execute("""INSERT INTO users(full_name, chat_id)
                VALUES(?, ?)
            """, (full_name, chat_id))
        except:
            pass
        else:
            self.connection.commit()
        finally:
            self.connection.close()


    def get_user_id(self, chat_id):
        self.cursor.execute("""SELECT id
            FROM users
            WHERE chat_id = ?
        """, (chat_id, ))
        user_id = self.cursor.fetchone()[0]
        self.connection.close()
        return user_id