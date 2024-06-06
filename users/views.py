from rest_framework.views import APIView
from rest_framework.response import Response
import requests
import random
import os
from dotenv import load_dotenv
from .models import LinkedAccount, FollowSummoner, FriendRequest
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .serializers import LinkedAccountSerializer, FollowSummonerSerializer, FriendRequestSerializer
from django.contrib.auth.models import User


load_dotenv()

class LinkAccountView(APIView):
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


class VerifyAccountView(APIView):
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



class GetVerifiedAccountsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({'error': 'User is not authenticated'}, status=401)

        verified_accounts = LinkedAccount.objects.filter(user=user)
        serializer = LinkedAccountSerializer(verified_accounts, many=True)
        return Response(serializer.data)
    

class FollowSummonerView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
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

        try:
            FollowSummoner.objects.get(
                game_name=game_name,
                tagline=tagline,
                server=server,
                main_server=main_server,
                user=user,
            ).delete()
            
            return Response({'Follow': False})

        except:
            FollowSummoner.objects.create(
                game_name=game_name,
                tagline=tagline,
                server=server,
                main_server=main_server,
                user=user,
            )

            return Response({'Follow': True})


class GetFollowedSummonersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({'error': 'User is not authenticated'}, status=401)

        followed_summoners = FollowSummoner.objects.filter(user=user)
        serializer = FollowSummonerSerializer(followed_summoners, many=True)
        return Response(serializer.data)
    



class FriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        sender = request.user
        receiver_username = request.data.get('receiver_username')
        if not receiver_username:
            return Response({'error': 'receiver username is required'}, status=400)

        try:
            receiver = User.objects.get(username=receiver_username)
        except User.DoesNotExist:
            return Response({'error': 'Receiver not found'}, status=404)

        if sender == receiver:
            return Response({'error': 'You cannot send a friend request to yourself'}, status=404)

        # Check if a friend request already exists
        existing_request_sent = FriendRequest.objects.filter(sender=sender, receiver=receiver).first()
        existing_request_received = FriendRequest.objects.filter(sender=receiver, receiver=sender).first()
        
        


        if existing_request_sent or existing_request_received:
            if (existing_request_sent and existing_request_sent.accepted) or (existing_request_received and existing_request_received.accepted):
                return Response({'error': 'You are already friends with this user'}, status=404)
            else:
                return Response({'error': 'Friend request already sent or received'}, status=404)

        friend_request = FriendRequest.objects.create(sender=sender, receiver=receiver)
        serializer = FriendRequestSerializer(friend_request)
        return Response(serializer.data, status=201)



class FriendRequestRecivedView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        receiver = request.user
        sender_username = request.data.get('sender_username')
        if not sender_username:
            return Response({'error': 'receiver username is required'}, status=400)

        try:
            sender = User.objects.get(username=sender_username)
        except User.DoesNotExist:
            return Response({'error': 'sender not found'}, status=404)

        if receiver == sender:
            return Response({'error': 'You cannot send a friend request to yourself'}, status=404)

        # Check if a friend request  exists
        existing_request = FriendRequest.objects.filter(receiver=receiver, sender=sender).first()
        if existing_request:
            # Update the friend request to accepted
            existing_request.accepted = True
            existing_request.save()
            serializer = FriendRequestSerializer(existing_request)
            return Response(serializer.data, status=200)

        else:
            return Response({'error': 'Friend request Dosnt exist'}, status=400)


    def delete(self, request):
        receiver = request.user
        sender_username = request.data.get('sender_username')
        if not sender_username:
            return Response({'error': 'sender_username is required'}, status=400)

        try:
            sender = User.objects.get(username=sender_username)
        except User.DoesNotExist:
            return Response({'error': 'sender not found'}, status=404)

        # Check if the friend request exists
        friend_request = FriendRequest.objects.filter(receiver=receiver, sender=sender).first()
        if not friend_request:
            return Response({'error': 'Friend request not found'}, status=404)

        friend_request.delete()
        return Response({'message': 'Friend request deleted'}, status=204)


class FriendRequestsListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        received_requests = FriendRequest.objects.filter(receiver=user, accepted=False)
        sent_requests = FriendRequest.objects.filter(sender=user, accepted=False)
        received_serializer = FriendRequestSerializer(received_requests, many=True)
        sent_serializer = FriendRequestSerializer(sent_requests, many=True)
        return Response({'received_requests': received_serializer.data, 'sent_requests': sent_serializer.data})
    

class FriendsListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        friends_received = FriendRequest.objects.filter(receiver=user, accepted=True)
        friends_sent = FriendRequest.objects.filter(sender=user, accepted=True)
        
        friends_received_usernames = [friend_request.sender.username for friend_request in friends_received]
        friends_sent_usernames = [friend_request.receiver.username for friend_request in friends_sent]

        all_friends_usernames = set(friends_received_usernames + friends_sent_usernames)

        return Response(list(all_friends_usernames))
