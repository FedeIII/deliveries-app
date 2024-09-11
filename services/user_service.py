from .errors import BadRequestError


class UserService:
    def __init__(self, deps):
        self.deps = deps

    def register(self, username, password):
        if not username or not password:
            raise BadRequestError("Missing username or password")

        user = self.deps['User'].find_user(username)
        if user:
            raise BadRequestError(f"Username {username} already exists")
        self.deps['User'].create(username, password)
        return True

    def check_password(self, username, password):
        user = self.deps['User'].find_user(username)
        return user.check_password(password)
