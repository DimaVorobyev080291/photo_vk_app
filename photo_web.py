import vkapiclient
import yaapiclient
import time 

tokens = []

with open('tokens.txt') as file :
    for row in file:
        red_row = row.strip()
        tokens.append(red_row)

print('Начало переноса фотографий из VK(профиль) на Яндекс.Диск:')
time.sleep(1)
vk_client = vkapiclient.VKAPIClient(tokens[0], tokens[1])
photos_info = vk_client.get_profile_photo()
photo_likes = vk_client.maximum_size_photo_likes(photos_info)
photo_size = vk_client.maximum_size_photo_links(photos_info)
photo_date = vk_client.maximum_size_photo_date(photos_info)
photo_name = vk_client.unique_names(photo_likes, photo_date)
time.sleep(1)
json_file = vk_client.info_photo(photo_name, photo_size)
ya_client = yaapiclient.YAAPIClient(tokens[2])
time.sleep(1)
folder = ya_client.creating_folder()
time.sleep(1)
load = ya_client.uploading_photos(photo_name, photo_size)
print('Перенос фотографий завершён!')