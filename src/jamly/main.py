"""Main application entrypoint."""

from uuid import uuid4

from flask import Flask, redirect, request, session, url_for

from jamly.auth import _get_auth, get_client, set_access_token

app = Flask(__name__)
app.secret_key = str(uuid4())


@app.route("/")
def index():
    if not session.get("token_info"):
        sp_oauth = _get_auth()
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    return "Welcome!"


@app.route("/callback")
def callback():
    set_access_token(request.args.get("code"))
    return redirect(url_for("index"))


@app.route("/playlists")
def playlists():
    client = get_client()
    if client is None:
        return redirect(url_for("index"))

    user_playlists = client.current_user_playlists()
    return f"Your playlists: {user_playlists}"


if __name__ == "__main__":
    app.run(debug=True)
