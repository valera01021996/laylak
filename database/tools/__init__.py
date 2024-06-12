from .product_tools import ProductTools
from .user_tools import UserTools

class DBTools:
    def __init__(self):
        self.product_tools: ProductTools = ProductTools()
        self.user_tools: UserTools = UserTools()
