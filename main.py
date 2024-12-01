import subprocess
import sys
import json

import pygame
from typing import List

# Constants
SCREEN_WIDTH = 2000
SCREEN_HEIGHT = 800
FPS = 60  # Frames per second
BAR_WIDTH = SCREEN_WIDTH // 2
NUM_BOOLS = 29 # or 34 for p1
NUM_INTS = 5   #10 for p1
TOTAL_VALS = NUM_BOOLS + NUM_INTS
max_number = 0
min_number = 1000000
avg_numbers = set()
avg_number_len = 0

# def tail_input_file():
#     try:
#         result = subprocess.Popen(
#             # This eventually should be a environment variable
#             # "/home/mia_bobia/Downloads/Fightcade-linux-latest/Fightcade/emulator/fbneo/scripts/state_dump_bools.json"
#             "tail -n 1 /home/nbee/Downloads/Fightcade/emulator/fbneo/scripts/state_dump.json",
#             shell=True, stdout=subprocess.PIPE
#         ).stdout.read().decode('UTF-8')

#         split = result.split('\r\n')
#         loaded = json.loads(split[0])
#         # print(loaded)
#         return { "p1_bools": loaded['bools']['p1'],
#                  "p2_bools": loaded['bools']['p2'],
#                  "p1_numbers": loaded['numbers']['p1'],
#                  "p2_numbers": loaded['numbers']['p2'],
#                  "p1_strings": loaded['strings']['p1'],
#                  "p2_strings": loaded['strings']['p2']
#                 }
#     except Exception as inst:
#         print("err", inst)
def tail_input_file():
    try:
        result = subprocess.Popen(
            # This eventually should be a environment variable
            # "/home/mia_bobia/Downloads/Fightcade-linux-latest/Fightcade/emulator/fbneo/scripts/state_dump_bools.json"
            "tail -n 1 /home/nbee/Downloads/Fightcade/emulator/fbneo/scripts/test_ram_dumper_state_dump.json",
            shell=True, stdout=subprocess.PIPE
        ).stdout.read().decode('UTF-8')

        split = result.split('\r\n')
        loaded = json.loads(split[0])
        print(loaded)
        return loaded
        # return { "p1_bools": loaded['bools']['p1'],
        #          "p2_bools": loaded['bools']['p2'],
        #          "p1_numbers": loaded['numbers']['p1'],
        #          "p2_numbers": loaded['numbers']['p2'],
        #          "p1_strings": loaded['strings']['p1'],
        #          "p2_strings": loaded['strings']['p2']
        #         }
    except Exception as inst:
        print("err", inst)
def bools_to_rects(vals: dict, origin: tuple) -> List[pygame.rect.Rect]:
    if vals is None:
        return ''

    print("Num bools", len(vals))
    rects = []
    rect_w, rect_h = BAR_WIDTH, SCREEN_HEIGHT//len(vals)
    x, y = origin
    index = 0

    for _, val in vals.items():
        r = pygame.rect.Rect(
            x,
            y + (index*rect_h),
            rect_w,
            rect_h
        )
        r_color = (0, 255, 0)
        if not val:
            r_color = (255, 0, 0)
        rects.append((r, r_color))
        index += 1

    return rects

def num_to_rects(vals: dict, origin: tuple) -> List[pygame.rect.Rect]:
    if vals is None:
        return ''
    print("Int values", len(vals))
    rects = []
    rect_w, rect_h = 10, 1


    #   __________________
    #  |                  |
    #  |                  |
    #  |                  |
    #  |                  |
    #  |                  |
    #  --------------------

    x, y = origin
    index = 0

    for _, val in vals.items():
        r = pygame.rect.Rect(
            x + index*rect_w,
            y,
            rect_w,
            y + val*rect_h,
        )

        r_color = (50, 60, 190)

        rects.append((r, r_color))

        index +=1
    
    return rects



def json_number_stats(vals: dict):
    global max_number
    global min_number
    global avg_number
    global avg_number_len

    avg_number_len += 1
    min_non_zero = filter(lambda x: x > 0, vals.values())

    max_number = max(max(vals.values()), max_number)
    min_number = min(min(min_non_zero), min_number)
    avg_numbers.add(sum(vals.values())//len(vals))

    print(f'MAX: {max_number}\nMIN: {min_number}\nAVG: {sum(avg_numbers)/len(avg_numbers)}')


# Initialize Pygame
pygame.init()


# Setup the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("🧛VSAV_VIZ!🧛")

# Colors
WHITE = (255, 255, 255)

# Clock to control the frame rate
clock = pygame.time.Clock()

data_time_passed = 500
read_interval = 50 # milliseconds
read_time = 0

# Main game loop
def main():
    global data_time_passed, read_interval, read_time
    running = True
    data_was_read = False
    i = 0
    rects = []
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        if data_time_passed >= read_interval:
            data = tail_input_file()
            data_time_passed = 0
            read_time = pygame.time.get_ticks()
            data_was_read = True
        else:
            data_time_passed = pygame.time.get_ticks() - read_time
            data_was_read = False

        if data and data_was_read:
            pass 
            # rects = bools_to_rects(data["p1_bools"], (0, 0))
            # rects.extend(bools_to_rects(data["p2_bools"], (SCREEN_WIDTH - BAR_WIDTH,0)))
            # # This would display the values as heights of a bar
            # rects.extend(num_to_rects(data['p1_numbers'], (0, 0)))
            # rects.extend(num_to_rects(data['p2_numbers'], (60, 0))) 

        # Drawing
        screen.fill(WHITE)  # Clear the screen with a white background
        # cut the screen in two
        pygame.draw.line(screen, (0,0,0), (SCREEN_WIDTH//2, 0), (SCREEN_WIDTH//2,SCREEN_HEIGHT), 4)

        if rects:
            for r, color in rects:
                # print(type(rect))
                pygame.draw.rect(screen, color, (r.left, r.top, r.width, r.height))

        pygame.display.flip()  # Update the display
        clock.tick(FPS)  # Maintain the frame rate

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    # print(tail_input_file()["p1_strings"])
    # print(tail_input_file()["p2_strings"])
    main()
