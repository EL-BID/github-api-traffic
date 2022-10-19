from flask import Flask
from utils.Scripts import GetInstallations, GetAccessToken, GetTraffic
import json
app = Flask(__name__)


@app.route('/')
def API():
    installation = GetInstallations()
    access_token = GetAccessToken(installation)
    token = json.loads(access_token)["token"]
    return GetTraffic(token)


if __name__ == '__main__':
    app.run()
