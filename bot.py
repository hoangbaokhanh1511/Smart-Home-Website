import requests

bot_token = '7389121854:AAGqG9T89nZB9xgUu3ULhjIav0U4Nfm4gEQ'

def send(message):
    get_data = requests.get(f'https://api.telegram.org/bot{bot_token}/getUpdates').json()
    id = get_data['result'][0]['message']['chat']['id']
    url = f'https://api.telegram.org/bot7389121854:AAGqG9T89nZB9xgUu3ULhjIav0U4Nfm4gEQ/sendMessage'
    parameter = {
        'chat_id': id,
        'text': message
    }
    response = requests.post(url, data=parameter)
    response.close()