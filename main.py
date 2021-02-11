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
    else:
        with open(map_f, "wb") as file_1:
            file_1.write(resp.content)
        screen.blit(pygame.image.load(map_file), (0, 50))
        return True


d, s, m = float(input()), float(input()), float(input())
now_type = "map"

map_request = f"http://static-maps.yandex.ru/1.x/?ll={d},{s}&spn={m},{m}&l=map"
response = requests.get(map_request)
if not response:
    print("Ошибка выполнения запроса:")
map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)


pygame.init()

screen = pygame.display.set_mode((600, 500))
screen.fill((255, 255, 255))
screen.blit(pygame.image.load(map_file), (0, 50))
schem = Button(0, 0, 100, 50, (150, 150, 150), "Схема", (0, 0, 0), 20)
sattalite = Button(100, 0, 100, 50, (255, 0, 255), "Спутник", (0, 0, 0), 20)
hybride = Button(200, 0, 100, 50, (0, 0, 255), "Гибрид", (0, 0, 0), 20)
schem.draw_button(screen)
sattalite.draw_button(screen)
hybride.draw_button(screen)
pygame.display.flip()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if schem.pressed(event.pos):
                schem.change_color((150, 150, 150), screen)
                sattalite.change_color((255, 0, 255), screen)
                hybride.change_color((0, 0, 255), screen)
                now_type = "map"
            elif sattalite.pressed(event.pos):
                schem.change_color((0, 255, 0), screen)
                sattalite.change_color((150, 150, 150), screen)
                hybride.change_color((0, 0, 255), screen)
                now_type = "sat"
            elif hybride.pressed(event.pos):
                hybride.change_color((150, 150, 150), screen)
                sattalite.change_color((255, 0, 255), screen)
                schem.change_color((0, 255, 0), screen)
                now_type = "sat,skl"
            reload(m, d, s, now_type)
        if event.type == pygame.KEYDOWN:
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
            if not(reload(m, d, s, now_type)):
                s = last_s
                m = last_m
                d = last_d
    pygame.display.flip()
pygame.quit()
os.remove(map_file)
