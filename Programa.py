import tkinter as tk
import random
import math

circulo = []
rectangulo=[]
numobjetos = 5

class Objetos:
    def __init__(self):
        self.centrox = random.randint(0,512) 
        self.centroy = random.randint(0,512) 
        self.radio = 30
        self.direccion = random.randint(0, 360)
        self.color = "green"
        self.color2="red"
        self.entidad = ""

    def visualizar(self):
        self.entidad = lienzo.create_oval(
            self.centrox - self.radio/2,
            self.centroy - self.radio/2,
            self.centrox + self.radio/2,
            self.centroy + self.radio/2,
            fill=self.color
        )
    def rectangulo(self):
        self.entidad = lienzo.create_rectangle(
            self.centrox - self.radio/2,
            self.centroy - self.radio/2,
            self.centrox + self.radio/2,
            self.centroy + self.radio/2,
            fill=self.color2
        )
    def mover(self):
        self.colisiona()
        lienzo.move(
            self.entidad,
            math.cos(self.direccion),
            math.sin(self.direccion)
        )
        self.centrox+= math.cos(self.direccion)
        self.centroy+= math.sin(self.direccion)

    def colisiona(self):
        if self.centrox < 0 or self.centrox > 512 or self.centroy < 0 or self.centroy > 512:
            self.direccion += 180

raiz = tk.Tk()

lienzo = tk.Canvas(raiz, width=512, height=512)
lienzo.pack()

for i in range(0, numobjetos):
    circulo.append(Objetos())
    rectangulo.append(Objetos())

for elemento in circulo:
    elemento.visualizar()
for elemento in rectangulo:
    elemento.rectangulo()

def bucleC():
    for objeto in circulo:
        objeto.mover()
    raiz.after(5, bucleC)
def bucleR():
    for objeto in rectangulo:
        objeto.mover()
    raiz.after(5, bucleR)

bucleC()
bucleR()

raiz.mainloop()
