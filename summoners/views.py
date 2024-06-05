from rest_framework.views import APIView
from rest_framework.response import Response
import requests
import os
from dotenv import load_dotenv
from builds.models import RuneSlot
from users.models import FollowSummoner
load_dotenv()

class AccountInfoView(APIView):
    def get(self, request):
        # Get queryset parameters from the frontend
        game_name = request.query_params.get('gameName', None)
        tagline = request.query_params.get('tagLine', None)
        server = request.query_params.get('server', None)
        main_server = request.query_params.get('mainServer', None)
        # Check if gameName and tagline are present
        if not (game_name and tagline):
            return Response({'error': 'gameName and tagline are required'}, status=400)

        # Build the header for the API call
        headers = {
            'X-Riot-Token': os.getenv('TOKEN'),
        }

        # Make a call to the Riot API for the first endpoint
        api_url = f'https://{main_server}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tagline}'
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
                profile_icon_url = f'/static/profileIcon/{profile_icon_id}.png'

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

                    if request.user.is_authenticated:
                        # Check if the user follows this summoner
                        try:
                            FollowSummoner.objects.get(user=request.user, game_name=game_name, tagline=tagline, server=server, main_server=main_server)
                            account_data['is_following'] = True
                        except FollowSummoner.DoesNotExist:
                            account_data['is_following'] = False
                    
                    else:
                        account_data['is_following'] = False

                    # Return account data with league data appended
                    return Response(account_data)
                
                else:
                    return Response({'error': 'Failed to fetch data from league API call'}, status=league_response.status_code)
            else:
                return Response({'error': 'Failed to fetch data from account API call'}, status=account_response.status_code)
        else:
            return Response({'error': 'Failed to fetch data from first API call'}, status=response.status_code)



class MatchIdView(APIView):
    def get(self, request):
        # Get the puuid parameter from the query
        encrypted_puuid = request.query_params.get('puuid', None)
        main_server = request.query_params.get('mainServer', None)

        # Check if puuid is present
        if not encrypted_puuid:
            return Response({'error': 'puuid is required'}, status=400)
        
        # Build the header for the API call
        headers = {
            'X-Riot-Token': os.getenv('TOKEN'),
        }

        # Make the call to the match_id API
        match_id_api_url = f'https://{main_server}.api.riotgames.com/lol/match/v5/matches/by-puuid/{encrypted_puuid}/ids?count=100'
        match_id_response = requests.get(match_id_api_url, headers=headers)

        # Check if the match_id API call was successful
        if match_id_response.status_code == 200:
            match_id_data = match_id_response.json()
            # Return the match IDs
            return Response( match_id_data)
        else:
            return Response({'error': 'Failed to fetch data from match_id API call'}, status=match_id_response.status_code)


class MatchInfoView(APIView):
    def post(self, request):
        # Obtain List of matches Ids
        ids = request.data.get('ids', [])
        main_server = request.data.get('mainServer')


        match_info_list = []

        # Build the header for the API call
        headers = {
            'X-Riot-Token': os.getenv('TOKEN'),
        }

        # Iterate over each ID in the list
        for match_id in ids:
            # Build the API URL for each ID
            match_info_api_url = f'https://{main_server}.api.riotgames.com/lol/match/v5/matches/{match_id}'
            
            # Make the call to the API
            match_info_response = requests.get(match_info_api_url, headers=headers)

            # Check if the API call was successful
            if match_info_response.status_code == 200:
                match_info_data = match_info_response.json()
                # Map rune IDs to RuneSlot models
                for participant in match_info_data['info']['participants']:
                    # Map style selections
                    for style in participant['perks']['styles']:
                        style['selections'] = [self.map_rune_to_dict(selection['perk']) for selection in style['selections']]
                match_info_list.append(match_info_data['info'])  # Add match information to the list
            else:
                return Response({'error': f'Failed to fetch data from match API call for match ID: {match_id}'}, status=match_info_response.status_code)
        
        # Return the list of match information
        return Response(match_info_list)

    def map_rune_to_dict(self, rune_id):
        try:
            rune_slot = RuneSlot.objects.get(id=rune_id)
            rune_path = rune_slot.rune_path  # Get the RunePath related to the RuneSlot
            return {
                'id': rune_slot.id,
                'key': rune_slot.key,
                'icon': rune_slot.icon,
                'name': rune_slot.name,
                'slot_number': rune_slot.slot_number,
                'rune_path': {  # Include RunePath information
                    'id': rune_path.id,
                    'key': rune_path.key,
                    'icon': rune_path.icon,
                    'name': rune_path.name,
                }
            }
        except RuneSlot.DoesNotExist:
            return None


class MatchTimeLineView(APIView):
    def get(self, request):
        # Get the matchId parameter from the query
        match_id = request.query_params.get('matchId', None)
        server = request.query_params.get('server', None)
        main_server = request.query_params.get('mainServer', None)


        # Check if matchId is present
        if not match_id:
            return Response({'error': 'matchId is required'}, status=400)
        
        # Build the header for the API call
        headers = {
            'X-Riot-Token': os.getenv('TOKEN'),
        }

        # Make the call to the timeline API using matchId
        timeline_api_url = f'https://{main_server}.api.riotgames.com/lol/match/v5/matches/{server}_{match_id}/timeline'
        timeline_response = requests.get(timeline_api_url, headers=headers)

        # Check if the timeline API call was successful
        if timeline_response.status_code == 200:
            timeline_data = timeline_response.json()
            # Return the timeline data
            return Response(timeline_data)
        else:
            return Response({'error': 'Failed to fetch data from timeline API call'}, status=timeline_response.status_code)
