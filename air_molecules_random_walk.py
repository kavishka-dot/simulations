import pygame
import random

pygame.init()


WIDTH, HEIGHT = 800, 800
TILE_SIZE = 5
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE

FPS = 180

screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

# initially air molecules will be distributed in a limited space
def gen(num):
    return set([(random.randrange((GRID_HEIGHT//2 - 20),(GRID_HEIGHT//2 + 20)), random.randrange((GRID_WIDTH//2 -20), (GRID_WIDTH//2 +20))) for _ in range(num)])

def adjust_grid(positions):
    new_positions = set()
    positions = list(positions)

    directions = [(1,0), (0,1),(-1,0),(0,-1),(1,1), (1,-1),(-1,1),(-1,-1)]

    i = 0

    while i < len(positions):
        pos = positions[i]
        x_c, y_c = local_concentartion(pos, positions,3)
        if x_c == 0 and y_c ==0:
            rand_dir = random.choice(directions)
        else:
            # normalize the direction of the gradient 
            if x_c == 0 and y_c != 0:
                x_c, y_c = 0, y_c/abs(y_c)
            if y_c ==0 and x_c != 0:
                x_c, y_c = x_c/abs(x_c), 0
            if x_c != 0 and y_c != 0:
                x_c, y_c = x_c/abs(x_c), y_c/abs(y_c)

            # add a high probability of moving in the opposite direction of the gradient
            rand_dir = random.choice(directions+[(-x_c, -y_c) ]*16)
        
        new_pos = (pos[0]+rand_dir[0], pos[1]+rand_dir[1])

        # check if the new position is already in the set of next positions to avoid collisions
        if new_pos not in new_positions:
            new_positions.add(new_pos)
            i+=1

    return new_positions

# calculate the direction of concentration within a local window 
def local_concentartion(pos,positions,window=3):
    x, y = pos

    x_c, y_c = (0,0)

    for dx in range(-window,window+1):
        if x + dx <0 or x + dx > GRID_WIDTH:
            continue
        for dy in range(-window,window+1):
            if y + dy < 0 or y + dy > GRID_HEIGHT:
                continue
            if dx == 0 and dy == 0:
                continue

            # calculate the direction of the gradient
            if (x + dx, y + dy) in positions:
                x_c += dx
                y_c += dy
    return (x_c, y_c)


def draw_grid(positions):
    for position in positions:
        col, row = position
        top_left = (col * TILE_SIZE , row * TILE_SIZE)
        pygame.draw.circle(screen, "black", (*top_left,), 5)


def main():
    running = True
    positions = set()
    playing = False
    count = 0
    update_freq = 10

    while running:
        
        clock.tick(FPS)
        
        
        if playing:
            count += 1

        if count >= update_freq:
            count = 0
            
            positions = adjust_grid(positions)

        pygame.display.set_caption("Playing" if playing else "Pause")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                col = x // TILE_SIZE
                row = y // TILE_SIZE

                pos = (col, row)

                if pos in positions:
                    positions.remove(pos)
                else:
                    positions.add(pos)

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    playing = not playing

                if event.key == pygame.K_c:
                    positions = set()
                    playing = False
                    count = 0
                    
                if event.key == pygame.K_g:
                    positions = gen(random.randrange(1,2)* GRID_WIDTH)


        
        screen.fill("gray")
        draw_grid(positions)

        pygame.display.update()
    
    pygame.quit()

if __name__ == "__main__":
    main()