import pandas as pd
import requests
import json

## Extração de dados
url = 'https://sdw-2023-prd.up.railway.app'
df = pd.read_csv('santander-etl.csv')
user_ids = df['UserID'].tolist()
print(user_ids)

def get_user(id):
    response = requests.get(f'{url}/users/{id}')
    return response.json() if response.status_code == 200 else None

users = [user for id in user_ids if (user := get_user(id)) is not None]
print(json.dumps(users, indent=2))
####

### Transformação
import openai
openai_key = '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'

openai.api_key = openai_key

def generate_ai_news(user):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é um engenheiro eletricista."},
            {"role": "user", "content": f"Crie uma mensagem para {user['name']} sobre a importância de usar os dispositivos de proteção nas instalações elétricas (máximo de 80 caracteres)"}
        ]
    )
    responseChatGPT = completion.choices[0].message.content.strip('\"')
    return responseChatGPT

for user in users:
    news = generate_ai_news(user)
    print(news)
    user['news'].append({'icon':'https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/pix.svg','description':news})
####


### Carregar os dados
def update_user(user):
    response = requests.put(f"{url}/users/{user['id']}", json=user)
    return True if response.status_code == 200 else False

for user in users:
    sucesso = update_user(user)
    print(f"O usuário {user['name']} update? {sucesso}!")
