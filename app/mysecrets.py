from secrets import token_urlsafe

def generate_secret_key(length: int = 32) -> str:
    """
    Generates a secret token to be used for the JWT Authentication
    """
    return token_urlsafe(length)

# Example usage:
print(generate_secret_key())