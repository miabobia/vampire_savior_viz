
# extend class and overwrite str method to make into hex

# visualizer.py
import pygame
import sys
from multiprocessing import Queue
from typing import Dict, List, Tuple, Optional
import logging
from schedule_test import start_scheduler
from random import randint

class Visualizer:
    def __init__(self, width: int = 800, height: int = 600, fps: int = 60, poll_rate: int = 5):
        pygame.init()
        pygame.font.init()
        
        self.width = width
        self.height = height
        self.fps = fps
        self.poll_rate = poll_rate
        
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Data Visualizer")
        
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 30)
        
        self.running = True
        self.tick = 0
        self.current_data: Optional[Dict] = None
        
    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update_data(self, queue: Queue) -> None:
        try:
            while not queue.empty():
                self.current_data = queue.get_nowait()
        except Exception as e:
            logging.error(f"Error updating data: {e}")

    def str_to_hex(self, s: str) -> str:
        return s.encode("utf-8").hex()

    def draw(self) -> None:
        self.screen.fill((255, 255, 255))  # White background
        RECT_W, RECT_H = 50, 50
        if self.current_data:
            # Example visualization - modify based on your data structure
            y_position = 50
            for i, (key, val) in enumerate(self.current_data.items()):
                # print(key, val)
                # print(self.str_to_h/ex(key), key)


                if key != '16745479': continue # action counter
                # if key != '16745476': continue # animation counter
                print(key, val)
                # c = min(255, i)
                # if val > 255:
                #     print(key, val)
                c = val * 4
                # co = (250, 100, c)
                co = (c,c,c)
                w = val * 50
                h = val * 50
                pygame.draw.rect(self.screen, co, rect=[0,0,w,h])

        
        pygame.display.flip()

    def run(self, queue: Queue) -> None:
        while self.running:
            self.tick += 1
            
            if self.tick % self.poll_rate == 0:
                self.update_data(queue)
                self.tick = 0
            
            self.handle_events()
            self.draw()
            self.clock.tick(self.fps)
        
        pygame.quit()
        sys.exit()

def main():
    # Configuration
    FILE_PATH = "/home/mia_bobia/Downloads/Fightcade-linux-latest/Fightcade/emulator/fbneo/scripts/testlua.json"
    
    try:
        queue = Queue()
        scheduler = start_scheduler(queue, FILE_PATH)
        
        visualizer = Visualizer()
        visualizer.run(queue)
        
    except KeyboardInterrupt:
        logging.info("Application terminated by user")
    except Exception as e:
        logging.error(f"Application error: {e}")
    finally:
        if 'scheduler' in locals():
            scheduler.shutdown()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()