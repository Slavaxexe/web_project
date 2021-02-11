import os
import pygame
import requests

from Button import Button


def reload(m_1, d_1, s_1, map_type):
    map_req = f"http://static-maps.yandex.ru/1.x/?ll={d_1},{s_1}&spn={m_1},{m_1}&l={map_type}"
    resp = requests.get(map_req)
    map_f = "map.png"
    if not resp:
        return False
    with open(map_f, "wb") as file_1:
        file_1.write(resp.content)
    screen.blit(pygame.image.load(map_file), (0, 50))
    return True


now_type = "map"
active = False
m = float(input())
pygame.init()

screen = pygame.display.set_mode((600, 500))

input_box = pygame.Rect(300, 0, 200, 50)
pygame.draw.rect(screen, (0, 0, 0), input_box, 1)
font = pygame.font.Font(None, 24)
text = "Moscow"
txt_surface = font.render(text, True, (0, 0, 0))
screen.blit(txt_surface, (input_box.x + 20, input_box.y + 20))

schem = Button(0, 0, 100, 50, (150, 150, 150), "Схема", (0, 0, 0), 20)
sattalite = Button(100, 0, 100, 50, (255, 255, 255), "Спутник", (0, 0, 0), 20)
hybride = Button(200, 0, 100, 50, (255, 255, 255), "Гибрид", (0, 0, 0), 20)
pygame.display.flip()
running = True

search = "Moscow"
geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={search}&format=json"
response = requests.get(geocoder_request)
cords = ""
if not response:
    print("Ошибка выполнения запроса")
else:
    cords = (response.json()["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"])
d, s = float(cords.split()[0]), float(cords.split()[1])
map_request = f"http://static-maps.yandex.ru/1.x/?ll={d},{s}&spn={m},{m}&l=map"
response = requests.get(map_request)
map_file = "map.png"
if not response:
    print("Ошибка выполнения запроса")
else:
    with open(map_file, "wb") as file:
        file.write(response.content)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active = True
            else:
                active = False
            if schem.pressed(event.pos):
                schem.change_color((150, 150, 150), screen)
                sattalite.change_color((255, 255, 255), screen)
                hybride.change_color((255, 255, 255), screen)
                now_type = "map"
            elif sattalite.pressed(event.pos):
                schem.change_color((255, 255, 255), screen)
                sattalite.change_color((150, 150, 150), screen)
                hybride.change_color((255, 255, 255), screen)
                now_type = "sat"
            elif hybride.pressed(event.pos):
                hybride.change_color((150, 150, 150), screen)
                sattalite.change_color((255, 255, 255), screen)
                schem.change_color((255, 255, 255), screen)
                now_type = "sat,skl"
            reload(m, d, s, now_type)
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={text}&format=json"
                    response = requests.get(geocoder_request)
                    cords = ["0", "0"]
                    if not response:
                        print("Ошибка выполнения запроса")
                    else:
                        cords = (
                            response.json()["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"][
                                "Point"][
                                "pos"])
                    d, s = float(cords.split()[0]), float(cords.split()[1])
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
            last_s = s
            last_d = d
            last_m = m
            if event.key == pygame.K_PAGEUP:
                m *= 2
            if event.key == pygame.K_PAGEDOWN:
                m /= 2
            if event.key == pygame.K_LEFT:
                d -= m / 3
            if event.key == pygame.K_RIGHT:
                d += m / 3
            if event.key == pygame.K_UP:
                s += m / 3
            if event.key == pygame.K_DOWN:
                s -= m / 3
            if not (reload(m, d, s, now_type)):
                s = last_s
                m = last_m
                d = last_d

    screen.fill((255, 255, 255))

    screen.blit(pygame.image.load(map_file), (0, 50))

    schem.draw_button(screen)
    sattalite.draw_button(screen)
    hybride.draw_button(screen)

    pygame.draw.rect(screen, (0, 0, 0), input_box, 1)
    txt_surface = font.render(text, True, (0, 0, 0))
    screen.blit(txt_surface, (input_box.x + 20, input_box.y + 20))
    pygame.display.flip()
pygame.quit()
os.remove(map_file)
