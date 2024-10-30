from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=['bcrypt'], deprecated="auto")


class Hash():
    @staticmethod
    def bcrypt(password: str):
        hashed_password = pwd_cxt.hash(password)
        return hashed_password

    def verify(hashed_password_from_db: str, password: str):
        return pwd_cxt.verify(password, hashed_password_from_db)
