import os
import sys
import pygame
import requests


d, s, m = float(input()), float(input()), float(input())
map_request = f"http://static-maps.yandex.ru/1.x/?ll={d},{s}&spn={m},{m}&l=map"
response = requests.get(map_request)

if not response:
    print("Ошибка выполнения запроса:")
    print(map_request)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)

map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

pygame.init()
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.flip()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            last_s = s
            last_d = d
            if event.key == pygame.K_LEFT:
                d -= m / 3
            if event.key == pygame.K_RIGHT:
                d += m / 3
            if event.key == pygame.K_UP:
                s += m / 3
            if event.key == pygame.K_DOWN:
                s -= m / 3
            map_request = f"http://static-maps.yandex.ru/1.x/?ll={d},{s}&spn={m},{m}&l=map"
            response = requests.get(map_request)
            if not response:
                s = last_s
                d = last_d
                print("Ошибка выполнения запроса:")
            else:
                map_file = "map.png"
                with open(map_file, "wb") as file:
                    file.write(response.content)
                screen.blit(pygame.image.load(map_file), (0, 0))
        elif event.type == pygame.QUIT:
            running = False
    pygame.display.flip()

pygame.quit()
os.remove(map_file)
