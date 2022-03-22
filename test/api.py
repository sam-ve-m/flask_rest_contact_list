import requests


class Api:
    def __init__(self, host: str):
        self.host = host

    def insert(self, index: int, first_letter: str, phones_amount: int = 1, first_dial: str = "22"):
        contact = {
            'firstName': f'{first_letter}-{index}-',
            'lastName': 'Dummy',
            'address': 'Dummy',
            'email': 'Dummy',
            'phoneList': [
                {
                    "type": "residential",
                    "number": "(11) 1111-1111"
                },
                {
                    "type": "mobile",
                    "number": f"({first_dial}) 1111-1111"
                },
                {
                    "type": "commercial",
                    "number": "(33) 1111-1111"
                }
            ][:phones_amount],
        }
        response = requests.post(self.host + "/register", json=contact)
        response_json = response.json()
        return response_json

    def update(self, _id: str):
        contact = {
            'lastName': 'Altered Dummy',
        }
        response = requests.put(self.host + "/edit/" + _id, json=contact)
        response_json = response.json()
        return response_json

    def delete(self, _id: str):
        response = requests.delete(self.host + "/remove/" + _id)
        response_json = response.json()
        return response_json

    def find_all(self):
        response = requests.get(self.host + "/contacts")
        response_json = response.json()
        return response_json

    def find_one(self, _id: str):
        response = requests.get(self.host + "/contact/" + _id)
        response_json = response.json()
        return response_json

    def find_by_letter(self, letter: str):
        response = requests.get(self.host + "/contacts/" + letter)
        response_json = response.json()
        return response_json

    def find_phones(self):
        response = requests.get(self.host + "/count")
        response_json = response.json()
        return response_json

