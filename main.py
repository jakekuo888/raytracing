import numpy as np
import pygame
import sys

class Ray:
    def __init__(self, P, d):
        self.P = P
        self.d = d

    def traceRay(self, scene, depth=0, max_depth=3):
        if depth > max_depth:
            return np.array([0,0,0])

        Q, N, M = scene.intersect(self.P, self.d)
        if Q is None:
            return np.array([255, 255, 255])

        I = self.shade(Q, N, M, self.d, scene)

        if M.ref > 0:
            reflect_dir = self.d - 2 * np.dot(self.d, N) * N
            reflect_dir = reflect_dir / np.linalg.norm(reflect_dir)
            reflected_color = Ray(Q + 1e-4 * N, reflect_dir).traceRay(scene, depth + 1, max_depth)
            I = I * (1 - M.ref) + reflected_color * M.ref

        return np.clip(I, 0, 255).astype(int)
    
    def shade(self, Q, N, M, d, scene):
        lightd = scene.l - Q
        lightd = lightd / np.linalg.norm(lightd)
        intensity = max(0, np.dot(N, lightd))
        return np.clip(M.c * intensity, 0, 255).astype(int)
    
class Scene:
    def __init__(self, objProperties, lightP):
        self.objects = []
        self.l = lightP
        for objP in objProperties:
            center = objP[0]
            radius = objP[1]
            color = objP[2]
            transparency = objP[3]
            reflectivity = objP[4]
            self.objects.append(Sphere(center, radius, color, transparency, reflectivity))

    def intersect(self, p, d):
        minT = float('infinity')
        hit_Obj = None

        for i in self.objects:
            t = i.intersect(p, d)
            if t is not None and t < minT:
                minT = t
                hit_Obj = i
        
        if hit_Obj is None:
            return None, None, None
        
        Q = p + d * minT
        N = hit_Obj.normal(Q)
        M = hit_Obj
        return Q, N, M

class Sphere:
    def __init__(self, center, radius, color, transparency, reflectivity):
        self.p = center
        self.r = radius
        self.c = color
        self.t = transparency
        self.ref = reflectivity
    
    def intersect(self, p, d):
        oc = p - self.p
        a = np.dot(d, d)
        b = 2 * np.dot(oc, d)
        c = np.dot(oc, oc) - self.r ** 2
        disc = b * b - 4 * a * c
        if disc < 0:
            return None
        t1 = (-b - np.sqrt(disc)) / (2 * a)
        t2 = (-b + np.sqrt(disc)) / (2 * a)
        ts = [t for t in [t1, t2] if t > 0]
        return min(ts) if ts else None

    def normal(self, point):
        return (point - self.p) / self.r

objProp = [
    [
        np.array([0, 0, 5]),
        1,
        np.array([184, 31, 31]),
        0.1,
        0.3,
    ],
    [
        np.array([2, 1, 3]),
        2,
        np.array([33, 184, 73]),
        0.1,
        0.3,
    ],
    [
        np.array([0, 2, 2]),
        1,
        np.array([41, 31, 184]),
        0.1,
        0.3,
    ],
]

scene_ = Scene(objProp, np.array([0,0,0]))

def raytrace(origin, direction, scene):
    return Ray(origin, direction).traceRay(scene)

pygame.init()

scale = 2
SCREEN_WIDTH = int(200*scale)
SCREEN_HEIGHT = int(150*scale)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Quasistar's RayTracing")
screen.fill((255, 255, 255))

camera_pos = np.array([-1,0,-5])
viewport_width = 1
viewport_height = SCREEN_HEIGHT / SCREEN_WIDTH
projection_plane_z = 1

def dostuff():
    for x in range(SCREEN_WIDTH):
        for y in range(SCREEN_HEIGHT):
            px = (x + 0.5) / SCREEN_WIDTH
            py = (y + 0.5) / SCREEN_HEIGHT

            vx = (2 * px - 1) * viewport_width
            vy = (1 - 2 * py) * viewport_height
            vz = projection_plane_z

            direction = np.array([vx, vy, vz])
            direction = direction / np.linalg.norm(direction)
            col = raytrace(camera_pos, direction, scene_)
            screen.set_at((x, y), col.astype(int))

dostuff()

print("done!")
pygame.display.flip()

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
sys.exit()
