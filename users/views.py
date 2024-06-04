from rest_framework.views import APIView
from rest_framework.response import Response
import requests
import random
import os
from dotenv import load_dotenv
from .models import LinkedAccount
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .serializers import LinkedAccountSerializer

load_dotenv()

class LinkAccount(APIView):
    def get(self, request):
        # Check if user is authenticated
        user = request.user
        if not user.is_authenticated:
            return Response({'error': 'User is not authenticated'}, status=401)
        
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

                # Check if the League of Legends account is already linked to another user and verified
                existing_verified_account = LinkedAccount.objects.get(
                    game_name=game_name,
                    tagline=tagline,
                    server=server,
                    main_server=main_server,
                    verified=True,
                )

                if existing_verified_account:
                    return Response({'error': 'This League of Legends account is already linked to another user'}, status=400)
            
                profile_icon_id = account_data.get('profileIconId')

                # Generate a random number for the temporary icon id
                random_number = random.randint(0, 27)
                while random_number == profile_icon_id:
                    random_number = random.randint(0, 27)

                # Create or get the LinkedAccount instance
                linked_account, created = LinkedAccount.objects.get_or_create(
                    user=user,
                    game_name=game_name,
                    tagline=tagline,
                    server=server,
                    main_server=main_server,
                    defaults={'temp_icon_id': random_number}
                )

                # If the instance already exists, update its temp_icon_id and verified status
                if not created:
                    linked_account.temp_icon_id = random_number
                    linked_account.verified = False
                    linked_account.save()
                # Return random number
                return Response({'random_number': random_number})


            else:
                return Response({'error': 'Failed to fetch data from account API call'}, status=account_response.status_code)
        else:
            return Response({'error': 'the summoner does not exist'}, status=response.status_code)


class VerifyAccount(APIView):
    def get(self, request):
        # Check if user is authenticated
        user = request.user
        if not user.is_authenticated:
            return Response({'error': 'User is not authenticated'}, status=401)

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
                profile_icon_id = account_data.get('profileIconId')

                # Get the LinkedAccount instance corresponding to the user and request parameters
                linked_account = get_object_or_404(
                    LinkedAccount,
                    user=user,
                    game_name=game_name,
                    tagline=tagline,
                    server=server,
                    main_server=main_server
                )

                # Check if the profile icon matches the temporary icon of the linked account
                if profile_icon_id == linked_account.temp_icon_id:
                    # If they match, mark the account as verified
                    linked_account.verified = True
                    linked_account.save()
                    return Response({'status': 'Account verified successfully'})
                else:
                    # If they don't match, return an error
                    return Response({'error': 'Profile icon does not match'}, status=400)
            else:
                return Response({'error': 'Failed to fetch data from account API call'}, status=account_response.status_code)
        else:
            return Response({'error': 'Failed to fetch data from first API call'}, status=response.status_code)





class GetVerifiedAccounts(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({'error': 'User is not authenticated'}, status=401)

        verified_accounts = LinkedAccount.objects.filter(user=user)
        serializer = LinkedAccountSerializer(verified_accounts, many=True)
        return Response(serializer.data)