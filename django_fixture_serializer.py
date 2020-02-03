import json


"""
Structure of JSON fixtures
[
    {"id": 1, "first_name": "Christie", "last_name": "Gann", "email": "cgann0@hostgator.com",
        "gender": "Female", "ip_address": "57.14.195.231"}, 
    {"id": 2, "first_name": "Hamil", "last_name": "Cressey", "email": "hcressey1@delicious.com",
        "gender": "Male", "ip_address": "45.225.25.145"}, ...
]

Fixtures files must match django serialization format, e.g:
[
    {
        "pk": "4b678b301dfd8a4e0dad910de3ae245b",
        "model": "sessions.session",
        "fields": {
            "expire_date": "2013-01-16T08:16:59.844Z",
            ...
        }
    }, ...
]

So we need to rewrite the fixtures in the following way:
- Add model key
- Add pk field
- Move the rest of fields to fields inner object

"""

USER_FIXTURE_PATH = 'users.json'
USER_STATISTIC_FIXTURE_PATH = 'users_statistic.json'

RESULT_USER_FIXTURE_PATH = 'serialized_user.json'
RESULT_USER_STATISTIC_FIXTURE_PATH = 'serialized_statistic_user.json'


# Serialize json for User model
with open(USER_FIXTURE_PATH, 'r') as json_file:
    # Result JSON data
    data = []

    json_file = json.loads(json_file.read())

    for obj in json_file:
        new_obj = {
            'pk': obj.get('id'),
            'model': 'core.User',
            'fields': obj
        }
        data.append(new_obj)

    # Writes serialized data into new json
    with open(RESULT_USER_FIXTURE_PATH, 'w') as result_json_file:
        print(RESULT_USER_FIXTURE_PATH)
        print('Serialized successfuly !!!')
        result_json_file.write(json.dumps(data))


# Serialize json for Statistic model
with open(USER_STATISTIC_FIXTURE_PATH, 'r') as json_file:
    # Result JSON data
    data = []

    json_file = json.loads(json_file.read())

    for pk, obj in enumerate(json_file, start=1):
        new_obj = {
            'pk': pk,
            'model': 'core.Statistic',
            'fields': obj
        }
        data.append(new_obj)

    # Writes serialized data into new json
    with open(RESULT_USER_STATISTIC_FIXTURE_PATH, 'w') as result_json_file:
        print(RESULT_USER_STATISTIC_FIXTURE_PATH)
        print('Serialized successfuly !!!')
        result_json_file.write(json.dumps(data))
