import os
import pygame
import requests

from Button import Button


# reload map
def reload(m_1, d_1, s_1, map_type, pts):
    # add points to map
    all_pt = ""
    if (pts != []):
        all_pt = "&pt="
        for i in range(len(pts)):
            if i != 0:
                all_pt += "~"
            all_pt += pts[i][0] + "," + pts[i][1] + ",round"
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
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={text_1}&format=json"
    response = requests.get(geocoder_request)
    if not response:
        print("Ошибка выполнения запроса")
        return 0, 0
    else:
        try:
            cords = (
                response.json()["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"][
                    "Point"][
                    "pos"])
        except IndexError:
            print("Ошибка выполнения запроса")
            return 0, 0
    return float(cords.split()[0]), float(cords.split()[1])


now_type = "map"
pts = []
active = False
m = float(input())
pygame.init()

screen = pygame.display.set_mode((600, 500))

# UI - text
input_box = pygame.Rect(300, 0, 200, 50)
pygame.draw.rect(screen, (0, 0, 0), input_box, 1)
font = pygame.font.Font(None, 24)
text = "Moscow"
txt_surface = font.render(text, True, (0, 0, 0))
screen.blit(txt_surface, (input_box.x + 20, input_box.y + 20))
find = Button(500, 0, 100, 50, (255, 255, 255), "Enter", (0, 0, 0), 20)
# UI - Buttons
schem = Button(0, 0, 100, 50, (150, 150, 150), "Схема", (0, 0, 0), 20)
sattalite = Button(100, 0, 100, 50, (255, 255, 255), "Спутник", (0, 0, 0), 20)
hybrid = Button(200, 0, 100, 50, (255, 255, 255), "Гибрид", (0, 0, 0), 20)
pygame.display.flip()
running = True
# First request
search = "Moscow"
d, s = find_place(search)
map_request = f"http://static-maps.yandex.ru/1.x/?ll={d},{s}&spn={m},{m}&l=map"
response = requests.get(map_request)
map_file = "map.png"
if not response:
    print("Ошибка выполнения запроса")
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
            if schem.pressed(event.pos):
                schem.change_color((150, 150, 150), screen)
                sattalite.change_color((255, 255, 255), screen)
                hybrid.change_color((255, 255, 255), screen)
                now_type = "map"
            # Set mode sattalite
            elif sattalite.pressed(event.pos):
                schem.change_color((255, 255, 255), screen)
                sattalite.change_color((150, 150, 150), screen)
                hybrid.change_color((255, 255, 255), screen)
                now_type = "sat"
            # Set mode hybrid
            elif hybrid.pressed(event.pos):
                hybrid.change_color((150, 150, 150), screen)
                sattalite.change_color((255, 255, 255), screen)
                schem.change_color((255, 255, 255), screen)
                now_type = "sat,skl"
            # Find new place and make a point
            elif find.pressed(event.pos):
                d, s = find_place(text)
                if d != 0 and s != 0:
                    pts.append([str(d), str(s)])
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
                    d, s = find_place(text)
                    if d != 0 and s != 0:
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
    # Fill screen
    screen.fill((255, 255, 255))
    # Show a map
    screen.blit(pygame.image.load(map_file), (0, 50))
    # Draw buttons
    find.draw_button(screen)
    schem.draw_button(screen)
    sattalite.draw_button(screen)
    hybrid.draw_button(screen)
    # Reload input text
    pygame.draw.rect(screen, (0, 0, 0), input_box, 1)
    txt_surface = font.render(text, True, (0, 0, 0))
    screen.blit(txt_surface, (input_box.x + 20, input_box.y + 20))
    # Yeah flippy-bottle challenge!!!
    pygame.display.flip()
pygame.quit()
os.remove(map_file)
