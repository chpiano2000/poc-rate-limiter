class IPersistentStorage:
    def get_token(self):
        raise NotImplementedError

    def add_token(self, capacity: int):
        raise NotImplementedError
