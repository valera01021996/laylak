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