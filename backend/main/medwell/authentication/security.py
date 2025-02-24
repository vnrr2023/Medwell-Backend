from cryptography.fernet import Fernet
import jwt
import os
import environ
from urllib.parse import quote

env=environ.Env()
env_file_path=os.path.join('..', '.env')
environ.Env.read_env(env_file_path)
key=env('CRYPT_KEY')
JWT_SECRET=env("SECRET_KEY")
cipher_suite=Fernet(key)


def create_token(payload):
    token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
    encrypted_token = cipher_suite.encrypt(token.encode()).decode()
    return encrypted_token

def decrypt_token(enc_token):
    try:
        dec_token=cipher_suite.decrypt(enc_token.encode()).decode()
        payload = jwt.decode(dec_token, JWT_SECRET, algorithms=['HS256'])
        return {'payload':payload,'status':True}
    except:
        return {'status':False}
    
def give_enc_token(payload:dict):
    encrypted_token=quote(create_token(payload))
    return encrypted_token

def give_token_for_otp(payload:dict):
    token=create_token(payload)
    return token
    
def create_encrypted_json(data:str):
    # string=json.dumps(payload)
    enc_string=cipher_suite.encrypt(data.encode()).decode()
    return enc_string

def decrypt_json_string(enc_string:str):
    data=cipher_suite.decrypt(enc_string.encode()).decode()
    return data
