from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    hashedvalue = pwd_context.hash(password)
    return hashedvalue


def verify(original_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(original_password, hashed_password)