import os
import json
import random
import datetime

from faker import Faker

fake = Faker()


def generate_json(num_fields=1000, max_nested_depth=2):
    data = {}
    for i in range(num_fields):
        field_name = f"field_{i}"
        data[field_name] = generate_value(max_nested_depth)
    return json.dumps(data, indent=2)


def generate_value(max_depth):
    if max_depth == 0:
        return random_simple_value()

    if random.random() < 0.3 and max_depth > 0:
        return generate_json(random.randint(10, 100), max_depth - 1)
    else:
        return random_simple_value()


def random_simple_value():
    value_type = random.choice(['int', 'float', 'str', 'bool', 'date'])
    if value_type == 'int':
        return random.randint(-1000, 1000)
    elif value_type == 'float':
        return random.uniform(-1000, 1000)
    elif value_type == 'str':
        return fake.text(max_nb_chars=50)
    elif value_type == 'bool':
        return random.choice([True, False])
    elif value_type == 'date':
        date_obj = datetime.datetime.strptime(fake.date(), '%Y-%m-%d').date()
        return date_obj.isoformat()


os.makedirs("./test_jsons", exist_ok=True)

json_data = generate_json(num_fields=100000, max_nested_depth=1)

with open('./test_jsons/test_json_3.json', 'w', encoding='utf-8') as f:
    f.write(json_data)

print("Large JSON data generated successfully!")
