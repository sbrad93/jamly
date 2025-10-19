import os
from typing import Any, Optional

from dotenv import load_dotenv
from flask import session
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

from jamly.constants import SCOPE


def _get_auth() -> SpotifyOAuth:
    """Get the SpotifyOAuth object.

    Returns
    -------
    SpotifyOAuth
        The authorization object.
    """
    load_dotenv()
    CLIENT_ID = os.environ["CLI_ID"]
    CLIENT_SECRET = os.environ["CLI_SECRET"]
    REDIRECT_URI = os.environ["REDIRECT_URI"]
    return SpotifyOAuth(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, scope=SCOPE)


def _get_token_info() -> Any:
    """Get session token info.

    Returns
    -------
    Any
        The token or None if there is no active token.
    """
    return session.get("token_info")


def set_access_token(code: Optional[str] = None) -> Any:
    """Set session access token.

    Parameters
    ----------
    code : str, optional
        The response code.

    Returns
    -------
    Any
        The access token or None if there is no active access token.
    """
    sp_oauth = _get_auth()
    token_info = sp_oauth.get_access_token(code)
    session["token_info"] = token_info
    return token_info


def get_client() -> Optional[Spotify]:
    """Get the Spotify API client.

    Returns
    -------
    Spotify
        The client or None if user is not authenticated.
    """
    token_info = _get_token_info()
    if token_info is None:
        return None
    return Spotify(auth=token_info["access_token"])
