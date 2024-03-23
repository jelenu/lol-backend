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
        server = request.query_params.get('server', None)

        # Check if gameName and tagline are present
        if not (game_name and tagline):
            return Response({'error': 'gameName and tagline are required'}, status=400)

        # Build the header for the API call
        headers = {
            'X-Riot-Token': os.getenv('TOKEN'),
        }

        # Make a call to the Riot API for the first endpoint
        api_url = f'https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tagline}'
        response = requests.get(api_url, headers=headers)

        # Check if the API call was successful
        if response.status_code == 200:
            data = response.json()
            encrypted_puuid = data.get('puuid')

            # Make a call to the Riot API for the account endpoint
            account_api_url = f'https://{server}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{encrypted_puuid}'
            account_response = requests.get(account_api_url, headers=headers)

            # Check if the account API call was successful
            if account_response.status_code == 200:
                account_data = account_response.json()

                # Construct the URL for profile icon
                profile_icon_id = account_data.get('profileIconId')
                profile_icon_url = f'/static/profileIcon/{profile_icon_id}.png'  # Assuming your static files are served from '/static/'

                # Add profile_icon_url to account_data
                account_data['profileIconUrl'] = profile_icon_url

                # Make a call to the Riot API for the league endpoint
                encrypted_summoner_id = account_data.get('id')
                league_api_url = f'https://{server}.api.riotgames.com/lol/league/v4/entries/by-summoner/{encrypted_summoner_id}'
                league_response = requests.get(league_api_url, headers=headers)

                # Check if the league API call was successful
                if league_response.status_code == 200:
                    league_data = league_response.json()

                    # Append league_data to account_data
                    account_data['leagueData'] = league_data

                    # Return account data with league data appended
                    return Response(account_data)
                
                else:
                    return Response({'error': 'Failed to fetch data from league API call'}, status=league_response.status_code)
            else:
                return Response({'error': 'Failed to fetch data from account API call'}, status=account_response.status_code)
        else:
            return Response({'error': 'Failed to fetch data from first API call'}, status=response.status_code)


class MatchInfo(APIView):
    def get(self, request):
        # Get queryset parameters from the frontend
        encrypted_puuid = request.query_params.get('puuid', None)

        # Check if puuid is present
        if not encrypted_puuid:
            return Response({'error': 'puuid is required'}, status=400)

        # Build the header for the API call
        headers = {
            'X-Riot-Token': os.getenv('TOKEN'),
        }

        # Make a call to the Riot API for the match_id endpoint
        match_id_api_url = f'https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{encrypted_puuid}/ids'
        match_id_response = requests.get(match_id_api_url, headers=headers)

        # Check if the match_id API call was successful
        if match_id_response.status_code == 200:
            match_id_data = match_id_response.json()

            # Get data for the first 5 match IDs
            match_data_list = []
            for match_id in match_id_data[:5]:
                match_info_api_url = f'https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}'
                match_info_response = requests.get(match_info_api_url, headers=headers)
                if match_info_response.status_code == 200:
                    match_info_data = match_info_response.json()
                    match_data_list.append(match_info_data['info'])

                else:
                    return Response({'error': f'Failed to fetch data from match API call for match ID: {match_id}'}, status=match_info_response.status_code)

            # Return both the list of match IDs and match information
            return Response({'match_ids': match_id_data, 'matches': match_data_list})
        else:
            return Response({'error': 'Failed to fetch data from match_id API call'}, status=match_id_response.status_code)
