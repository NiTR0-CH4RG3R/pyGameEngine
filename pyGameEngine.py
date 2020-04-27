#Created by Buddhima Zoysa on 27th of April 2020
#This is just a wrapper to pygame module (https://www.pygame.org) that provides funcionality like One Lone Coder's olcPixelGameEngine.h (which you can find here https://github.com/OneLoneCoder/olcPixelGameEngine)
#This may not be perfect I actually don't use python that often so there may be so many bugs and bad programming
#If someone find this useful go ahead download it experiment with it (And this only tested on windows)
#Good luck :)
#P.S. Sorry for my Bad English
#
#Dependancies : Just pygame module (to install pygame just run "pip install pygame")

from threading import Thread
import time
import math
import pygame
from pygame import gfxdraw

class pyGameEngine(Thread):
    Keys = {
        'A':pygame.K_a,
        'B':pygame.K_b,
        'C':pygame.K_c,
        'D':pygame.K_d,
        'E':pygame.K_e,
        'F':pygame.K_f,
        'G':pygame.K_g,
        'H':pygame.K_h,
        'I':pygame.K_i,
        'J':pygame.K_j,
        'K':pygame.K_k,
        'L':pygame.K_l,
        'M':pygame.K_m,
        'N':pygame.K_n,
        'O':pygame.K_o,
        'P':pygame.K_p,
        'Q':pygame.K_q,
        'R':pygame.K_r,
        'S':pygame.K_s,
        'T':pygame.K_t,
        'U':pygame.K_u,
        'V':pygame.K_v,
        'W':pygame.K_w,
        'X':pygame.K_x,
        'Y':pygame.K_y,
        'Z':pygame.K_z,
        '0':pygame.K_0,
        '1':pygame.K_1,
        '2':pygame.K_2,
        '3':pygame.K_3,
        '4':pygame.K_4,
        '5':pygame.K_5,
        '6':pygame.K_6,
        '7':pygame.K_7,
        '8':pygame.K_8,
        '9':pygame.K_9,
        'UP':pygame.K_UP,
        'DOWN':pygame.K_DOWN,
        'LEFT':pygame.K_LEFT,
        'RIGHT':pygame.K_RIGHT
    }

    def __init__(self):
        self.sAppName = 'Defualt'
        self.sIconPath = ''

    def Construct(self, nScreenWidth, nScreenHeight):
        self.nScreenWidth = nScreenWidth
        self.nScreenHeight = nScreenHeight
        pygame.init()
        self.screen = pygame.display.set_mode((self.nScreenWidth,self.nScreenHeight))
        if self.sIconPath != '':
            icon = pygame.image.load(self.sIconPath)
            pygame.display.set_icon(icon)
        self.bAtomRunning = True

    def ScreenHeight(self):
        return self.nScreenHeight

    def ScreenWidth(self):
        return self.nScreenWidth

    def SetPixel(self, x, y, color = (255, 255, 255)):
        x = int(x); y = int(y)
        if x >= 0 and x < self.nScreenWidth and y >= 0 and y < self.nScreenHeight:
            pygame.gfxdraw.pixel(self.screen,x,y,color)

    def DrawLine(self, x1, y1, x2, y2, color = (255, 255, 255)):
            if x1 > x2:
                x1, x2 = x2, x1
                y1, y2 = y2, y1

            dx = x2 - x1
            dy = y2 - y1

            if dx != 0:
                m = float(dy) / float(dx)
                for xi in range(dx + 1):
                    x = xi + x1
                    y = m * xi + y1
                    self.SetPixel(x, y, color)

            else:
                for yi in range(dy + 1):
                    y = yi + y1
                    self.SetPixel(x1, y, color)

            if dy != 0:
                m = float(dx) / float(dy)
                for yi in range(dy + 1):
                    y = yi + y1
                    x = m * yi + x1
                    self.SetPixel(x, y, color)

    def DrawTriangle(self, x1, y1, x2, y2, x3, y3, color = (255,255,255)):
        self.DrawLine(x1, y1, x2, y2, color)
        self.DrawLine(x2, y2, x3, y3, color)
        self.DrawLine(x3, y3, x1, y1, color)

    def FillTriangle(self, x1, y1, x2, y2, x3, y3, color = (255,255,255)):
        if y1 > y2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1

        if y1 > y3:
            x1, x3 = x3, x1
            y1, y3 = y3, y1
        

        if y2 > y3:
            x2, x3 = x3, x2
            y2, y3 = y3, y2

        dxA = x2 - x1
        dyA = y2 - y1

        dxB = x3 - x1
        dyB = y3 - y1

        dax_step = 0.0

        if dyA > 0 :
            dax_step = float(dxA) / math.fabs(float(dyA))

        if dyB > 0 :
            dbx_step = float(dxB) / math.fabs(float(dyB))

        if dyA > 0:
            for y in range(y1, y2):
                ax = x1 + int(float(y - y1) * dax_step)
                bx = x1 + int(float(y - y1) * dbx_step)

                if ax > bx:
                    ax, bx = bx, ax

                if (bx - ax) > 0:
                    tstep = 1.0 / float(bx - ax)
                    t = 0.0

                    for x in range(ax,bx):
                        self.SetPixel(x, y, color)
                        t += tstep

        dxA = x3 - x2
        dyA = y3 - y2

        if dyA > 0 :
            dax_step = float(dxA) / math.fabs(float(dyA))

        if dyA > 0:
            for y in range(y2, y3):
                ax = x2 + int(float(y - y2) * dax_step)
                bx = x1 + int(float(y - y1) * dbx_step)

                if ax > bx:
                    ax, bx = bx, ax
                if (bx - ax) > 0:
                    tstep = 1.0 / float(bx - ax)
                    t = 0.0

                    for x in range(ax,bx):
                        self.SetPixel(x, y, color)
                        t += tstep

    def Fill(self, color = (0, 0, 0)):
        self.screen.fill(color)

    def OnUserCreate(self):
        return True

    def OnUserUpdate(self, fElapsedTime):
        return True

    def GameThread(self):
        self.keyHolding = pygame.key.get_pressed()
        
        if not self.OnUserCreate():
            self.bAtomRunning = False

        tp1 = float(time.time())
        tp2 = float(time.time())

        while self.bAtomRunning:
            #Handling Timing
            tp2 = float(time.time())
            fElapsedTime = tp2 - tp1
            tp1 = tp2

            #Handling Inputs

            #Handling keyboard inputs
            self.keyHolding = pygame.key.get_pressed()

            #Handling events
            for event in pygame.event.get():

                #Check if the quit event has occured
                if event.type == pygame.QUIT:
                    self.bAtomRunning = False

            if not self.OnUserUpdate(fElapsedTime):
                self.bAtomRunning = False

            pygame.display.update()

        pygame.quit()

    def Start(self):
        self.GameThread()
    
