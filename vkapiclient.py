import requests
import time
import json

class VKAPIClient:

    API_BASE_URL = 'https://api.vk.com/method'

    def __init__(self, token, user_id):
        self.token = token
        self.user_id = user_id

    def get_common_params(self):
        return{
            'access_token': self.token,
            'v': '5.131'
        }
    
    def _build_url(self, api_method):
        return f'{self.API_BASE_URL}/{api_method}'
    
    def get_profile_photo(self):
        params = self.get_common_params()
        params.update({'owner_id': self.user_id, 'album_id': 'profile','extended':'likes'})
        response = requests.get(self._build_url('photos.get'), params=params)
        if 200 <= response.status_code < 300:
            print(f'Фотографии из VK получены. Код ответа {response.status_code}')
        else:
            print(f'Не удалось получить доступ к фотографиям. Код ответа {response.status_code}. ')
        return response.json()
    
    def maximum_size_photo_links(self, profile_photo):
        maximum_size_photo = []

        photos = profile_photo["response"]["items"]
        for i in photos :
            maximum_size_photo.append(i["sizes"][-1])
        
        return maximum_size_photo
    
    def maximum_size_photo_likes(self, profile_photo):
        maximum_size_photo_likes = []

        photos = profile_photo["response"]["items"]
        for i in photos :
            maximum_size_photo_likes.append(i["likes"]["count"])
        
        return maximum_size_photo_likes
    
    def maximum_size_photo_date(self, profile_photo):
        maximum_size_photo_date = []

        photos = profile_photo["response"]["items"]
        for i in photos :
            unix_timestamp = i["date"]
            unix_timestamp = float(unix_timestamp)
            time_struct = time.gmtime(unix_timestamp)
            maximum_size_photo_date.append(time.strftime("%d-%B-%Y", time_struct))

        return maximum_size_photo_date
    
    def unique_names(self, likes , date):
        unque_name = []

        for l ,d in zip(likes, date): 
            if l in unque_name:
                unque_name.append(d)
            else:
                unque_name.append(l)

        return unque_name
    
    def info_photo (self, name, type):
        info_photo = []

        for n,t in zip(name, type):
            info_photo.append({"file_name": f'{n}.jpg', "size": t["type"]})
        
        with open('info_photo.json', 'w') as json_file :
            json.dump(info_photo, json_file)

        return print('Файл с информацией по фотографиям создан.')