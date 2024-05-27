import requests

def send_sms(phone, text):
    url = "https://direct.i-dgtl.ru/api/v1/message"
    header = {
        "Authorization": "Basic MzE5NTp3UXd3NHE2VmFPbHpjcFdKWDU0dHBI",
        "Content-Type": "application/json"
    }
    data = [
        {
            "channelType": "SMS",
            "senderName": "sms_promo",
            "destination": phone,
            "content": text,
            "ttl": 70
        }
    ]
    response = requests.post(url, json=data, headers=header)
    return response.status_code, response.json()


def validation_phone(phone, validation_code):#SMSPROMO
    return send_sms(phone, validation_code)

if __name__ == "__main__":
    print(validation_phone('79067316555', '5678'))