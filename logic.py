import pygame
import sys
import random

class Cell:
    def __init__(self):
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.neighbor_mines = 0
        self.clicked_mine = False

class Minesweeper:
    def __init__(self, cfg):
        self.cfg = cfg
        
        self.screen = pygame.display.set_mode((self.cfg.SCREEN_WIDTH, self.cfg.SCREEN_HEIGHT))
        pygame.display.set_caption("Minesweeper")

        #Load the images
        self.cfg.load_all_assets()
        
        self.clock = pygame.time.Clock()
        self.font_big   = pygame.font.SysFont("Arial", 24, bold=True)
        self.font_small = pygame.font.SysFont("Arial", 14)
        self.reset()

    def reset(self):
        self.grid = [[Cell() for _ in range(self.cfg.COLS)] for _ in range(self.cfg.ROWS)]
        self.state = self.cfg.STATE_PLAYING
        self.first_click = True
        self.flags_placed = 0
        self.start_ticks = None
        self.time = 0

    def place_mines(self, safe_row, safe_col):
        #Place mines after the first click, so the first cell is safe.
        all_cells = [(r, c) for r in range(self.cfg.ROWS) for c in range(self.cfg.COLS) if not (r == safe_row and c == safe_col)]
        mine_positions = random.sample(all_cells, self.cfg.MINES)
        for r, c in mine_positions:
            self.grid[r][c].is_mine = True
        self._calculate_neighbours()
    
    def _calculate_neighbours(self):
        for r in range(self.cfg.ROWS):
            for c in range(self.cfg.COLS):
                if not self.grid[r][c].is_mine:
                    count = 0
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            nr, nc = dr + r, dc + c
                            if 0 <= nr < self.cfg.ROWS and 0 <= nc < self.cfg.COLS:
                                if self.grid[nr][nc].is_mine:
                                    count += 1
                    self.grid[r][c].neighbor_mines = count

    def place_flag(self, row, col):
        cell = self.grid[row][col]
        if cell.is_revealed:
            return
        if cell.is_flagged:
            cell.is_flagged = False
            self.flags_placed -= 1
        else:
            cell.is_flagged = True
            self.flags_placed += 1

    def get_cell_from_mouse(self, mx, my):
        if my < self.cfg.HEADER_HEIGHT:
            return None, None
        col = mx // self.cfg.TILE_SIZE
        row = (my - self.cfg.HEADER_HEIGHT) // self.cfg.TILE_SIZE
        if 0 <= row < self.cfg.ROWS and 0 <= col < self.cfg.COLS:
            return row, col
        return None, None
    
    def reveal(self, row, col):
        cell = self.grid[row][col]
        if cell.is_revealed or cell.is_flagged:
            return
        cell.is_revealed = True
        if cell.is_mine:
            cell.clicked_mine = True
            self._lose()
            return
        
        if cell.neighbor_mines == 0:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < self.cfg.ROWS and 0 <= nc < self.cfg.COLS:
                        if not self.grid[nr][nc].is_revealed:
                            self.reveal(nr, nc)

    def chord(self, row, col):
        cell = self.grid[row][col]
        if not cell.is_revealed or cell.neighbor_mines == 0:
            return
        flag_count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = row + dr, col + dc
                if 0 <= nr < self.cfg.ROWS and 0 <= nc < self.cfg.COLS:
                    if self.grid[nr][nc].is_flagged:
                        flag_count += 1
        if flag_count == cell.neighbor_mines:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < self.cfg.ROWS and 0 <= nc < self.cfg.COLS:
                        if not self.grid[nr][nc].is_flagged:
                            self.reveal(nr, nc)


    def _lose(self):
        self.state = self.cfg.STATE_LOST
        # Reveal all mines
        for r in range(self.cfg.ROWS):
            for c in range(self.cfg.COLS):
                cell = self.grid[r][c]
                if cell.is_mine and not cell.is_flagged:
                    cell.is_revealed = True
                elif not cell.is_mine and cell.is_flagged:
                    cell.is_revealed = True 


    def draw_grid(self):
        for r in range(self.cfg.ROWS):
            for c in range(self.cfg.COLS):
                x = c * self.cfg.TILE_SIZE
                y = r * self.cfg.TILE_SIZE + self.cfg.HEADER_HEIGHT
                cell = self.grid[r][c]
                
                if not cell.is_revealed:
                    if cell.is_flagged:
                        self.screen.blit(self.cfg.spr_flag, (x, y))
                    else:
                        self.screen.blit(self.cfg.spr_grid, (x, y))
                else:
                    if cell.is_mine:
                        if cell.clicked_mine:
                            self.screen.blit(self.cfg.spr_mineClicked, (x, y))
                        else:
                            self.screen.blit(self.cfg.spr_mine, (x, y))
                    elif not cell.is_mine and cell.is_flagged:
                        self.screen.blit(self.cfg.spr_mineFalse, (x, y))
                    else:
                        self.screen.blit(self.cfg.NUMBER_SPRITES[cell.neighbor_mines], (x, y))

    def draw_header(self):
        pygame.draw.rect(self.screen, self.cfg.Colors.COLOR_BG, (0, 0, self.cfg.SCREEN_WIDTH, self.cfg.HEADER_HEIGHT))
        pygame.draw.rect(self.screen, self.cfg.Colors.COLOR_DARK,  (0, 0, self.cfg.SCREEN_WIDTH, self.cfg.HEADER_HEIGHT), 3)

        # Timer
        if self.start_ticks and self.state == self.cfg.STATE_PLAYING:
            self.time = (pygame.time.get_ticks() - self.start_ticks) // 1000
        timer_text = self.font_big.render(f"{min(self.time, 999):03d}", True, (255, 0, 0))
        self.screen.blit(timer_text, (self.cfg.SCREEN_WIDTH - 60, 15))


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos

                    row, col = self.get_cell_from_mouse(mx, my)

                    if row is None:
                        continue

                    if event.button == 1:
                        if self.first_click:
                            self.first_click = False
                            self.place_mines(row, col)
                            self.start_ticks = pygame.time.get_ticks()
                        cell = self.grid[row][col]
                        if cell.is_revealed:
                            self.chord(row, col)
                        else:
                            self.reveal(row, col)
                    elif event.button == 3:
                        if not self.first_click:
                            self.place_flag(row, col)



            self.screen.fill(self.cfg.Colors.COLOR_BG)
            self.draw_header()
            self.draw_grid()
            pygame.display.flip()
            self.clock.tick(60)
