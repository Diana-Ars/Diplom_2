class Data:
    empty_param = ''
    fake_param = 'fake_value'
    fix_email = 'fix_email@email.com'

    fix_order_body = {
        'ingredients': ['61c0c5a71d1f82001bdaaa6d','61c0c5a71d1f82001bdaaa6f']
    }

    empty_order_body = {}
    empty_order_body_list = {
        'ingredients': []
    }
    fake_hash_order_body = {'ingredients': ['6666666666666aaaaaaaaa']}

    error_message_create_user = 'Email, password and name are required fields'
    error_message_double_user = 'User already exists'
    error_message_not_auth = 'You should be authorised'
    error_message_login = 'email or password are incorrect'
    error_message_create_order = 'Ingredient ids must be provided'
    error_message_double_email = 'User with such email already exists'