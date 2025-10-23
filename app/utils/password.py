from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hash_password(password_plain:str) -> str:
    return pwd_context.hash(password_plain[:72])



def verify_password(password_plain:str,hash_password:str) -> bool:
    return pwd_context.verify(password_plain,hash_password)

