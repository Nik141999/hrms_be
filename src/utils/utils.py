import uuid 
import random

def generate_uuid() -> str:
    return str(uuid.uuid4())


def generate_otp(length: int = 6) -> int:
    return random.randint(10**(length-1), 10**length - 1)

print(generate_otp())  