import numpy as np
import pygame as pyg

def raytrace(origin, recursion, scene):
    x,y,z = origin
    return 0


class Ray:
    def __init__(self, P, d):
        #self, origin, direction
        self.P = P
        self.d = d

    def traceRay(self, P, d, scene):
        (Q, N, M) = scene.intersect(P, d)#pretend that this is a given
        #Q is point of intersection
        #N is surface normal
        #M is the material properties
        I = shade(Q, N, M, d, scene)
        return I
    
class Scene:
    def __init__(self, objN, objProperties, lightP, lightS):
        self.objects = []
        self.l = lightP #pos
        self.st = lightS #strength
        #only supports spheres, add more unique shapes later I guess.
        for i in range(objN):
            center = objProperties[0]
            radius = objProperties[1]
            #worry about the latter two later
            color = objProperties[2]
            transparency = objProperties[3]
            self.objects.append(Sphere(center, radius, color, transparency))

    def intersect(self, p, d):
        hit_Obj = None
        for i in self.objects:
            inter = i.intersect(p,d)
        if(hit_Obj == None)
            return None, None, None
        return false

class Sphere:
    def __init__(self, center, radius, color, transparency):
        self.x = center[0]
        self.y = center[1]
        self.z = center[2]
        self.r = radius
        self.c = color
        self.t = transparency
    
    def intersect(self, p, d):
        #