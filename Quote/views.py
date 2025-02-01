import requests


def get_quote():
    response = requests.get("https://qapi.vercel.app/api/random")
    data = response.json()
    return data