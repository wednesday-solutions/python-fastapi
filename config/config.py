from dotenv import load_dotenv
import os

def get_secret_key():
    load_dotenv()
    secret_key = os.getenv("YOUR_SECRET_KEY")
    
    if secret_key is None:
        raise EnvironmentError("Secret Key not found. Ensure YOUR_SECRET_KEY is set in the .env file.")
    
    return secret_key