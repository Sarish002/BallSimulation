import pygame
import numpy as np

# Initialize
pygame.init()
pygame.display.set_caption("Ball Simulation")
WIDTH, HEIGHT = 400, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

# Info
CIRCLE_POS = np.array([WIDTH/2, HEIGHT/2], dtype=np.float64)
BALL_POS = np.array([WIDTH/2, HEIGHT/2 - 70], dtype=np.float64)

CIRCLE_COLOR = [255, 255, 255]
BALL_COLOR = 0

CIRCLE_RADIUS = WIDTH/3
BALL_RADIUS = WIDTH/80

GRAVITY = 0.2
BALL_VEL = np.array([4, 4], dtype=np.float64)

GAMELIST = ["Sa", "Sa", "Pa", "Pa", "Dha", "Dha", "Pa", "Ma", "Ma", "Ga", "Ga", "Re", "Re", "Sa",
            "Pa", "Pa", "Ma", "Ma", "Ga", "Ga", "Re", "Pa", "Pa", "Ma", "Ma", "Ga", "Ga", "Re",
            "Sa", "Sa", "Pa", "Pa", "Dha", "Dha", "Pa", "Ma", "Ma", "Ga", "Ga", "Re", "Re", "Sa"]
i = 0

POSLIST = []
POINTLIST = []

# Game Loop
while running:

    # Event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Moving Y
    BALL_VEL[1] += GRAVITY
    BALL_POS += BALL_VEL

    # Bouncing
    dist = np.linalg.norm(BALL_POS - CIRCLE_POS)
    if dist + BALL_RADIUS > CIRCLE_RADIUS:
        NORMAL = BALL_POS - CIRCLE_POS
        NORMAL_HAT = NORMAL/np.linalg.norm(NORMAL)
        TANGENT = np.array([-NORMAL[1], NORMAL[0]], dtype=np.float64)
        BALL_POS = CIRCLE_POS + (CIRCLE_RADIUS - BALL_RADIUS) * NORMAL_HAT
        POINTLIST.append(BALL_POS.copy())
        PROJ_NT = (np.dot(BALL_VEL, TANGENT)/np.dot(TANGENT, TANGENT)) * TANGENT

        # Music
        BALL_VEL = 2 * PROJ_NT - BALL_VEL
        if i >= 41: i = 0
        pygame.mixer.Sound("Notes/" + GAMELIST[i] + "_square_quaver.wav").play()
        i += 1

        # CIRCLE_RADIUS -= 1

        for k in POINTLIST:
            direction = k - CIRCLE_POS
            direction /= np.linalg.norm(direction)

            k[:] = CIRCLE_POS + direction * (CIRCLE_RADIUS - 2)

            k += np.array([2, 2], dtype=np.float64)



    screen.fill("BLACK")

    # Drawing the Circles
    rainbow = pygame.Color(0)
    rainbow.hsva = [BALL_COLOR, 100, 100, 100]

    pygame.draw.circle(screen, rainbow, BALL_POS, BALL_RADIUS)

    # Trail
    # if len(POSLIST) > 100:
    #    POSLIST.pop(0)

    # POSLIST.append((BALL_POS.copy(), rainbow))
    # for j in POSLIST:
    #    pygame.draw.circle(screen, j[1], j[0], BALL_RADIUS)

    for k in POINTLIST:
        pygame.draw.line(screen, rainbow, k, BALL_POS.copy(), 3)

    # Colors
    BALL_COLOR += 0.5
    if BALL_COLOR >= 360:
        BALL_COLOR = 0

    pygame.draw.circle(screen, CIRCLE_COLOR, CIRCLE_POS, CIRCLE_RADIUS, 5)

    # Ending
    pygame.display.flip()
    clock.tick(60)

# Quitting
pygame.quit()