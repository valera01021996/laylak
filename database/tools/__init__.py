from .product_tools import ProductTools
from .user_tools import UserTools
from .cart_tools import CartTools

class DBTools:
    def __init__(self):
        self.product_tools: ProductTools = ProductTools()
        self.user_tools: UserTools = UserTools()
        self.cart_tools: CartTools = CartTools()
