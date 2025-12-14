class Bill:
    def __init__(self,id,user_id,products,total):
        self.id= id
        self.user_id= user_id
        self.products = products
        self.total= total


    def to_dict(self):
        return{
            "id": self.id,
            "user_id":self.user_id,
            "products": self.products,
            "total": self.total
        }