import numpy as np
import pygame
import sys

class Ray:
    def __init__(self, P, d):
        #self, origin, direction
        self.P = P
        self.d = d

    def traceRay(self, P, d, scene):
        Q, N, M = scene.intersect(P, d)
        #Q is point of intersection
        #N is surface normal
        #M is the material properties
        if Q == None:
            return np.array([0, 0, 0])
        I = self.shade(Q, N, M, d, scene)
        return I
    
    def shade(self, Q, N, M, d, scene):
        lightd = scene.l-Q
        lightd = lightd / np.linalg.norm(lightd)
        intensity = max(0, np.dot(N, lightd))
        return M.c*intensity
    
class Scene:
    def __init__(self, objProperties, lightP):
        self.objects = []
        self.l = lightP #pos
        #only supports spheres, add more unique shapes later I guess.
        for objP in objProperties:
            center = objP[0]
            radius = objP[1]
            #worry about the latter two later
            color = objP[2]
            transparency = objP[3]
            self.objects.append(Sphere(center, radius, color, transparency))

    def intersect(self, p, d):
        minT = float('infinity')
        hit_Obj = None

        for i in self.objects:
            t = i.intersect(p,d)
            if t and t < minT:
                minT = t
                hit_Obj = i
        
        if hit_Obj == None:
            return None, None, None
        
        Q = p+d*minT
        N = hit_Obj.normal(Q)
        M = hit_Obj
        return Q, N, M

class Sphere:
    def __init__(self, center, radius, color, transparency):
        self.p = center
        self.r = radius
        self.c = color
        self.t = transparency
    
    def intersect(self, p, d):
        oc = p-self.p
        a = np.dot(d,d)
        b = 2*np.dot(oc, d)
        c = np.dot(oc,oc)-self.r**2
        disc = b*b-4*a*c
        if disc < 0:
            return None
        t1 = (-b - np.sqrt(disc)) / (2*a)
        t2 = (-b + np.sqrt(disc)) / (2*a)
        return min(t for t in [t1, t2] if t > 0) if any(t > 0 for t in [t1, t2]) else None

    def normal(self, point):
        return (point - self.p) / self.r


objProp = [
    [
        np.array([5,5,1]),
        1,
        np.array([0, 47, 255]),
        0.1
    ],
    [
        np.array([3,3,5]),
        1.2,
        np.array([0, 148, 2]),
        0.1
    ],
]

scene_ = Scene(objProp, np.array([2, 2, 10]))

def raytrace(origin, direction, scene):
    x,y,z = origin
    return 0

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jake's RayTracing")
screen.fill((255, 255, 255))

for x in range(SCREEN_WIDTH):
    for y in range(SCREEN_HEIGHT):
        direction = 
        col = raytrace(camera_pos, direction, scene_)

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
sys.exit()