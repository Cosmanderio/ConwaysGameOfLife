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
        pygame.draw.circle(window, WHITE if self.is_clicked else LIGHT_GRAY, (self.x, self.y), 8)
        
    def update(self):
        if self.is_clicked:
            if mouse[0] > 0:
                global simulation_speed
                simulation_speed = max(1, min(MAX_SPEED, round((mouse[1]-window_size[0]//2+self.range//2)*MAX_SPEED/self.range)))
                self.last_mouse_x = pygame.mouse.get_pos()[0]
            else:
                self.is_clicked = False
        self.x = window_size[0]//2-self.range//2+round(simulation_speed/MAX_SPEED*self.range)
        
    def onMouseClick(self, x, y):  # Clic de la souris
        if (self.x-x)**2+(self.y-y)**2 <= 64:
            self.is_clicked = True
            self.last_mouse_x = x
            return True
        return False
    

# Définition des fonctions

def simulateCells():  # Simule les cellules
    neighbors = dict((living_cell, 0) for living_cell in living_cells)
    for x, y in living_cells:  # On compte le nombre de voisins de chaque cellule en possèdant au moins 1
        for dx, dy, in NEIGHBORS:
            try:
                neighbors[(x+dx, y+dy)] += 1
            except KeyError:
                neighbors[(x+dx, y+dy)] = 1
    
    for i in range(len(living_cells)-1, -1, -1):  # On tue les cellules vivantes n'ayant pas un nombre de voisins entre 2 et 3
        if not 2 <= neighbors[living_cells[i]] <= 3:
            living_cells.pop(i)

    for cell in neighbors:  # On fait naitre les nouvelles cellules qui possèdent 3 voisins
        if neighbors[cell] == 3 and cell not in living_cells:
            living_cells.append(cell)
                

def displayGrid(line_width):  # Affiche la grille
    for x in range(-((scroll_x-window_size[0]//2)%cell_size), window_size[0]+1, cell_size):
        pygame.draw.line(window, GRAY, (x, 0), (x, window_size[1]), line_width)
    for y in range(-((scroll_y-window_size[1]//2)%cell_size), window_size[1]+1, cell_size):
        pygame.draw.line(window, GRAY, (0, y), (window_size[0], y), line_width)
        

def displayCells():  # Affiche les cellules
    for i, j in living_cells:
        pygame.draw.rect(window, BLACK, (j*cell_size-scroll_x+window_size[0]//2, i*cell_size-scroll_y+window_size[1]//2, cell_size, cell_size))
                
                
def onMouseClick(nb_clicks, x, y):  # Clic de souris
    global brush
    if nb_clicks == 1 and speed_button.onMouseClick(x, y): return
    if simulating: return
    i = (y+scroll_y-window_size[1]//2) // cell_size
    j = (x+scroll_x-window_size[0]//2) // cell_size
    if nb_clicks == 1:
        brush = (i, j) in living_cells
    if brush:
        if (i, j) in living_cells:
            living_cells.remove((i, j))
    elif (i, j) not in living_cells:
        living_cells.append((i, j))
        

def displayStats():  # Affiche le bandeau de statistique en haut de l'écran
    pygame.draw.rect(window, BLACK, (window_size[0]//2-210, -40, 420, 110), border_radius=40)
    txt = font.render(f"Vitesse de simulation : {simulation_speed} ticks/s", True, WHITE)
    txt_size = txt.get_size()
    window.blit(txt, (window_size[0]//2-txt_size[0]//2, 20-txt_size[1]//2))
    pygame.draw.rect(window, LIGHT_GRAY, (window_size[0]//2-160, 48, 320, 5), border_radius=2)
    speed_button.display()
    
    
def changeCellSize(value):  # Zoom / Dezoom
    global cell_size, scroll_x, scroll_y
    real_scroll_x = scroll_x / cell_size
    real_scroll_y = scroll_y / cell_size
    cell_size = round(cell_size * 1.1**value)
    scroll_x = round(real_scroll_x*cell_size)
    scroll_y = round(real_scroll_y*cell_size)
            

pygame.init()  # Initiation de pygame

# Définition des couleurs

WHITE = (255, 255, 255)
LIGHT_GRAY = (220, 220, 220)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)

# Création de la fenêtre et autres

window_size = (800, 600)
window = pygame.display.set_mode(window_size, pygame.RESIZABLE)
pygame.display.set_caption("Conway's Game of Life")
clock = pygame.time.Clock()

font = pygame.font.SysFont("arial", 24)

cell_size = 40
living_cells = []  # Stocke la liste des coordonnées (x, y) de chaque cellule vivante
NEIGHBORS = ((-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1), (1, -1))
simulating = False
simulation_speed = 5
MAX_SPEED = 100
speed_button = RangeButton(50, 320)
mouse = [0, 0, 0]  # Informations sur la souris : [durée du clic, x, y]
LOOP_SPEED = 30
simulation_loop_ticks = 0
main_loop_ticks = 0
scroll_x = 0
scroll_y = 0
keys = dict((key, 0) for key in (pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_LEFT, pygame.K_SPACE, pygame.K_LSHIFT))
brush = False

running = True

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

        for key in keys:
            if keys[key] > 0:
                keys[key] += 1
            
        for event in pygame.event.get():  # Boucle d'évènements
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in keys:
                    keys[event.key] = 1
            elif event.type == pygame.KEYUP:
                if event.key in keys:
                    keys[event.key] = 0
            elif event.type == pygame.MOUSEWHEEL:
                changeCellSize(event.y)
                    
        # Mise à jour des données

        if keys[pygame.K_SPACE] == 1:
            simulating = not simulating

        scroll_x += ((keys[pygame.K_RIGHT] > 0) - (keys[pygame.K_LEFT] > 0)) * (30 if keys[pygame.K_LSHIFT] > 0 else 14)
        scroll_y += ((keys[pygame.K_UP] > 0) - (keys[pygame.K_DOWN] > 0)) * (-30 if keys[pygame.K_LSHIFT] > 0 else -14)
                    
        mouse[1], mouse[2] = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            mouse[0] += 1
        else:
            mouse[0] = 0
        window_size = window.get_size()
        
        if mouse[0] > 0:
            onMouseClick(*mouse)
            
        speed_button.update()
                
        # Affichage
        
        window.fill(WHITE)  # Efface l'écran
        
        if not simulating:
            displayGrid(3)
        displayCells()
        displayStats()
        
        pygame.display.flip() # Actualise l'écran
    
    clock.tick(MAX_SPEED)  # Limite la boucle à 'MAX_SPEED' ticks / seconde

pygame.quit()  # Fermeture de la fenêtre
