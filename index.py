from types import new_class
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from os import remove, path
from flask.wrappers import Response
from modelo.ecuacion import Ecuacion
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Polygon
from modelo.coord import Coord
import json
import datetime

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
numRestricciones = 1

# RUTA INICIAL 
@app.route('/')
def index():
    return render_template('index.html')

# RUTA QUE RECIBE EL NUMERO DE VARIABLES Y RESTRICCIONES
@app.route('/data', methods=['POST', 'GET'])
def data():
    if request.method == 'POST':
        metodo = request.form.get("tipoMetodo")
        session['metodo'] = metodo
        session['numVariables'] = int(request.form.get("numVariables"))
        session['numRes'] = int(request.form.get("numRestricciones"))    
        return render_template(
            "data.html",
            restricciones = session['numRes'],
            variables = session['numVariables']
        )
    else:
        flash(request.args.get("error"), "alert-danger")
        return render_template("data.html", restricciones = session['numRes'])

@app.route('/metodo', methods=['POST', 'GET'])
def selecMethod():
    data = json.loads(request.form.get('hidden-data'))
    res = grafico(data)
    return res

def mapearFuncObjetivo(func_objetivo):
    new_FO = ''
    for key, value in func_objetivo.items():
        new_value = '+' + str(value) if int(value) > 0 and not 'x1' in key else str(value)
        new_FO += (new_value + key + ' ').upper()
    return new_FO

def mapearRestric(restric):
    old_array_restric = []
    new_array_restric = []

    for res in restric:
        old_restric = ''
        new_restric = ''
        for key, value in res.items():
            if key != 'op' and key != 'result':
                new_value = '+' + str(value) if float(value) > 0 and not 'x1' in key else str(value)
                new_restric += (new_value + key + ' ').upper()
            
            if key != 'op' and key != 'result' and 'x' in key:
                old_value = '+' + str(value) if float(value) > 0 and not 'x1' in key else str(value)
                old_restric += (old_value + key + ' ').upper()
                
        new_restric += res['op'] + ' ' + res['result']
        old_restric += res['op'] + ' ' + res['result']
        new_array_restric.append(new_restric)
        old_array_restric.append(old_restric)
        
    return [old_array_restric, new_array_restric]

def grafico(data):

    # SE RECIBE LA INFORMACIÓN    
    
    func_obj = data.get('Funcion objetivo')
    func_obj_x1 = float(func_obj['x1'])
    func_obj_x2 = float(func_obj['x2'])
    min_max = data.get('Minmax')

    fig, ax=plt.subplots()

    restricciones= [] #las restricciones por post
    puntosCorte = [] #Puntos que corte
    puntosSoli = [] #Puntos de solucion

    # PROCESAMOS LAS RESTRICCIONES
    # Ciclo for que nos recorra las restricciones
    restric = data.get('Restricciones')
    for rest in restric:
        restriccion=Ecuacion(float(rest['x1']),float(rest['x2']),rest['op'],float(rest['result']))
        restricciones.append(restriccion)
    # ENCONTRAMOS LOS PUNTOS DE CORTE ENTRE LAS RESTRICCIONES

    puntosCorte.append(Coord(0,0))
    for rest in restricciones:
        if rest.puntCortX() is not None:
            puntosCorte.append(rest.puntCortX())
        if rest.puntCortY() is not None:
            puntosCorte.append(rest.puntCortY())
        for rest2 in restricciones:
            if rest != rest2:
                coord=rest.puntCortEcua(rest2)
                if coord is not None:
                    if coord not in puntosCorte:
                        puntosCorte.append(coord) 
    # DETERMINAMOS CUALES DE ESTOS PUNTOS DE CORTE SON DE SOLUCION

    for punt in puntosCorte:
        if punt.coord_restric(restricciones):
            puntosSoli.append(punt)
            
    if len(puntosSoli) == 0:
        return redirect(url_for('data', error = "El modelo no tiene solución"))

    # PROBAMOS LOS PUNTOS DE SOLUCIÓN EN LA FO Y ENCONTRAMOS EL MAXIMO Y MINIMO

    min = func_obj_x1*puntosSoli[0].x + func_obj_x2*puntosSoli[0].y
    max = func_obj_x1*puntosSoli[0].x + func_obj_x2*puntosSoli[0].y
    punt_min = puntosSoli[0]
    punt_max = puntosSoli[0]
    for punt in puntosSoli:
        punto = round(func_obj_x1*punt.x + func_obj_x2*punt.y,2)
        if punto < min:
            min = punto
            punt_min = punt
        elif punto > max:
            max = punto
            punt_max = punt
    # USAMOS VARIABLES AUXILIARES PARA SABER CUAL ES EL RANGO MAXIMO A GRAFICAR EN EL EJE X Y EJE Y
    max_range_x = 0
    max_range_y = 0
    for res in restricciones:
        if res.puntCortX() is not None and res.puntCortX().x > max_range_x:
            max_range_x = res.puntCortX().x
        if res.puntCortY() is not None and res.puntCortY().y > max_range_y:
            max_range_y = res.puntCortY().y
    # SE ENCUENTRAN LOS EXTREMOS DE CADA RESTRICCION Y SE AGREGA UNA DESCRIPCION PARA CADA UNA

    legend = []
    ax.grid()
    for res in restricciones:
        if res.pedPositiv():
            x=[0,max_range_x]
            y=[res.resultado/(res.y if res.y !=0 else 1),((res.x*(-1))*(max_range_x)+res.resultado)/(res.y if res.y != 0 else 1)]
        elif res.puntCortX() is None:
            x = [0, max_range_x]
            y = [res.puntCortY().y, res.puntCortY().y]
        elif res.puntCortY() is None:
            x = [res.puntCortX().x, res.puntCortX().x]
            y = [0, max_range_y]
        else:    
            x = [res.puntCortX().x, res.puntCortY().x]
            y = [res.puntCortX().y, res.puntCortY().y]
        legend.append(res.__str__())
        ax.plot(x,y)
        
    # SE GRAFICAN LOS PUNTOS DE SOLUCIÓN
    
    for solu in puntosSoli:
        ax.plot(solu.x, solu.y, marker="o", color="black")
    
    # SE GRAFICA LA RECTA DE LA FUNCIÓN OBJETIVO
    if(resmax(restricciones) and min_max=='max'):
        func_obj_ecua = Ecuacion(func_obj_x1, func_obj_x2, "=", 'Indefinido')
    else:
        if min_max == "min":
            func_obj_ecua = Ecuacion(func_obj_x1, func_obj_x2, "=", min)
        elif min_max == "max":
            func_obj_ecua = Ecuacion(func_obj_x1, func_obj_x2, "=", max)
        if(func_obj_ecua.pedPositiv()):
            f_o_x = [func_obj_ecua.puntCortX().x, max_range_x]
            f_o_y = [func_obj_ecua.puntCortX().y, (func_obj_ecua.resultado + (-1)*(func_obj_ecua.x)*(max_range_x))/(func_obj_ecua.y if func_obj_ecua.y !=0 else 1)]
        else:
            f_o_x = [func_obj_ecua.puntCortX().x, func_obj_ecua.puntCortY().x]
            f_o_y = [func_obj_ecua.puntCortX().y, func_obj_ecua.puntCortY().y]
        ax.plot(f_o_x,f_o_y, color="black")
    # SE PROCESAN LOS DATOS QUE SE VAN A VER EN LA TABLA
    #Estos son los datos que debe incluir la tabla
    datos_tabla=tabla(puntosSoli,func_obj, func_obj_ecua)
    
    if resmax(restricciones):
        may = mayor(restricciones,max_range_x)
        puntosSoli.append(Coord(max_range_x, (max_range_y if max_range_y > may else may)))

    # SE GRAFICA LA FIGURA A PARTIR DE LOS PUNTOS DE SOLUCIÓN

    areaSolu = Polygon([[punt.x,punt.y] for punt in puntosSoli], alpha=0.2,facecolor="Green",edgecolor="green",linewidth=2)
    ax.add_patch(areaSolu)
    # SE AGREGAN FUNCIONES DE LA GRAFICA COMO EL NOMBRE DEL EJE X,Y ...

    legend.append("FO: "+func_obj_ecua.__str__())

    ax.legend(legend,shadow=True, title="Restricciones", framealpha=0.5)
    plt.xlabel("X1")
    plt.ylabel("X2")
    nombre='static/img/grafica'+str(datetime.datetime.now().timestamp())+'.png'
    plt.savefig(nombre)
    plt.close()

    return render_template('metodoGrafico.html', data_table = datos_tabla, restricciones= restricciones, fo = func_obj_ecua, nom=nombre, MaxMin= "Maximizar" if min_max == "max" else "Minimizar")

@app.route('/delete', methods=['POST'])
def deleteImage():
    data= request.get_json(force=True)
    name=data.get('image')
    if(path.exists("./static/img/"+name)):
        remove("./static/img/"+name)
    respuesta ={
        'status':'success',
        'code':200,
        'message':"Se ha eliminado la imagen de manera correcta",
        'deletedImage':name
    }
    return jsonify(respuesta)

def resmax(restricciones):
    for res in restricciones:
        if res.tipo != ">=":
            return False
    return True

# FUNCION QUE REORDENA LOS PUNTOS
def reordenarpunt(puntosSoli, restricciones):
    puntosOrde=[]
    puntosOrde.append(puntosSoli[0])
    puntosSoli.pop(0)
    cont=0
    while len(puntosSoli)!=0:
        if puntosOrde[len(puntosOrde)-1].ecuaPerte(puntosSoli[cont],restricciones):
            puntosOrde.append(puntosSoli[cont])
            puntosSoli.pop(cont)
        else:
            cont=cont+1
        if cont==len(puntosSoli):
            cont=0
    return puntosOrde

# FUNCIÓN QUE PROCESA LOS DATOS DE LA TABLA    
def tabla(puntSoli, func_obj, func_obj_ecua):
    data={}
    puntos=[]
    i=1
    for punt in puntSoli:
        valor = round(float(func_obj['x1'])*punt.x + float(func_obj['x2'])*punt.y,2)
        dicpunt={
            'Punto':f'{i}',
            'Coordenada X (X1)':f'{round(punt.x,3)}',
            'Coordenada Y (X2)':f'{round(punt.y,3)}',
            'Valor de la función objetivo (Z)':f'{valor}',
            'Solu': 1 if valor == func_obj_ecua.resultado else 0
            }
        puntos.append(dicpunt)
        i+=1
    data['puntos']=puntos
    return data

def mayor(restricciones, x_value):
    max=0
    for res in restricciones:
        resultado = (res.resultado + ((-1) * res.x * x_value)) / (res.y if res.y != 0 else 1) 
        if(resultado > max):
            max=resultado
    return max

if __name__=="__main__":
    app.run(debug=True)