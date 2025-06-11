from faker import Faker
import uuid

fake = Faker()

def generate_user_body():
    unique_login = str(uuid.uuid4())
    return {
        "email":fake.unique.email(),
        "password":fake.password(),
        "name":f"user_{unique_login}"
    }

def generate_fake_new_email():
    fake_new_email = fake.unique.email()
    return fake_new_email

def generate_user_body_with_fake_params(param, user_data):
    data = {'email': user_data['email'],
            'name': user_data['name']
    }
    if param == 'both':
        data['email'] = fake.unique.email()
        data['name'] = fake.unique.word()
    elif param == 'email':
        data['email'] = fake.unique.email()
    elif param == 'name':
        data['name'] = fake.unique.word()
    return data

def generate_user_body_with_empty_params(param, user_data):
    data = {'email': user_data['email'],
            'password': user_data['password']
    }
    if param == 'both':
        data['email'] = ''
        data['password'] = ''
    elif param == 'email':
        data['email'] = ''
    elif param == 'password':
        data['password'] = ''
    return data

def create_user_body_without_fields(missing_fields, user_data):
    data = {'email': user_data['email'],
            'password': user_data['password'],
            'name': user_data['name']
    }
    for field in missing_fields:
        if field in data:
            del data[field]
    return data

def login_user_body_without_fields(missing_fields, user_data):
    data = {'email': user_data['email'],
            'password': user_data['password']
    }
    for field in missing_fields:
        if field in data:
            del data[field]
    return data

