import tkinter as tk
import random
import math
import json

circulo = []
rectangulo=[]
numobjetos = 5
class Estructura:
    def __init__(self):
        pass
    def serializar(self):
        self.centrox = random.randint(0,512) 
        self.centroy = random.randint(0,512)
        self.color = "green"
        objeto_serializado={
            "centrox": self.centrox,
            "centroy": self.centroy,
            "color": self.color
            }
        return objeto_serializado

class Objetos:
    def __init__(self,forma):
        self.centrox = random.randint(0,512) 
        self.centroy = random.randint(0,512) 
        self.radio = 30
        self.direccion = random.randint(0, 360)
        self.color = "green"
        self.color2="red"
        self.entidad = ""
        self.caracteristicas=[]
        self.forma=forma
        self.caracteristicas.append(Estructura())

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
    def serializar(self):
        objeto_serializado={
            "entidad":self.entidad,
            "forma":self.forma,
            "centrox": self.centrox,
            "centroy": self.centroy,
            "radio": self.radio,
            "direccion": self.direccion,
            "color": self.color,
            "caracteristicas":[item.serializar() for item in self.caracteristicas]
            }
        return objeto_serializado

def guardarJSON():
    objeto_serializado =[circulo.serializar() for circulo in circulo + rectangulo]
    cadena=json.dumps(objeto_serializado)
    with open("C:\\Users\\fonsi\\Desktop\\ESTUDIO\\IMF 2\\ACCESO A DATOS\\Practicas\\Practica8AD\\bbdd.json",'w') as archivo:
        archivo.write(cadena)

raiz = tk.Tk()
#Elementos
lienzo = tk.Canvas(raiz, width=512, height=512)
lienzo.pack()

boton_guardar=tk.Button(raiz,text="GUARDAR",command=guardarJSON).pack()

for i in range(0, numobjetos):
    circulo.append(Objetos("circulo"))
    rectangulo.append(Objetos("rectangulo"))

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
