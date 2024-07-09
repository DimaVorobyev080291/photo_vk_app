import requests
import time 
from tqdm import tqdm

class YAAPIClient:

    def __init__(self, token_ya):
        self.token_ya = token_ya

    def creating_folder(self, folder_name):
        self.folder_name = folder_name

        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        payload = {}
        headers = {
            'Authorization': self.token_ya 
            }
        params = {'path': self.folder_name}
        response = requests.request('PUT', url, headers=headers, data=payload, params=params)

        if 200 <= response.status_code < 300:
            return print (f'Папка {self.folder_name} успешно создана.')
        elif response.status_code == 401:
            return print ('Яндекс токен не верный !')
        elif response.status_code == 409:
            return print ('Папка с таким именем уже есть !')
        else:
            return print (f'Проблема с созданием папки !{response.status_code}')

    def uploading_photos(self, photo_name, photo_size, folder_name):
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        payload = {}
        headers = {
            'Authorization': self.token_ya
        }

        count = 1 
        for name,size in tqdm(zip(photo_name, photo_size)):
            params = {
                'path': (f'{folder_name}/{name}'),
                'url': size['url']
            }
              
            response = requests.request('POST', url, headers=headers, data=payload, params=params)
            time.sleep(4)
            if 200 <= response.status_code < 300:
                print (f'Фото номер {count} успешно отправленно. Код ответа {response.status_code}.')
            elif response.status_code == 400:
                print (f'Фото номер {count} ошибка отправки, некорректные данные!')
                print (f'Код ответа {response.status_code}.')
            elif response.status_code == 403:
                print (f'Фото номер {count} ошибка отправки! Ваши файлы занимают больше места,')
                print (f'чем у вас есть! Код ответа {response.status_code}.')
            else:
                print (f'Проблема с отправкой фото!{response.status_code}')           
            count+=1