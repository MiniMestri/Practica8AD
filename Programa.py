import tkinter as tk
import random
import math
import json
import sqlite3

circulo = []
rectangulo=[]
numobjetos = 0

#Clase estructura que genera otra tabla con propiedades de los objetos
class Estructura:
    def __init__(self):
        self.centrox = random.randint(0,512) 
        self.centroy = random.randint(0,512)
        self.color = "green"
    def serializar(self):
        objeto_serializado={
            "centrox": self.centrox,
            "centroy": self.centroy,
            "color": self.color
            }
        return objeto_serializado

#Clase objetos para crear elementos
class Objetos:
    def __init__(self,forma):
        self.centrox = random.randint(0,512) 
        self.centroy = random.randint(0,512) 
        self.radio = 30
        self.direccion = random.randint(0, 360)
        self.color1 = "green"
        self.color2="red"
        self.entidad = ""
        self.caracteristicas=[Estructura() for _ in range(2)]
        self.forma=forma
        self.caracteristicas.append(Estructura())
        
    #Visualización de circulo
    def circulo(self):
        self.entidad = lienzo.create_oval(
            self.centrox - self.radio/2,
            self.centroy - self.radio/2,
            self.centrox + self.radio/2,
            self.centroy + self.radio/2,
            fill=self.color1
        )
    #Visualización de rectangulo
    def rectangulo(self):
        self.entidad = lienzo.create_rectangle(
            self.centrox - self.radio/2,
            self.centroy - self.radio/2,
            self.centrox + self.radio/2,
            self.centroy + self.radio/2,
            fill=self.color2
        )
        
    #Mover el rectangulo y circulo por el lienzo
    def mover(self):
        self.colisiona()
        lienzo.move(
            self.entidad,
            math.cos(self.direccion),
            math.sin(self.direccion)
        )
        self.centrox+= math.cos(self.direccion)
        self.centroy+= math.sin(self.direccion)
        
    #Colision con los limites de la ventana
    def colisiona(self):
        if self.centrox < 0 or self.centrox > 512 or self.centroy < 0 or self.centroy > 512:
            self.direccion += 180
    #Serializar los datos para volcarlos en json
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
    
    #Método limpiar lienzo
    def limpiar(self):
        lienzo.delete(self.entidad)
        if self.forma == "circulo" and self in circulo:
            circulo.remove(self)
        elif self.forma == "rectangulo" and self in rectangulo:
            rectangulo.remove(self)

#guardar en JSON
def guardarJSON():
    objeto_serializado =[circulo.serializar() for circulo in circulo + rectangulo]
    cadena=json.dumps(objeto_serializado)
    with open("C:\\Users\\fonsi\\Desktop\\ESTUDIO\\IMF 2\\ACCESO A DATOS\\Practicas\\Practica8AD\\bbdd.json",'w') as archivo:
        archivo.write(cadena)

#Guardar objeto en SQL
def guardarSQL():
    try:
        conexion = sqlite3.connect("C:\\Users\\fonsi\\Desktop\\ESTUDIO\\IMF 2\\ACCESO A DATOS\\Practicas\\Practica8AD\\bbdd.sqlite3")
        cursor = conexion.cursor()

        for objeto in circulo + rectangulo:
            sql_query = '''INSERT INTO objetos VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
            cursor.execute(sql_query, (
                str(objeto.entidad),
                str(objeto.forma),
                objeto.centrox,
                objeto.centroy,
                objeto.radio,
                objeto.direccion,
                str(objeto.color1),
                str(objeto.color2),
                str(objeto.caracteristicas)
            ))

            for elemento in objeto.caracteristicas:
                sql_query2 = '''INSERT INTO caracteristicas VALUES (NULL, ?, ?, ?, ?)'''
                cursor.execute(sql_query2, (
                    str(objeto.entidad),
                    str(elemento.centrox),
                    str(elemento.centroy),
                    str(elemento.color)
                ))

        conexion.commit()
        conexion.close()

    finally:
        if conexion:
            conexion.close()

#Cargar objetos desde SQLite3
def leerSQL():
    

        conexion = sqlite3.connect("C:\\Users\\fonsi\\Desktop\\ESTUDIO\\IMF 2\\ACCESO A DATOS\\Practicas\\Practica8AD\\bbdd.sqlite3")
        cursor = conexion.cursor()

        cursor.execute('''SELECT * FROM objetos''')

        while True:
            fila = cursor.fetchone()
            if fila is None:
                break
            
            forma = fila[2]
            objeto = Objetos(forma)
            objeto.entidad = fila[1]
            objeto.centrox = fila[3]
            objeto.centroy = fila[4]
            objeto.radio = fila[5]
            objeto.direccion = fila[6]
            objeto.caracteristicas = fila[9]

            if forma == "circulo":
                objeto.color1 = fila[7]
                circulo.append(objeto)
                objeto.circulo()
            elif forma == "rectangulo":
                objeto.color2 = fila[8]
                rectangulo.append(objeto)
                objeto.rectangulo()

            cursor2= conexion.cursor()
            peticion2='''SELECT * FROM caracteristicas WHERE objeto='''+(str(objeto.entidad))+'''
            '''
            cursor2.execute(peticion2)
            while True:
                fila1 = cursor2.fetchone()
                if fila1 is None:
                    break
                estructura = Estructura()
                estructura.centrox=fila[2]
                estructura.centroy=fila[3]
                estructura.color=fila[4]
                objeto.caracteristicas.append(estructura)
                
        conexion.close()

#Limpiar el lienzo    
def limpiar_lienzo():
    for objeto in circulo + rectangulo:
        objeto.limpiar()

#Añadir rectangulo al lienzo
def anadirRectangulo():
    global numobjetos
    numobjetos+=1
    nuevo_rectangulo=Objetos("rectangulo")
    nuevo_rectangulo.rectangulo()
    rectangulo.append(nuevo_rectangulo)

#Añadir un circulo al lienzo
def anadirCirculo():
    global numobjetos
    numobjetos+=1
    nuevo_circulo=Objetos("circulo")
    nuevo_circulo.circulo()
    circulo.append(nuevo_circulo)
    
        
raiz = tk.Tk()
#Elementos
lienzo = tk.Canvas(raiz, width=512, height=512)
lienzo.pack()

frame_botones=tk.Frame(raiz)
frame_botones.pack()

#Botones
boton_guardar=tk.Button(frame_botones,text="GUARDAR",command=guardarSQL).grid(row=0,column=0,padx=10,pady=10)
boton_limpiar=tk.Button(frame_botones,text="LIMPIAR",command=limpiar_lienzo).grid(row=0,column=1,padx=10,pady=10)
boton_cargar=tk.Button(frame_botones,text="CARGAR",command=leerSQL).grid(row=0,column=2,padx=10,pady=10)
boton_anadirR=tk.Button(frame_botones,text="+1 RECTANGULO",command=anadirRectangulo).grid(row=0,column=3,padx=10,pady=10)
boton_anadirC=tk.Button(frame_botones,text="+1 CIRCULO",command=anadirCirculo).grid(row=0,column=4,padx=10,pady=10)

#Funcionamiento
for elemento in circulo:
    elemento.circulo()
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
