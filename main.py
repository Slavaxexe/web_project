import os
from time import time

import pygame
import requests

from Button import Button


# reload map
def reload(m_1, d_1, s_1, map_type, points):
    # add points to map
    all_pt = ""
    if points:
        all_pt = "&pt="
        for i in range(len(points)):
            if i != 0:
                all_pt += "~"
            all_pt += points[i][0] + "," + points[i][1] + ",round"
    # request for new map
    map_req = f"http://static-maps.yandex.ru/1.x/?ll={d_1},{s_1}&spn={m_1},{m_1}&l={map_type}{all_pt}"
    resp = requests.get(map_req)
    map_f = "map.png"
    if not resp:
        return False
    with open(map_f, "wb") as file_1:
        file_1.write(resp.content)
    return True


# find place by name
def find_place(text_1):
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&" \
                       f"geocode={text_1}&format=json"
    response_1 = requests.get(geocoder_request)
    if not response_1:
        print("Ошибка выполнения запроса3")
        return 0, 0, "Null"
    else:
        try:
            response_json = response_1.json()
            cords = response_json["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"][
                "Point"][
                "pos"]
            place = response_json["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"][
                "metaDataProperty"][
                "GeocoderMetaData"]["text"]
        except IndexError:
            print("Ошибка выполнения запроса2")
            return 0, 0, "Null"
    return float(cords.split()[0]), float(cords.split()[1]), place


# Type of the map
now_type = "map"
# All points
pts = []
# Can we write&
active = False
# Scale
m = float(input())
# Last time for scrolling
last_time = time()
now_sim = 0
pygame.init()

screen = pygame.display.set_mode((600, 550))

# UI - text
input_box = pygame.Rect(300, 0, 200, 50)
pygame.draw.rect(screen, (0, 0, 0), input_box, 1)
font = pygame.font.Font(None, 24)
text = "Moscow"
txt_surface = font.render(text, True, (0, 0, 0))
input_box_2 = pygame.Rect(300, 50, 200, 50)
pygame.draw.rect(screen, (0, 0, 0), input_box_2, 1)
text_2 = ""
text_place = font.render(text_2, True, (0, 0, 0))
text_2_enter = text_2
# UI - Buttons
find = Button(500, 0, 100, 50, (255, 255, 255), "Enter", (0, 0, 0), 20)
remove = Button(500, 50, 100, 50, (255, 255, 255), "Remove", (0, 0, 0), 20)
schema = Button(0, 0, 100, 50, (150, 150, 150), "Схема", (0, 0, 0), 20)
satellite = Button(100, 0, 100, 50, (255, 255, 255), "Спутник", (0, 0, 0), 20)
hybrid = Button(200, 0, 100, 50, (255, 255, 255), "Гибрид", (0, 0, 0), 20)
pygame.display.flip()
running = True
# First request
search = "Moscow"
d, s, _ = find_place(search)
map_request = f"http://static-maps.yandex.ru/1.x/?ll={d},{s}&spn={m},{m}&l=map"
response = requests.get(map_request)
map_file = "map.png"
if not response:
    print("Ошибка выполнения запроса1")
else:
    with open(map_file, "wb") as file:
        file.write(response.content)
# Main cycle
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Mouse events
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Enter a text
            if input_box.collidepoint(event.pos):
                active = True
            else:
                active = False
            # Set mode schema
            if schema.pressed(event.pos):
                schema.change_color((150, 150, 150), screen)
                satellite.change_color((255, 255, 255), screen)
                hybrid.change_color((255, 255, 255), screen)
                now_type = "map"
            # Set mode satellite
            elif satellite.pressed(event.pos):
                schema.change_color((255, 255, 255), screen)
                satellite.change_color((150, 150, 150), screen)
                hybrid.change_color((255, 255, 255), screen)
                now_type = "sat"
            # Set mode hybrid
            elif hybrid.pressed(event.pos):
                hybrid.change_color((150, 150, 150), screen)
                satellite.change_color((255, 255, 255), screen)
                schema.change_color((255, 255, 255), screen)
                now_type = "sat,skl"
            # Find new place and make a point
            elif find.pressed(event.pos):
                d, s, text_2 = find_place(text)
                text_2 = "     " + text_2
                text_2_enter = text_2
                now_sim = 0
                if d != 0 and s != 0 and [str(d), str(s)] not in pts:
                    pts.append([str(d), str(s)])
            elif remove.pressed(event.pos):
                pts = []
                text_2 = ""
                text_2_enter = ""
            # Reload if not tap on change-text window
            if not input_box.collidepoint(event.pos):
                reload(m, d, s, now_type, pts)
        # Keyboard
        if event.type == pygame.KEYDOWN:
            last_text = text
            # Add new letters
            if active:
                # Enter a value, add new point
                if event.key == pygame.K_RETURN:
                    d, s, text_2 = find_place(text)
                    text_2 = "     " + text_2
                    text_2_enter = text_2
                    now_sim = 0
                    if d != 0 and s != 0 and [str(d), str(s)] not in pts:
                        pts.append([str(d), str(s)])
                    active = False
                # Remove last symbol
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                # Add text
                else:
                    text += event.unicode
            last_s = s
            last_d = d
            last_m = m
            # Change scale
            if event.key == pygame.K_PAGEUP:
                m *= 2
            if event.key == pygame.K_PAGEDOWN:
                m /= 2
            # Move for a map
            if event.key == pygame.K_LEFT:
                d -= m / 3
            if event.key == pygame.K_RIGHT:
                d += m / 3
            if event.key == pygame.K_UP:
                s += m / 3
            if event.key == pygame.K_DOWN:
                s -= m / 3
            # If text not changed reload a map
            if last_text == text:
                if not (reload(m, d, s, now_type, pts)):
                    s = last_s
                    m = last_m
                    d = last_d
    #show_all_text
    if time() - last_time > 0.1 and len(text_2) > 19:
        last_time = time()
        if now_sim != len(text_2):
            now_sim += 1
        else:
            now_sim = 0
        text_2_enter = text_2[now_sim:now_sim + 19]
    # Fill screen
    screen.fill((255, 255, 255))
    # Show a map
    screen.blit(pygame.image.load(map_file), (0, 100))
    # Draw buttons
    remove.draw_button(screen)
    find.draw_button(screen)
    schema.draw_button(screen)
    satellite.draw_button(screen)
    hybrid.draw_button(screen)
    # Reload input text
    pygame.draw.rect(screen, (0, 0, 0), input_box, 1)
    txt_surface = font.render(text, True, (0, 0, 0))
    screen.blit(txt_surface, (input_box.x + 20, input_box.y + 20))
    pygame.draw.rect(screen, (0, 0, 0), input_box_2, 1)
    text_place = font.render(text_2_enter, True, (0, 0, 0))
    screen.blit(text_place, (input_box_2.x + 10, input_box_2.y + 20))
    # Yeah flippy-bottle challenge!!!
    pygame.display.flip()
pygame.quit()
os.remove(map_file)
