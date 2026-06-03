import pygame
import numpy as np
from math import radians as rad
import random

# Ball
class Ball:
    def __init__(self, WIDTH, HEIGHT, clr):

        # Attributes
        self.BALL_POS = np.array([WIDTH / 2, HEIGHT / 2 - 70], dtype=np.float64)
        self.BALL_COLOR = clr
        self.BALL_RADIUS = WIDTH / 80
        self.BALL_VEL = np.array([random.choice([-1, -2, -3, -4, 1, 2, 3, 4, 0]), random.choice([-1, -2, -3, -4, 1, 2, 3, 4, 0])], dtype=np.float64)
        self.POSLIST = []
        self.POINTLIST = []
        self.rainbow = pygame.Color(0)
        self.rainbow.hsva = [self.BALL_COLOR, 100, 100, 100]

# The APP
class App:
    def __init__(self, spin_: bool, gap: int, spn_chnge: bool, trail: bool, trail_len: int, init_clr: int,
                 balls: int, grvty: float, clrchange: bool, szchange: bool, melody: list[str], connect: bool, grvtchange: bool, grvtdelta: float):

        # Initializing
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Ball Simulation")
        WIDTH, HEIGHT = 400, 400
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        clock = pygame.time.Clock()
        running = True

        # Info
        CIRCLE_POS = np.array([WIDTH / 2, HEIGHT / 2], dtype=np.float64)
        CIRCLE_COLOR = [255, 255, 255]
        CIRCLE_RADIUS = WIDTH / 3
        GRAVITY = grvty
        Balls = [Ball(WIDTH, HEIGHT, init_clr) for _ in range(balls)]
        Fallen = []

        # Spinning
        if spin_:
            stopping = 180 - gap
            starting = 180
        else:
            stopping = 0
            starting = 0

        # The Melody
        GAMELIST = melody
        i = 0

        # Game LOOP
        while running:

            current_ticks = pygame.time.get_ticks()

            # Loop Variable 1: event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            screen.fill("BLACK")
            
            for a in Fallen:
                a.BALL_VEL[1] += GRAVITY
                a.BALL_POS += a.BALL_VEL

            # Loop Variable 2: n (Consolidated primary loop for single-ball updates and drawing)
            for n in list(Balls):

                # Physics movements
                n.BALL_VEL[1] += GRAVITY
                n.BALL_POS += n.BALL_VEL



                # Boundaries and arc checking
                dist = np.linalg.norm(n.BALL_POS - CIRCLE_POS)
                if dist + n.BALL_RADIUS > CIRCLE_RADIUS:
                    NORMAL = n.BALL_POS - CIRCLE_POS
                    NORMAL_HAT = NORMAL / np.linalg.norm(NORMAL)
                    if spin_:
                        angle = np.degrees(np.arctan2(NORMAL[1], -NORMAL[0]))
                        angle += 180

                        if starting < stopping:
                            good = starting < angle < stopping
                        else:
                            good = angle > starting or angle < stopping

                        if good:
                            n.POINTLIST.append(n.BALL_POS.copy())
                            TANGENT = np.array([-NORMAL[1], NORMAL[0]], dtype=np.float64)
                            n.BALL_POS = CIRCLE_POS + (CIRCLE_RADIUS - n.BALL_RADIUS) * NORMAL_HAT
                            PROJ_NT = (np.dot(n.BALL_VEL, TANGENT) / np.dot(TANGENT, TANGENT)) * TANGENT

                            n.BALL_VEL = 2 * PROJ_NT - n.BALL_VEL
                            if i >= len(melody): i = 0
                            if melody:
                                pygame.mixer.Sound("Notes/" + GAMELIST[i] + "_square_quaver.wav").play()
                            i += 1

                            if szchange:
                                CIRCLE_RADIUS -= 1

                            for q in n.POINTLIST:
                                direction = q - CIRCLE_POS
                                direction /= np.linalg.norm(direction)
                                q[:] = CIRCLE_POS + direction * (CIRCLE_RADIUS - 1)

                            if grvtchange:
                                GRAVITY += grvtdelta

                        else:
                            Fallen.append(n)
                            Balls.remove(n)

                            continue

                    else:
                        n.POINTLIST.append(n.BALL_POS.copy())
                        TANGENT = np.array([-NORMAL[1], NORMAL[0]], dtype=np.float64)
                        n.BALL_POS = CIRCLE_POS + (CIRCLE_RADIUS - n.BALL_RADIUS) * NORMAL_HAT
                        PROJ_NT = (np.dot(n.BALL_VEL, TANGENT) / np.dot(TANGENT, TANGENT)) * TANGENT

                        n.BALL_VEL = 2 * PROJ_NT - n.BALL_VEL
                        if i >= len(melody): i = 0
                        if melody:
                            pygame.mixer.Sound("Notes/" + GAMELIST[i] + "_square_quaver.wav").play()
                        i += 1

                        if szchange:
                            CIRCLE_RADIUS -= 1

                        for q in n.POINTLIST:
                            direction = q - CIRCLE_POS
                            direction /= np.linalg.norm(direction)
                            q[:] = CIRCLE_POS + direction * (CIRCLE_RADIUS - 1)

                        if grvtchange:
                            GRAVITY += 0.002


                # Drawing base ball
                pygame.draw.circle(screen, n.rainbow, n.BALL_POS, n.BALL_RADIUS)

                # Trail tracking and drawing
                if trail and not szchange:
                    if len(n.POSLIST) > trail_len:
                        n.POSLIST.pop(0)
                    n.POSLIST.append((n.BALL_POS.copy(), n.rainbow))
                    for j in n.POSLIST:
                        pygame.draw.circle(screen, j[1], j[0], n.BALL_RADIUS)

                # Connection lines
                if connect:
                    for k in n.POINTLIST:
                        pygame.draw.line(screen, n.rainbow, k - np.array([0, 4], dtype=np.float64), n.BALL_POS.copy(), 3)

                # Color shifting
                if clrchange:
                    n.BALL_COLOR += 0.5
                    if n.BALL_COLOR >= 360:
                        n.BALL_COLOR = 0
                    n.rainbow.hsva = (n.BALL_COLOR, 100, 100, 100)

            for b in Fallen:
                # Trail tracking and drawing
                if trail and not szchange:
                    if len(b.POSLIST) > trail_len:
                        b.POSLIST.pop(0)
                    b.POSLIST.append((b.BALL_POS.copy(), b.rainbow))
                    for j in b.POSLIST:
                        pygame.draw.circle(screen, j[1], j[0], b.BALL_RADIUS)

                # Connection lines
                if connect:
                    for k in b.POINTLIST:
                        pygame.draw.line(screen, b.rainbow, k - np.array([0, 4], dtype=np.float64), b.BALL_POS.copy(),
                                         3)

                # Color shifting
                if clrchange:
                    b.BALL_COLOR += 0.5
                    if b.BALL_COLOR >= 360:
                        b.BALL_COLOR = 0
                    b.rainbow.hsva = (b.BALL_COLOR, 100, 100, 100)
                    
            # Loop Variable 3: idx (Handles multi-ball collisions alongside target peer 'u')
            for idx, t in enumerate(Balls):
                for u in Balls[idx + 1:]:
                    delta = t.BALL_POS - u.BALL_POS
                    d = np.linalg.norm(delta)

                    if d <= WIDTH / 40 and d != 0:
                        normal = delta / d
                        overlap = WIDTH / 40 - d
                        t.BALL_POS += normal * overlap / 2
                        u.BALL_POS -= normal * overlap / 2
                        rel_vel = t.BALL_VEL - u.BALL_VEL
                        Normal_VEL = np.dot(rel_vel, normal)

                        if Normal_VEL < 0:
                            impulse = Normal_VEL * normal
                            t.BALL_VEL -= impulse
                            u.BALL_VEL += impulse

            # Main environment container drawing
            if spin_:
                pygame.draw.arc(screen, CIRCLE_COLOR,
                                [float(CIRCLE_POS[0]) - CIRCLE_RADIUS, float(CIRCLE_POS[1]) - CIRCLE_RADIUS,
                                 CIRCLE_RADIUS * 2, CIRCLE_RADIUS * 2], rad(starting), rad(stopping), 5)
            else:
                pygame.draw.circle(screen, CIRCLE_COLOR, CIRCLE_POS, CIRCLE_RADIUS, 5)

            if spin_:
                starting += spn_chnge
                stopping += spn_chnge

            if starting >= 360:
                starting = 0

            if stopping >= 360:
                stopping = 0

            pygame.display.flip()
            clock.tick(100)

        pygame.quit()


if __name__ == "__main__":
    App(True,   30,
        0.1,    True,
        100,    180,2,
        0.1,    True, False,
        ["Ga", "Ga", "Ga", "Sa", "Ga", "Pa"],    False,
        True, 0)
