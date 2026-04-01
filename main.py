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
    def __init__(self, objProperties, lightP, lightS):
        self.objects = []
        self.l = lightP #pos
        self.st = lightS #strength
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
        
        if(hit_Obj == None)
            return None, None, None
        
        Q = p+d*minT
        N = hit_Obj.normal(Q)
        M = hit_Obj
        return Q, N, M

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

    def normal(self, point):
        center = np.array([self.x, self.y, self.z])
        return (point - center) / self.r