import secrets
import string

class API_generator:
    # Google bata copy gareko yo
    @staticmethod
    def generate_secure_string(length):
        # changed the last part for easy typing
        characters = string.ascii_uppercase + string.digits
        random_part = ''.join(secrets.choice(characters) for _ in range(length))

        api = f"SOS-{random_part}"
        return api
    # # print(f"SOS-{generate_secure_string(16)}")
    # a = generate_secure_string(16)
    # print(a)
    # print(len(a))