class Info(object):
    def __init__(self):
        self.login_valid = False
        self.id = None
        self.mode = 'seller'
        return

    def update(self, login_valid, id):
        self.login_valid = login_valid
        self.id = id
        return

    def get_mode(self, mode):
        self.mode = mode
        return
