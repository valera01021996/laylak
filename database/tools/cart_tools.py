from database.tools.base_tools import BaseTools


class CartTools(BaseTools):
    def get_active_cart(self, user_id: int) -> tuple:
        self.cursor.execute("""SELECT *
            FROM carts
            WHERE user_id =?  AND in_order = 0
        """, (user_id,))
        cart: tuple = self.cursor.fetchone()
        self.connection.close()
        return cart

    def register_cart(self, user_id: int):
        # LBYL - Не зная броду, не лезь в воду
        if not self.get_active_cart(user_id):
            self._repeat_connection()
            self.cursor.execute("""INSERT INTO carts (user_id)
                VALUES (?)
            """, (user_id,))
            self.connection.commit()
            self.connection.close()

    def recalc_cart(self, cart_id: int):
        self.cursor.execute("""SELECT sum(quantity), SUM(total_coast)
            FROM cart_products
            WHERE cart_id = ?
        """, (cart_id,))
        total_price, total_amount = self.cursor.fetchone()
        self.cursor.execute("""UPDATE carts
            SET total_price = ?, total_amount = ?
            WHERE cart_id = ?
        """, (total_price, total_amount, cart_id))
        self.connection.commit()
        self.connection.close()

    def add_cart_product(self, cart_id: int, product_id: int, product_name: str, quantity: int, total_coast: float) \
            -> bool:
        status_add = False
        try:
            self.cursor.execute("""INSERT INTO cart_products
                (cart_id, product_id, product_name, quantity, total_coast)
                VALUES(?, ?, ?, ?, ?)
            """, (cart_id, product_id, product_name, quantity, total_coast))
        except:
            self.cursor.execute("""UPDATE cart_products
            SET quantity = ?, total_coast = ?
            WHERE product_id = ?
            """, (quantity, total_coast, product_id))
        else:
            status_add = True


        finally:
            self.connection.commit()
            self.connection.close()
            return status_add

    def get_cart_products(self, cart_id):
        self.cursor.execute(f"""SELECT product_id, product_name, quantity, total_coast
            FROM cart_products
            WHERE cart_id=?
        """, (cart_id,))
        cart_products = self.cursor.fetchall()
        self.connection.close()
        return cart_products

    def change_order_status(self, cart_id: int):
        self.cursor.execute("""UPDATE carts
            SET in_order = 1
            WHERE id = ?
        """, (cart_id,))
        self.connection.commit()
        self.connection.close()

    def get_cart_product(self, user_id: int):
        cart_id = self.get_active_cart(user_id)[0]
        self._repeat_connection()
        self.cursor.execute("""SELECT product_name
            FROM cart_products
            WHERE cart_id = ?
        """, (cart_id,))
        product_names = self.cursor.fetchall()
        self.connection.close()
        return product_names

    def delete_product_from_cart(self, product_name: str, cart_id: int):
        self.cursor.execute("""DELETE FROM cart_products
            WHERE product_name = ? and cart_id = ?
        """, (product_name, cart_id))
        self.connection.commit()
        self.connection.close()


    def delete_all_products_from_cart(self, cart_id: int):
        self.cursor.execute("""DELETE FROM cart_products
            WHERE cart_id = ?
            """, (cart_id,))
        self.connection.commit()
        self.connection.close()