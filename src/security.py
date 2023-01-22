import bcrypt


def generate_password(password):
    password_bin = password.encode('utf-8')
    hashed = bcrypt.hashpw(password_bin, bcrypt.gensalt())
    return hashed.decode('utf-8')


def check_password(raw_password, password_hash):
    raw_password_bin = raw_password.encode('utf-8')
    password_bin = password_hash.encode('utf-8')
    is_correct = bcrypt.checkpw(raw_password_bin, password_bin)
    return is_correct
