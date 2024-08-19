import bcrypt

salt = bcrypt.gensalt(rounds=12)

def encrypt(plain_text: str):
    encoded_text = plain_text.encode('utf-8')
    return bcrypt.hashpw(encoded_text, salt).decode('utf-8')

def match_values(plain_text:str, to_be_matched_text:str):
    encoded_text = plain_text.encode('utf-8')
    hashed_text = to_be_matched_text.encode('utf-8')
    return bcrypt.checkpw(encoded_text, hashed_text)