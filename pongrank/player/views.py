from rest_framework import viewsets
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
import requests
from collections import defaultdict
import ast
from django.conf import settings
import spotipy
import spotipy.util as util
# Create your views here.


class SpotifyViewSet(viewsets.ViewSet):

    @staticmethod
    def spotify(request):

        url = 'https://api.spotify.com/v1/users/12130416973/playlists/1I1h4VN5ztjrlRpkOZCbHU?si=yjlwSodiQ_uJbKF-H1w6m'
        url_user = 'https://api.spotify.com/v1/users/'
        headers = {'Authorization': 'Bearer BQBRz8zvS9r27Rv62a8w-2THknmWp-71WE4Lh7d2SYRbZHDZNW78DnysqHGb2T1WAm374qms1OZXdMTqBUdbLu8_6zhy6vrgt8HJkmCeSLkPrij8Vt5_w6Fhmycn7Rpd9Z23RwzllZBpRiYmyYQa8R_lanF6QH3x6AVcbcUrX8ztBoH0TfnE44-Oyag94pXeZ86qJhvsaDrELwToTQ2ULUA-VDCge2XtMHbTQgMtc6TupPzLTBGEpPAxKmTDwCMNtoUuc2oE'}
        response = requests.get(url, headers=headers)
        tracks = list()
        tracks.extend(response.json().get('tracks').get('items'))
        next_tracks = response.json().get('tracks').get('next')
        go = True
        while(go):

            if next_tracks is not None:
                response = requests.get(next_tracks, headers=headers)
                tracks.extend(response.json().get('items'))
                next_tracks = response.json().get('next')
            else:
                go = False

        users = dict()

        for track in tracks:
            number_id = track.get('added_by').get('id')
            response2 = requests.get(url_user + number_id, headers=headers)
            id = response2.json().get('display_name')
            if id is None:
                id = number_id
            if users.get(id) is not None:
                users[id] = users.get(id) + 1
            else:
                response2 = requests.get(url_user + number_id, headers=headers)
                id = response2.json().get('display_name')
                if id is None:
                    id = number_id
                users.update({id: 1})

        return Response(data=users, status=status.HTTP_200_OK)
