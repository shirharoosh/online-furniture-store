class User:
    def __init__(self, username: str, email: str, password: str, address: str):
        self.username = username
        self.email = email
        self.password = password
        self.address = address
        self.orders = []

    def sign_up(self):
        pass

    def login(self):
        pass