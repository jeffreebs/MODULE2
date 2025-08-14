class Product:
    def __init__(self,id,name,price,stock):
        self.id = id
        self.name = name
        self.price = price
        self.stock= stock


    def to_dict(self):
        return{
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "stock": self.stock
        }
