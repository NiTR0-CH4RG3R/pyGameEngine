#Created by Buddhima Zoysa (27/04/2020)
#This is just a experimental 3D engine that uses pyGameEngine.py
#This is still working progress (Not working)
from pyGameEngine import pyGameEngine
import math

class py3DEngine(pyGameEngine):
    def __init__(self):
        self.sAppName = "3D Engine"
        self.sIconPath = ''

    def WorldToScreenCord(self, x, y, z):
        fXToXRatio = x / (z * self.fFOVHalfTan)
        fYToYRatio = y / (z * self.fFOVHalfTan * self.fAspectRatio)

        fNormalizedX = (fXToXRatio + 1.0) * 0.5 * self.ScreenWidth()
        fNormalizedY = (1 - (fYToYRatio + 1) * 0.5) * self.ScreenHeight()
        fNormalizedZ = ((z - self.fZNear) * self.fZFar) / (self.fZFar - self.fZNear)

        return [int(fNormalizedX), int(fNormalizedY), fNormalizedZ]

    def VectorDotProduct(self, a, b):
        return (a[0] * b[0] + a[1] * b[1] + a[2] * b[2])

    def VectorCrossProduct(self, a, b):
        outPutVector = [None] * 3
        outPutVector[0] = a[1] * b[2] - a[2] * b[1]
        outPutVector[1] = a[2] * b[0] - a[0] * b[2]
        outPutVector[2] = a[0] * b[1] - a[1] * b[0]
        return outPutVector

    def OnUserCreate(self):

        self.fFOV = 90.0 #Field of view in degrees
        self.fZFar = 1000.0
        self.fZNear = 0.1

        self.fPlayerMovingSpeed = 2.0
        self.fPlayerRotatingSpeed = 1.0
        self.camera =   [
                        [0.0, 0.0, -6.0], #Camera position
                        [0.0, 0.0, 0.0]  #Camera rotation (in degrees)
                        ]
        self.directionalLight = [
                                [0.0, 0.0, 0.0],
                                [-1.0, -1.0, -1.0]
                                ]

        self.meshObjects = [] #This holds all the objects that need to be rendered
        self.fDepthBuffer = [0.0] * self.ScreenWidth() * self.ScreenHeight()
        self.fFOVHalfTan = math.tan(math.radians(self.fFOV / 2))
        self.fAspectRatio = float(self.ScreenWidth()) / float(self.ScreenHeight())

        for i in range(len(self.camera[1])):
            self.camera[1][i] = math.radians(self.camera[1][i])
        
        meshCube = [
                    #SOUTH
                    ((0.0, 0.0, 0.0),     (0.0, 1.0, 0.0),     (1.0, 1.0, 0.0)), 
                    ((0.0, 0.0, 0.0),     (1.0, 1.0, 0.0),     (1.0, 0.0, 0.0)), 
                                                                                
                    #EAST           												
                    ((1.0, 0.0, 0.0),     (1.0, 1.0, 0.0),     (1.0, 1.0, 1.0)), 
                    ((1.0, 0.0, 0.0),     (1.0, 1.0, 1.0),     (1.0, 0.0, 1.0)), 
                                                                                
                    #NORTH           											
                    ((1.0, 0.0, 1.0),     (1.0, 1.0, 1.0),     (0.0, 1.0, 1.0)), 
                    ((1.0, 0.0, 1.0),     (0.0, 1.0, 1.0),     (0.0, 0.0, 1.0)), 
                                                                                
                    #WEST            											
                    ((0.0, 0.0, 1.0),     (0.0, 1.0, 1.0),     (0.0, 1.0, 0.0)), 
                    ((0.0, 0.0, 1.0),     (0.0, 1.0, 0.0),     (0.0, 0.0, 0.0)), 
                                                                                
                    #TOP             											
                    ((0.0, 1.0, 0.0),     (0.0, 1.0, 1.0),     (1.0, 1.0, 1.0)), 
                    ((0.0, 1.0, 0.0),     (1.0, 1.0, 1.0),     (1.0, 1.0, 0.0)), 
                                                                                
                    #BOTTOM          											
                    ((1.0, 0.0, 1.0),     (0.0, 0.0, 1.0),     (0.0, 0.0, 0.0)), 
                    ((1.0, 0.0, 1.0),     (0.0, 0.0, 0.0),     (1.0, 0.0, 0.0))
                    ]
        self.meshObjects.append(meshCube)
        return True

    def OnUserUpdate(self, fElapsedTime):
        #Clear the screen
        self.Fill((0, 0, 0))


        if self.keyHolding[self.Keys['W']]:
            self.camera[0][2] += self.fPlayerMovingSpeed * fElapsedTime
        if self.keyHolding[self.Keys['S']]:
            self.camera[0][2] -= self.fPlayerMovingSpeed * fElapsedTime
        if self.keyHolding[self.Keys['D']]:
            self.camera[0][0] += self.fPlayerMovingSpeed * fElapsedTime
        if self.keyHolding[self.Keys['A']]:
            self.camera[0][0] -= self.fPlayerMovingSpeed * fElapsedTime

        if self.keyHolding[self.Keys['Q']]:
            self.camera[0][1] += self.fPlayerMovingSpeed * fElapsedTime
        if self.keyHolding[self.Keys['E']]:
            self.camera[0][1] -= self.fPlayerMovingSpeed * fElapsedTime

        for mesh in self.meshObjects:
            for tri in mesh:
                
                camRelV1 = (tri[0][0] - self.camera[0][0], tri[0][1] - self.camera[0][1], tri[0][2] - self.camera[0][2])
                camRelV2 = (tri[1][0] - self.camera[0][0], tri[1][1] - self.camera[0][1], tri[1][2] - self.camera[0][2])
                camRelV3 = (tri[2][0] - self.camera[0][0], tri[2][1] - self.camera[0][1], tri[2][2] - self.camera[0][2])

                line1 = [None] * 3
                line2 = [None] * 3
                line1[0] = camRelV2[0] - camRelV1[0]
                line1[1] = camRelV2[1] - camRelV1[1]
                line1[2] = camRelV2[2] - camRelV1[2]
                
                line2[0] = camRelV3[0] - camRelV1[0]
                line2[1] = camRelV3[1] - camRelV1[1]
                line2[2] = camRelV3[2] - camRelV1[2]

                normal = self.VectorCrossProduct(line1, line2)
                
                normalLength = math.sqrt(normal[0] * normal[0] + normal[1] * normal[1] + normal[2] * normal[2])
                normal[0] /= normalLength
                normal[1] /= normalLength
                normal[2] /= normalLength

                #a = normal[0] * camRelV3[0]
                #b = normal[1] * camRelV3[1]
                #c = normal[2] * camRelV3[2]
                #d = a + b + c
                d = self.VectorDotProduct(normal,camRelV3)
                if d < 0.0:
                    if camRelV1[2] > 0.5 and camRelV2[2] > 0.5 and camRelV3[2] > 0.5:
                        v1 = self.WorldToScreenCord(camRelV1[0], camRelV1[1], camRelV1[2])
                        v2 = self.WorldToScreenCord(camRelV2[0], camRelV2[1], camRelV2[2])
                        v3 = self.WorldToScreenCord(camRelV3[0], camRelV3[1], camRelV3[2])

                        #lightAndNormalDot = self.VectorDotProduct(normal, directionalLight[1])
                        #lightAndNormalDot = 1 - (lightAndNormalDot * 0.5 + 0.5)
                        #lightAndNormalDot *= 255

                        self.DrawTriangle(v1[0], v1[1], v2[0], v2[1], v3[0], v3[1])

        return True
