import requests
import random

BASE_URL = "http://127.0.0.1:5000"

user_data = {"username": "joey_test", "password": "123456"}
res_register = requests.post(f"{BASE_URL}/users/register", json=user_data)
print("POST /users/register →", res_register.status_code, res_register.json())

res_login = requests.post(f"{BASE_URL}/users/login", json=user_data)
login_json = res_login.json()
token = login_json.get("token")
print("POST /users/login →", res_login.status_code, login_json)

headers = {"Authorization": f"Bearer {token}"}

players = requests.get(f"{BASE_URL}/players/").json()
games = requests.get(f"{BASE_URL}/games/").json()

games_to_vote = games[:4]

for game in games_to_vote:
    player = random.choice(players)
    vote_data = {"game_id": int(game["id"]), "player_id": int(player["id"])}
    res_vote = requests.post(f"{BASE_URL}/votes/", json=vote_data, headers=headers)
    if res_vote.status_code == 201:
        print(f"Voted for {player['first_name']} {player['last_name']} in game {game['id']}")
    else:
        print(f"Impossible de voter pour {player['first_name']} {player['last_name']} in game {game['id']} → {res_vote.status_code} {res_vote.json()}")


res_top = requests.get(f"{BASE_URL}/votes/top")
if res_top.status_code == 200:
    print("Top players:", res_top.json())
else:
    print("Aucun vote enregistré ou erreur :", res_top.json())