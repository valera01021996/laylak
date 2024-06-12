from .base_tools import BaseTools


class ProductTools(BaseTools):
    CATEGORIES = []
    PRODUCTS = []

    def get_categories(self, lang):
        self.cursor.execute(f"SELECT name_{lang} FROM categories")
        categories = []
        for category in self.cursor.fetchall():
            categories.append(*category)
        ProductTools.CATEGORIES = categories
        self.connection.close()
        return categories

    def get_category_id(self, category_name, lang):
        self.cursor.execute(f"""SELECT id
            FROM categories
            WHERE name_{lang} = ?
        """, (category_name,))
        category_id = self.cursor.fetchone()[0]
        self.connection.close()
        return category_id

    def get_products(self, category_id, lang):
        self.cursor.execute(f"SELECT name_{lang} FROM products WHERE category_id = ?",
                            (category_id,))
        products = []
        for product in self.cursor.fetchall():
            products.append(*product)
        ProductTools.PRODUCTS = products
        self.connection.close()
        return products

    def get_product_detail(self, product_name: str, lang):
        self.cursor.execute(f"""SELECT id, name_{lang}, price, image, ingredients_{lang}
            FROM products
            WHERE name_{lang} = ?
        """, (product_name, ))
        product = self.cursor.fetchone()
        self.connection.close()
        return product
