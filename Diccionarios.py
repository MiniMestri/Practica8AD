import tkinter as tk
from tkinter import ttk
import random
import math
import sqlite3

objetos=[]
numerosats=0

#Clase objeto "Objetos"
class Objetos:
    def __init__(self):
        self.centrox = 512
        self.centroy = 300
        self.radioS = 30
        self.radioM = 300
        self.direccion = random.randint(0,360)
        self.color1 = "blue"
        self.color2 = "green"
        self.color3="grey"
        self.grosorborde=10
        self.entidad=""
        self.velocidad = random.randint(1,20)
        self.a=random.randint(2,8)
        self.b=random.randint(1,4)
        self.energia= 100
        self.entidadenergia=""
        
#Método visualizar propiedades tierra
    def visualizarT(self):
        lienzo.create_oval(
            self.centrox-self.radioM/2,
            self.centroy-self.radioM/2,
            self.centrox+self.radioM/2,
            self.centroy+self.radioM/2,
            fill=self.color1,
            outline=self.color2,
            width=self.grosorborde)
        
#Método visualizar propiedades satélites
    def visualizarS(self):
        self.entidad=lienzo.create_oval(
            self.centrox-self.radioS/2,
            self.centroy-self.radioS/2,
            self.centrox+self.radioS/2,
            self.centroy+self.radioS/2,
            fill=self.color3)
        self.visualizarEnergia()
    def visualizarEnergia(self):
        self.entidadenergia = lienzo.create_rectangle(
            self.centrox-self.radioS/2,
            self.centroy-self.radioS/2-10,
            self.centrox+self.radioS/2,
            self.centroy-self.radioS/2-8,
            fill="red")
        
#Movimientos elípticos de los satélites
    def mueve(self):
         if self.energia > 0:
            self.energia -= 0.1

         self.direccion += math.radians(self.velocidad)
         x = self.centrox + self.a * math.cos(self.direccion)
         y = self.centroy + self.b * math.sin(self.direccion)

         # Mover la entidad a las nuevas coordenadas
         lienzo.move(self.entidad, x - self.centrox, y - self.centroy)

         self.centrox = x
         self.centroy = y

         direccion_x = math.cos(self.direccion)
         direccion_y = math.sin(self.direccion)

         lienzo.move(self.entidadenergia, direccion_x, direccion_y)

         # Actualizar la barra de energía
         anchuraenergia = (self.energia / 100) * self.radioS
         lienzo.coords(
            self.entidadenergia,
            self.centrox - self.radioS / 2,
            self.centroy - self.radioS / 2 - 10,
            self.centrox - self.radioS / 2 + anchuraenergia,
            self.centroy - self.radioS / 2 - 8 
         )

        #Eliminar satelite si llega a 0 de energia
         if self.energia <=0:
             lienzo.delete(self.entidad)
             lienzo.delete(self.entidadenergia)
             objetos.remove(self)

def incluir():
    global numerosats
    numerosats+=1
    nuevo_satelite=Objetos()
    nuevo_satelite.visualizarS()
    nuevo_satelite.visualizarEnergia()
    objetos.append(nuevo_satelite)

#Método guardar posición de cada objeto (satélites)
def guardarPosicion():
    conexion = sqlite3.connect("C:\\Users\\fonsi\\Desktop\\ESTUDIO\\IMF 2\\ACCESO A DATOS\\Practicas\\Practica7AD\\nasa.sqlite3")
    cursor = conexion.cursor()
    for objeto in objetos:
        cursor.execute('''INSERT INTO satelites VALUES (NULL,
                                '''+str(objeto.centrox)+''',
                                '''+str(objeto.centroy)+''',
                                '''+str(objeto.radioS)+''',
                                '''+str(objeto.direccion)+''',
                                "'''+str(objeto.color3)+'''",
                                "'''+str(objeto.entidad)+'''",
                                '''+str(objeto.velocidad)+''',
                                '''+str(objeto.a)+''',
                                '''+str(objeto.b)+''',
                                '''+str(objeto.energia)+''',
                               "'''+str(objeto.entidadenergia)+'''") ''')
    conexion.commit()
    conexion.close()
    
#Cargar satelites desde sql
try:
    conexion = sqlite3.connect("C:\\Users\\fonsi\\Desktop\\ESTUDIO\\IMF 2\\ACCESO A DATOS\\Practicas\\Practica7AD\\nasa.sqlite3")
    cursor = conexion.cursor()

    cursor.execute('''SELECT * FROM satelites''')

    while True:
        fila = cursor.fetchone()
        if fila is None:
            break
        satelite= Objetos()
        satelite.centrox=fila[1]
        satelite.centroy=fila[2]
        satelite.radioS=fila[3]
        satelite.direccion=fila[4]
        satelite.color3=fila[5]
        satelite.entidad=fila[6]
        satelite.velocidad=fila[7]
        satelite.a=fila[8]
        satelite.b=fila[9]
        objetos.append(Objetos())

    conexion.close()
except:
    print("ERROR")
                 
raiz=tk.Tk()

#Lienzo
lienzo=tk.Canvas(width=1024,height=600)
lienzo.pack()

#Declaración de objeto
objeto=Objetos()
objeto.visualizarT()

#Crear frame para organizar los botones
frame_botones=tk.Frame(raiz)
frame_botones.pack()

#Boton par añadir elementos
boton_crear=tk.Button(frame_botones,text="Añadir 1",command=incluir)
boton_crear.grid(row=0,column=0,padx=10,pady=10)

#velocaidad seleccionada
velocidad_seleccionada = tk.StringVar()
velocidad_seleccionada.set("10")

#Combobox para seleccionar la velocidad 
combobox= ttk.Combobox(frame_botones,values=[0,10,20,30,40,50,75,100],textvariable=velocidad_seleccionada)
combobox.grid(row=0,column=2,padx=10,pady=10)

#Boton para guardar
boton = tk.Button(frame_botones,text="Guardar", command=guardarPosicion)
boton.grid(row=0,column=1,padx=10,pady=10)

#Velocidad de movimiento en el tiempo 
def velocidad():
    eleccion=int(velocidad_seleccionada.get())
    for objeto in objetos:
        objeto.mueve()
    raiz.after(eleccion,velocidad)
velocidad()

raiz.mainloop()
