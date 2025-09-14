import requests
from flask import Flask, render_template, abort
import os
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv("API_KEY")
app = Flask(__name__)
app.jinja_env.globals.update(round=round)


@app.route("/players/<string:id>")
def get_player_data(id):
    # URL-encode the player ID to handle the '#' character
    url = f"https://proxy.royaleapi.dev/v1/players/%23" + id
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {API_TOKEN}'
    }

    try:
        response = requests.get(url, headers=headers)
        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            return render_template("clash.html", player=data)
        elif response.status_code == 404:
            # Handle invalid player ID
            abort(404, description="Player not found")
        elif response.status_code == 403:
            # Handle authentication issues
            abort(403, description="Invalid API token or access denied")
        else:
            # Handle other errors
            abort(response.status_code, description=f"API request failed with status {response.status_code}")

    except requests.exceptions.RequestException as e:
        # Handle network or connection errors
        abort(500, description=f"Error connecting to the API: {str(e)}")


@app.route("/log/<string:id>")
def get_battle_data(id):
    url = f"https://proxy.royaleapi.dev/v1/players/%23{id}/battlelog"
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {API_TOKEN}'
    }

    try:
        response = requests.get(url, headers=headers)
        print(response.status_code)
        print(response.json())
        if response.json() != []:
            data = response.json()
            return render_template("battle_log.html", battles=data)
        else:
            abort(404, description="Battle log not found")


    except requests.exceptions.RequestException as e:
        abort(500, description=f"Error connecting to the API: {str(e)}")

@app.route("/clan/<string:id>")
def get_clan_data(id):
    url = f"https://proxy.royaleapi.dev/v1/clans/%23" + id
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {API_TOKEN}'
    }

    try:
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            return render_template("clan.html", player=data)
        elif response.status_code == 404:
            # Handle invalid player ID
            abort(404, description="Clan not found")
        elif response.status_code == 403:
            # Handle authentication issues
            abort(403, description="Invalid API token or access denied")
        else:
            # Handle other errors
            abort(response.status_code, description=f"API request failed with status {response.status_code}")

    except requests.exceptions.RequestException as e:
        # Handle network or connection errors
        abort(500, description=f"Error connecting to the API: {str(e)}")


@app.route("/")
def home():
    return render_template("home.html")
# Custom error handler for better user feedback
@app.errorhandler(404)
def not_found(error):
    return render_template("error.html", error=error), 404


@app.errorhandler(403)
def forbidden(error):
    return render_template("error.html", error=error), 403


@app.errorhandler(500)
def server_error(error):
    return render_template("error.html", error=error), 500


if __name__ == "__main__":
    app.run(debug=True)