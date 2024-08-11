"""file holds utily functions"""
from passlib.context import CryptContext

#hashing algorithm for hashing passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

#hash plain_pass then compare with hashed_pass stored in database
def verify(plain_pass, hashed_pass):
    return pwd_context.verify(plain_pass, hashed_pass)