import pygame
from logic import Minesweeper


class GameConfig:


    TILE_SIZE = 50
    COLS = 12
    ROWS = 12
    MINES = 20

    SCREEN_WIDTH = COLS * TILE_SIZE
    HEADER_HEIGHT = 60
    SCREEN_HEIGHT = ROWS * TILE_SIZE + HEADER_HEIGHT    

    # Game states
    STATE_PLAYING = 0
    STATE_WON = 1
    STATE_LOST = 2

    def __init__(self):
        self.spr_emptyGrid = None
        self.spr_flag = None
        self.spr_grid = None
        self.spr_mine = None
        self.spr_mineClicked = None
        self.spr_mineFalse = None
        self.NUMBER_SPRITES = []

    @staticmethod
    def load_sprite(path, size):
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (size, size))

    def load_all_assets(self):
        """Call this ONLY after pygame.display.set_mode()"""
        ts = self.TILE_SIZE
        
        self.spr_emptyGrid = self.load_sprite("icons/empty.png", ts)
        self.spr_flag      = self.load_sprite("icons/flag.png", ts)
        self.spr_grid      = self.load_sprite("icons/Grid.png", ts)
        self.spr_mine      = self.load_sprite("icons/mine.png", ts)
        self.spr_mineClicked = self.load_sprite("icons/mine_clicked.png", ts)
        self.spr_mineFalse = self.load_sprite("icons/mine_false.png", ts)

        self.NUMBER_SPRITES = [
            self.spr_emptyGrid,
            self.load_sprite("icons/grid1.png", ts),
            self.load_sprite("icons/grid2.png", ts),
            self.load_sprite("icons/grid3.png", ts),
            self.load_sprite("icons/grid4.png", ts),
            self.load_sprite("icons/grid5.png", ts),
            self.load_sprite("icons/grid6.png", ts),
            self.load_sprite("icons/grid7.png", ts),
            self.load_sprite("icons/grid8.png", ts)
        ]

    class Colors:
        COLOR_BG = (189, 189, 189)
        COLOR_DARK = (128, 128, 128)
        COLOR_LIGHT = (255, 255, 255)
        COLOR_TEXT = (0, 0, 0)
        GREEN = (0, 200, 0, 80)
        RED = (200, 0, 0, 80)



if __name__ == "__main__":
    pygame.init()

    cfg = GameConfig()
    game = Minesweeper(cfg)

    game.run()