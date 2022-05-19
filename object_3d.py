#import pygame as pg
from matrix_functions import *
from numba import njit


@njit(fastmath=True)
def any_func(arr, a, b):
    return np.any((arr == a) | (arr == b))


class Object3D:
    def __init__(self, render, vertexes='', faces=''):
        self.render = render
        self.vertexes = np.array([np.array(v) for v in vertexes])
        self.faces = np.array([np.array(face) for face in faces])
        self.translate([0.0001, 0.0001, 0.0001])

        #self.font = pg.font.SysFont('Arial', 30, bold=True)
        self.color_faces = [('orange', face) for face in self.faces]
        self.movement_flag, self.draw_vertexes = True, False
        self.label = ''
        self.counter = 0

    def draw(self, turtle):
        self.screen_projection(turtle)
        self.movement()

    def movement(self):
        self.counter += 1
        if self.movement_flag:
            self.rotate_y(0.5)

    def screen_projection(self, turtle):
        vertexes = self.vertexes @ self.render.camera.camera_matrix()
        vertexes = vertexes @ self.render.projection.projection_matrix
        vertexes /= vertexes[:, -1].reshape(-1, 1)
        vertexes[(vertexes > 2) | (vertexes < -2)] = 0
        vertexes = vertexes @ self.render.projection.to_screen_matrix
        vertexes = vertexes[:, :2]


        for index, color_face in enumerate(self.color_faces):
            color, face = color_face
            polygon = vertexes[face]

            if not any_func(polygon, self.render.H_WIDTH, self.render.H_HEIGHT):
                turtle.penup()
                turtle.goto(polygon[0][0] - self.render.H_WIDTH, -polygon[0][1] + self.render.H_HEIGHT)
                turtle.pendown()
                for x, y in polygon:
                    turtle.goto(x - self.render.H_WIDTH, -y + self.render.H_HEIGHT)
                turtle.goto(polygon[0][0] - self.render.H_WIDTH, -polygon[0][1] + self.render.H_HEIGHT)
                turtle.penup()
                #pg.draw.polygon(self.render.screen, color, polygon, 1)
                #print(polygon)
                # if self.label:
                #     text = self.font.render(self.label[index], True, pg.Color('white'))
                #     self.render.screen.blit(text, polygon[-1])

        # if self.draw_vertexes:
        #     for vertex in vertexes:
        #         if not any_func(vertex, self.render.H_WIDTH, self.render.H_HEIGHT):
        #             pg.draw.circle(self.render.screen, pg.Color('white'), vertex, 2)

    def translate(self, pos):
        self.vertexes = self.vertexes @ translate(pos)

    def scale(self, scale_to):
        self.vertexes = self.vertexes @ scale(scale_to)

    def rotate_x(self, angle):
        self.vertexes = self.vertexes @ rotate_x(angle)

    def rotate_y(self, angle):
        self.vertexes = self.vertexes @ rotate_y(angle)

    def rotate_z(self, angle):
        self.vertexes = self.vertexes @ rotate_z(angle)


class Axes(Object3D):
    def __init__(self, render):
        super().__init__(render)
        self.vertexes = np.array([(0, 0, 0, 1), (1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1)])
        self.faces = np.array([(0, 1), (0, 2), (0, 3)])
        self.colors = ['red', 'green', 'blue']
        self.color_faces = [(color, face) for color, face in zip(self.colors, self.faces)]
        self.draw_vertexes = False
        self.label = 'XYZ'
