from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    hashedvalue = pwd_context.hash(password)
    return hashedvalue
    