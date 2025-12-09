# Importation des librairies

import pygame


class RangeButton:  # Class du bouton de vitesse de simulation
    
    def __init__(self, y, button_range):
        self.is_clicked = False
        self.range = button_range
        self.x = 0
        self.y = y
        
    def display(self):  # Affiche le bouton
        self.update()
        pygame.draw.circle(fenetre, WHITE if self.is_clicked else LIGHT_GRAY, (self.x, self.y), 8)
        
    def update(self):
        if self.is_clicked:
            if mouse[0] > 0:
                global simulation_speed
                simulation_speed = max(1, min(MAX_SPEED, round((mouse[1]-fenetre_size[0]//2+self.range//2)*MAX_SPEED/self.range)))
                self.last_mouse_x = pygame.mouse.get_pos()[0]
            else:
                self.is_clicked = False
        self.x = fenetre_size[0]//2-self.range//2+round(simulation_speed/MAX_SPEED*self.range)
        
    def onMouseClick(self, x, y):  # Clic de la souris
        if (self.x-x)**2+(self.y-y)**2 <= 64:
            self.is_clicked = True
            self.last_mouse_x = x
            return True
        return False
    

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
    if speed_button.onMouseClick(x, y): return
    if simulating: return
    i = y // cell_size
    j = x // cell_size
    if 0 <= i < len(grid) and 0 <= j < len(grid[0]):
        grid[i][j] = not grid[i][j]
        
        
def greenToRed(percent):  # Renvoie une couleur RGB entre vert et rouge dépendant du pourcentage
    if percent > 50:
        return (255, 255-round(5.1*(percent-50)), 0)
    return (round(5.1*percent), 255, 0)
        

def displayStats():  # Affiche le bandeau de statistique en haut de l'écran
    pygame.draw.rect(fenetre, BLACK, (fenetre_size[0]//2-210, -40, 420, 110), border_radius=40)
    txt = font.render(f"Vitesse de simulation : {simulation_speed} ticks/s", True, WHITE)
    txt_size = txt.get_size()
    fenetre.blit(txt, (fenetre_size[0]//2-txt_size[0]//2, 20-txt_size[1]//2))
    pygame.draw.rect(fenetre, LIGHT_GRAY, (fenetre_size[0]//2-160, 48, 320, 5), border_radius=2)
    speed_button.display()
            

pygame.init()  # Initiation de pygame

# Définition des couleurs

WHITE = (255, 255, 255)
LIGHT_GRAY = (220, 220, 220)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)

# Création de la fenêtre et autres

fenetre_size = (800, 600)
fenetre = pygame.display.set_mode(fenetre_size, pygame.RESIZABLE)
pygame.display.set_caption("Conway's Game of Life")
clock = pygame.time.Clock()

font = pygame.font.SysFont("arial", 24)

cell_size = 40
grid = [[False]*20 for _ in range(15)]  # Représente la grille de cellules : True = vivante, False = morte
simulating = False
simulation_speed = 5
MAX_SPEED = 100
speed_button = RangeButton(50, 320)
mouse = [0, 0, 0]  # Informations sur la souris : [durée du clique, x, y]
LOOP_SPEED = 20
simulation_loop_ticks = 0
main_loop_ticks = 0

running = True

# Boucle principale

while running:
        
    # Boucle de simulation
    
    if simulating:
        simulation_loop_ticks += 1
        if simulation_loop_ticks >= MAX_SPEED / simulation_speed:
            simulation_loop_ticks -= MAX_SPEED / simulation_speed
            simulateCells()
        
    # Boucle principale
    
    main_loop_ticks += 1
    
    if main_loop_ticks >= MAX_SPEED / LOOP_SPEED:
        main_loop_ticks -= MAX_SPEED / LOOP_SPEED
            
        for event in pygame.event.get():  # Boucle d'évènements
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    simulating = not simulating
                    
        # Mise à jour des données
                    
        mouse[1], mouse[2] = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            mouse[0] += 1
        else:
            mouse[0] = 0
        fenetre_size = fenetre.get_size()
        
        if mouse[0] == 1:
            onMouseClick(*mouse[1:3])
            
        speed_button.update()
                
        # Affichage
        
        fenetre.fill(WHITE)  # Efface l'écran
        
        if not simulating:
            displayGrid(3)
        displayCells()
        displayStats()
        
        pygame.display.flip() # Actualise l'écran
    
    clock.tick(MAX_SPEED)  # Limite la boucle à 'MAX_SPEED' ticks / seconde

pygame.quit()  # Fermeture de la fenêtre
