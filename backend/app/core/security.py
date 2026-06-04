from passlib.context import CryptContext


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password,
    )
    
def verify_api_key(
    raw_key: str,
    hashed_key: str,
) -> bool:

    return pwd_context.verify(
        raw_key,
        hashed_key,
    )