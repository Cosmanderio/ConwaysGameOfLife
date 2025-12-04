# Importation des librairies

import pygame

pygame.init()  # Initiation de pygame

# Définition des couleurs

BLANC = (255, 255, 255)

# Création de la fenêtre et autres

fenetre = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
pygame.display.set_caption("Conway's Game of Life")
clock = pygame.time.Clock()

running = True

# Boucle principale

while running:

    for event in pygame.event.get():  # Boucle d'évènements
        if event.type == pygame.QUIT:
            running = False
    
    fenetre.fill(BLANC)  # Efface l'écran
    pygame.display.flip() # Actualise l'écran
    clock.tick(20)  # Limite la boucle à 20 ticks / seconde

pygame.quit()  # Fermeture de la fenêtre
