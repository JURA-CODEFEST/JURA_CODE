import secrets


class OTPgenerator:
    def generate_numeric_otp(length=6):
        # Restrict allowed characters strictly to digits
        digits = "0123456789"
        # Choose characters securely and join them
        random =  "".join(secrets.choice(digits) for _ in range(length))
        return random
    # # Example Usage
