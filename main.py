from object_3d import *
from camera import *
from projection import *
#import pygame as pg
import turtle
from time import sleep


class SoftwareRender:
    def __init__(self):
        self.s = turtle.Screen()
        self.t = turtle.Turtle()
        turtle.speed(0)
        turtle.pensize(1)
        turtle.color('orange')
        self.WIDTH = self.s.window_width()
        self.HEIGHT = self.s.window_height()
        #pg.init()
        self.RES = self.WIDTH, self.HEIGHT
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        #self.FPS = 60
        #self.screen = pg.display.set_mode(self.RES)
        #self.clock = pg.time.Clock()

        self.camera = Camera(self, [-5, 6, -55])
        self.projection = Projection(self)
        self.object = self.get_object_from_file('resources/t_34_obj.obj')
        self.object.rotate_y(-math.pi / 4)

    def get_object_from_file(self, filename):
        vertex, faces = [], []
        with open(filename) as f:
            for line in f:
                if line.startswith('v '):
                    vertex.append([float(i) for i in line.split()[1:]] + [1])
                elif line.startswith('f'):
                    faces_ = line.split()[1:]
                    faces.append([int(face_.split('/')[0]) - 1 for face_ in faces_])
        return Object3D(self, vertex, faces)

    def draw(self):
        self.s.bgcolor('darkgrey')
        self.s.tracer(10000)
        self.object.draw(self.t)
        self.s.update()
        sleep(1)
        self.s.clear()



    def run(self):
        while True:
            self.draw()
            self.camera.control()


if __name__ == '__main__':
    app = SoftwareRender()
    app.run()