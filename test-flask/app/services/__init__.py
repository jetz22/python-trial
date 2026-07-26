def calculate_sum(a, b):
    return a + b

def process_user_data(user_data):
    if not user_data:
        return {"error": "No data provided"}
    user_data['processed'] = True
    return user_data
