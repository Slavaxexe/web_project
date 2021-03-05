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
        print("error")
        return False
    with open(map_f, "wb") as file_1:
        file_1.write(resp.content)
    return True


# find place by name
def find_place(cords):
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&" \
                       f"geocode={cords}&format=json"

    response_1 = requests.get(geocoder_request)
    if not response_1:
        print("Ошибка выполнения запроса3")
        return 0, 0, "Null", "No postal code"
    else:
        try:
            response_json = response_1.json()
            cords = response_json["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"][
                "Point"][
                "pos"]
            place = response_json["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"][
                "metaDataProperty"][
                "GeocoderMetaData"]["text"]
            try:
                postal_code_func = " " + response_json["response"]["GeoObjectCollection"]["featureMember"][0][
                    "GeoObject"][
                    "metaDataProperty"][
                    "GeocoderMetaData"]["Address"]["postal_code"]
            except KeyError:
                postal_code_func = " No postal code"
        except IndexError:
            print("Ошибка выполнения запроса2")
            return 0, 0, "Null", "No postal code"
    return float(cords.split()[0]), float(cords.split()[1]), place, postal_code_func


# Type of the map
now_type = "map"
# All points
pts = []
now_point = []
# Can we write&
active = False
# Scale
m = 1
kf = 0.825
# Last time for scrolling
last_time = time()
now_sim = 0
# Is postal code showing
postal_code_show = False
postal_code = ""
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
info_text = ""
text_place = font.render(info_text, True, (0, 0, 0))
info_text_show = info_text
# UI - Buttons
find = Button(500, 0, 100, 50, (255, 255, 255), "Enter", (0, 0, 0), 20)
remove = Button(500, 50, 100, 50, (255, 255, 255), "Remove", (0, 0, 0), 20)
schema = Button(0, 0, 100, 50, (150, 150, 150), "Схема", (0, 0, 0), 20)
satellite = Button(100, 0, 100, 50, (255, 255, 255), "Спутник", (0, 0, 0), 20)
hybrid = Button(200, 0, 100, 50, (255, 255, 255), "Гибрид", (0, 0, 0), 20)
postal_code_button = Button(200, 50, 100, 50, (255, 255, 255), "Индекс", (0, 0, 0), 20)
next_place = Button(0, 50, 100, 50, (255, 255, 255), "Следующее", (0, 0, 0), 20)
pygame.display.flip()
running = True
# First request
search = "Moscow"
d, s, _, _ = find_place(search)
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
            if event.button == 3:
                right_position = list(event.pos)
                right_position[0] -= 300
                right_position[1] -= 325
                req = str(d + right_position[0] * (2 * m * 0.825 / 300)) + "," + str(
                    s - right_position[1] * (m * 0.7 / 225))
                _, _, info_text, postal_code = find_place(req)
                text = str(round(float(req.split(",")[0]), 3)) + "," + str(round(float(req.split(",")[1]), 3))
                d_mid = d + right_position[0] * (2 * m * 0.825 / 300)
                s_mid = s - right_position[1] * (m * 0.7 / 225)
                info_text = "     " + info_text
                if postal_code_show:
                    info_text += postal_code
                info_text_show = info_text
                now_sim = 0
                if d_mid != 0 and s_mid != 0 and [str(d_mid), str(s_mid)] not in pts:
                    pts.append([str(d_mid), str(s_mid)])
                    now_point = [str(d_mid), str(s_mid)]
            # Enter a text
            if input_box.collidepoint(event.pos):
                active = True
            else:
                active = False
            # Set mode schema
            if schema.pressed(event.pos):
                schema.change_color((150, 150, 150))
                satellite.change_color((255, 255, 255))
                hybrid.change_color((255, 255, 255))
                now_type = "map"
            # Set mode satellite
            elif satellite.pressed(event.pos):
                schema.change_color((255, 255, 255))
                satellite.change_color((150, 150, 150))
                hybrid.change_color((255, 255, 255))
                now_type = "sat"
            # Set mode hybrid
            elif hybrid.pressed(event.pos):
                hybrid.change_color((150, 150, 150))
                satellite.change_color((255, 255, 255))
                schema.change_color((255, 255, 255))
                now_type = "sat,skl"
            # Find new place and make a point
            elif find.pressed(event.pos):
                d, s, info_text, postal_code = find_place(text)
                info_text = "     " + info_text
                if postal_code_show:
                    info_text += postal_code
                info_text_show = info_text
                now_sim = 0
                if d != 0 and s != 0 and [str(d), str(s)] not in pts:
                    pts.append([str(d), str(s)])
                    now_point = [str(d), str(s)]
            # Remove all points
            elif remove.pressed(event.pos):
                pts = []
                info_text = ""
                info_text_show = ""
            # Show postal code or not
            elif postal_code_button.pressed(event.pos):
                postal_code_show = not postal_code_show
                if postal_code_show:
                    info_text += postal_code
                    postal_code_button.change_color((150, 150, 150))
                else:
                    # If no postal code
                    if "No postal code" in info_text:
                        info_text = info_text[0:-15]
                        info_text_show = info_text
                    else:
                        info_text = info_text[0:-7]
                        info_text_show = info_text
                    postal_code_button.change_color((255, 255, 255))
            elif next_place.pressed(event.pos) and len(pts) > 1:
                index_next = pts.index(now_point) - 1
                if index_next == -1:
                    index_next = len(pts) - 1
                d, s, info_text, postal_code = find_place(pts[index_next][0] + "," + pts[index_next][1])
                now_point = [str(d), str(s)]
                pts[index_next] = [str(d), str(s)]
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
                    d, s, info_text, postal_code = find_place(text)
                    info_text = "     " + info_text
                    info_text_show = info_text
                    if postal_code_show:
                        info_text += postal_code
                    now_sim = 0
                    if d != 0 and s != 0 and [str(d), str(s)] not in pts:
                        pts.append([str(d), str(s)])
                        now_point = [str(d), str(s)]
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
    # Show_all_text
    if time() - last_time > 0.1 and len(info_text) > 19:
        last_time = time()
        if now_sim != len(info_text):
            now_sim += 1
        else:
            now_sim = 0
        info_text_show = info_text[now_sim:now_sim + 19]
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
    postal_code_button.draw_button(screen)
    next_place.draw_button(screen)
    # Reload input text
    pygame.draw.rect(screen, (0, 0, 0), input_box, 1)
    txt_surface = font.render(text, True, (0, 0, 0))
    screen.blit(txt_surface, (input_box.x + 20, input_box.y + 20))
    pygame.draw.rect(screen, (0, 0, 0), input_box_2, 1)
    text_place = font.render(info_text_show, True, (0, 0, 0))
    screen.blit(text_place, (input_box_2.x + 10, input_box_2.y + 20))
    # Yeah flippy-bottle challenge!!!
    pygame.display.flip()
pygame.quit()
os.remove(map_file)
