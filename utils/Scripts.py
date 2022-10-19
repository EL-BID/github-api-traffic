import jwt
import time
import requests
import json


def CreateJWT():
    with open("utils/priv.pem") as f:
        private_pem = f.read()
        payload = {
            "iat": int(time.time()) - 60,
            "exp": int(time.time()) + (10 * 10),
            "iss": "250374"
        }
        return jwt.encode(payload, private_pem, algorithm="RS256")


def GetInstallations():
    headers = {
        "Authorization": "Bearer " + CreateJWT(),
        "Accept": "application/vnd.github+json"
    }
    r = requests.get("https://api.github.com/app/installations", headers=headers)
    return r.json()[0]["id"]


def GetAccessToken(installation_id):
    headers = {
        "Authorization": "Bearer " + CreateJWT(),
        "Accept": "application/vnd.github+json"
    }
    r = requests.post("https://api.github.com/app/installations/" + str(installation_id) + "/access_tokens", headers=headers)
    return r.text


def GetRepos():
    headers = {
        "Accept": "application/vnd.github+json"
    }
    r = requests.get("https://api.github.com/users/EL-BID/repos", headers=headers)
    return json.loads(r.text)


def GetTraffic(token):
    repos = GetRepos()
    results = []
    for repo in repos:
        headers = {
            "Authorization": "Bearer " + token,
            "Accept": "application/vnd.github+json"
        }
        r = requests.get("https://api.github.com/repos/EL-BID/"+repo["name"]+"/traffic/clones", headers=headers)
        results.append(json.loads(r.text))

    return results