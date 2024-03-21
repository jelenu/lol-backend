from rest_framework.views import APIView
from rest_framework.response import Response
import requests
import os
from dotenv import load_dotenv

load_dotenv()

class AccountInfo(APIView):
    def get(self, request):
        # Get queryset parameters from the frontend
        game_name = request.query_params.get('gameName', None)
        tagline = request.query_params.get('tagLine', None)

        # Check if gameName and tagline are present
        if not (game_name and tagline):
            return Response({'error': 'gameName and tagline are required'}, status=400)

        # Build the header
        headers = {
            'X-Riot-Token': os.getenv('TOKEN'),
        }

        # Make a call to the Riot API
        api_url = f'https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tagline}'
        response = requests.get(api_url, headers=headers)

        # Check if the API call was successful
        if response.status_code == 200:
            data = response.json()
            return Response(data)
        else:
            return Response({'error': 'Failed to fetch data from third-party API'}, status=response.status_code)
