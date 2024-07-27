import os
import requests
from fastapi import HTTPException, status, Request
from music_service.music_service import MusicService
from tokens.token import Token
from tokens.deezer_token import DeezerToken

class DeezerService(MusicService):
    def __init__(self):
        super().__init__(
        	auth_url=f'https://connect.deezer.com/oauth/auth.php?app_id={os.getenv("DEEZER_APP_ID")}&redirect_uri={os.getenv("DEEZER_CALLBACK_URL")}&perms={os.getenv("DEEZER_PERMS")}',
        	token_url=f'https://connect.deezer.com/oauth/access_token.php?app_id={os.getenv("DEEZER_APP_ID")}&secret={os.getenv("DEEZER_SECRET_KEY")}&output=json',
        	base_url='https://api.deezer.com'
        )
        self.token: DeezerToken | None = None

    def callback(self, request: Request) -> Token:
        code : str | None = request.query_params.get('code')
        if code is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='no code found')
        self.token_url += f'&code={code}'
        response = requests.get(self.token_url)
        if response.status_code != status.HTTP_200_OK:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        self.token = DeezerToken(**(response.json()))
        return self.token

    def get_user(self, endpoint: str):
        if self.token is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="token not set")
        endpoint += f'?access_token={self.token.access_token}'
        response = requests.get(self.base_url + endpoint)
        if response.status_code != status.HTTP_200_OK:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()['name']
