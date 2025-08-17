import requests
from flask import Flask, render_template, abort


API_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjNlN2E2YjBjLTUzZWUtNDM0NC04OWQ0LTBiYWU4Y2NmZjQ3MSIsImlhdCI6MTc1NDgxMTk4Nywic3ViIjoiZGV2ZWxvcGVyL2ZjMDM5NjE1LTM5NjItNmNiNy1hMjAxLTY3YzgwZDBlZGYwZCIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyI1OC4xNTIuNDYuMjQ3Il0sInR5cGUiOiJjbGllbnQifV19.6OW010gg6c6A1y5JaSNfTWw_lXVGuEJ0i03IONZbSkRyVSQLyA-uiWwFjaHEp-mDFfhW7VdlEouWGAb7xKbGJA"

app = Flask(__name__)
app.jinja_env.globals.update(round=round)


@app.route("/players/<string:id>")
def get_data(id):
    # URL-encode the player ID to handle the '#' character

    url = f"https://api.clashroyale.com/v1/players/%23" + id
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