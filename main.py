# Importation des librairies

import pygame

# Définition des fonctions

def countLivingNeighbors(x, y, matrix):  # Retourne le nombre de voisins vivants d'une cellule
    c = 0
    for x2 in range(max(x-1, 0), min(x+2, len(matrix[0]))):
        for y2 in range(max(y-1, 0), min(y+2, len(matrix))):
            if matrix[y2][x2] and (x != x2 or y != y2):
                c += 1
    return c


def simulateCells():  # Simule les cellules
    last = [line.copy() for line in grid]
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            living_neighbors = countLivingNeighbors(j, i, last)
            if grid[i][j]:
                grid[i][j] = 2 <= living_neighbors <= 3
            else:
                grid[i][j] = living_neighbors == 3
                

def displayGrid(line_width):  # Affiche la grille
    for x in range(0, 801, cell_size):
        pygame.draw.line(fenetre, GRAY, (x, 0), (x, 600), line_width)
    for y in range(0, 601, cell_size):
        pygame.draw.line(fenetre, GRAY, (0, y), (800, y), line_width)
        

def displayCells():  # Affiche les cellules
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j]:
                pygame.draw.rect(fenetre, BLACK, (j*cell_size, i*cell_size, cell_size, cell_size))
                
                
def onMouseClick(x, y):  # Clic de souris
    if simulating: return
    i = y // cell_size
    j = x // cell_size
    if 0 <= i < len(grid) and 0 <= j < len(grid[0]):
        grid[i][j] = not grid[i][j]
            

pygame.init()  # Initiation de pygame

# Définition des couleurs

WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)

# Création de la fenêtre et autres

fenetre = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
pygame.display.set_caption("Conway's Game of Life")
clock = pygame.time.Clock()

cell_size = 40
grid = [[False]*20 for _ in range(15)]  # Représente la grille de cellules : True = vivante, False = morte
simulating = False

running = True

# Boucle principale

while running:

    for event in pygame.event.get():  # Boucle d'évènements
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                simulating = not simulating
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                onMouseClick(*event.pos)
            
    # Traitement des données
            
    if simulating:
        simulateCells()
            
    # Affichage
    
    fenetre.fill(WHITE)  # Efface l'écran
    
    if not simulating:
        displayGrid(3)
    displayCells()
    
    pygame.display.flip() # Actualise l'écran
    clock.tick(5)  # Limite la boucle à 20 ticks / seconde

pygame.quit()  # Fermeture de la fenêtre
