from datetime import datetime

from .base_tools import BaseTools


class OrderTools(BaseTools):
    def create_order(self, cart_id: int):
        create_date = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self.cursor.execute("""INSERT INTO orders (cart_id, create_date)
            VALUES(?, ?)
        """, (cart_id, create_date))
        self.connection.commit()
        self.connection.close()

    def change_order_status(self, cart_id: int):
        self.cursor.execute("""UPDATE carts
            SET in_order = 1
            WHERE id = ?
        """, (cart_id, ))
        self.connection.commit()
        self.connection.close()
