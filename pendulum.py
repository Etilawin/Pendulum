from tkinter import Tk, Canvas
from math import cos, pi, sin, sqrt, acos


WIDTH = HEIGHT = 500
SIZE = 50
LENGTH = 300
GRAVITY = 9.81
tk = Tk()
canvas = Canvas(tk, width=WIDTH, height=HEIGHT, bg="grey")
canvas.pack()
color = 'black'


class Pendulum:
    def __init__(self, theta=10 * pi/180, v0=0):
        self._ball = canvas.create_oval(WIDTH // 2 - SIZE // 2,
                                        LENGTH - SIZE // 2,
                                        WIDTH // 2 + SIZE // 2,
                                        LENGTH + SIZE // 2,
                                        fill=color)
        self._string = canvas.create_line(WIDTH // 2, 0,
                                          WIDTH // 2, LENGTH)
        if theta > 25 * pi/180:
            print("This is based on the approximation on a small theta")
            print("Therefore it is not accurate for such big thetas")
        self.v0 = v0  # Vitesse initiale de theta
        self.theta = theta  # Theta a l'origine
        self.amplitude = 0
        self.phaseo = 0
        self.tick = 0  # Equivalent of time
        self.__resolve_initial()
        self.__move_active()

    def __resolve_initial(self):
        self.amplitude = sqrt(self.theta**2 + self.v0**2*GRAVITY/LENGTH)
        if self.amplitude >= pi/2:
            print("v0 and theta are too big, trying to reduce v0")
            if abs(self.v0) > 0:
                self.v0 = abs(self.v0) - 1
                self.__resolve_initial()
            else:
                print("The original theta is too big, reducing it to pi/3")
                assert self.theta > pi/3, \
                    "Error too small length, or too heavy gravity"
                self.theta = pi/3

        self.phaseo = acos(self.theta / self.amplitude)

    def __update(self):
        x = LENGTH * sin(self.theta)
        y = LENGTH * cos(self.theta)
        x_off = WIDTH // 2
        y_off = 0
        canvas.coords(self._ball,
                      x - SIZE // 2 + x_off,
                      y - SIZE // 2 + y_off,
                      x + SIZE // 2 + x_off,
                      y + SIZE // 2 + y_off)
        canvas.coords(self._string, x_off, y_off, x + x_off, y + y_off)
        self.theta = self.amplitude * cos(sqrt(LENGTH / GRAVITY)*self.tick
                                          + self.phaseo)

    def __move_active(self):
        self.__update()
        self.tick += 1/50
        tk.after(50, self.__move_active)


pendulum = Pendulum(theta=pi/4)
tk.mainloop()
