from flask import Flask, render_template, request, jsonify
import math
import random

app = Flask(__name__)

coord = {
    'Jiloyork': (19.916012, -99.580580),
    'Toluca': (19.289165, -99.655697),
    'Atlacomulco': (19.799520, -99.873844),
    'Guadalajara': (20.677754472859146, -103.34625354877137),
    'Monterrey': (25.69161110159454, -100.321838480256),
    'QuintanaRoo': (21.163111924844458, -86.80231502121464),
    'Michohacan': (19.701400113725654, -101.20829680213464),
    'Aguascalientes': (21.87641043660486, -102.26438663286967),
    'CDMX': (19.432713075976878, -99.13318344772986),
    'QRO': (20.59719437542255, -100.38667040246602)
}

def distancia(coord1, coord2):
    """Calcula la distancia euclidiana correctamente"""
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    return math.sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2)  # Corregido el cálculo

def evalua_ruta(ruta, coord):
    """Calcula la distancia total de la ruta"""
    total = sum(distancia(coord[ruta[i]], coord[ruta[i + 1]]) for i in range(len(ruta) - 1))
    total += distancia(coord[ruta[-1]], coord[ruta[0]])  # Regresa a la ciudad origen
    return total

def hill_climbing(origen, coord):
    """Optimiza el recorrido usando Hill Climbing"""
    ciudades = list(coord.keys())
    ciudades.remove(origen)  # Eliminamos la ciudad origen
    random.shuffle(ciudades)  # Generamos una ruta inicial aleatoria

    mejor_ruta = [origen] + ciudades + [origen]  # La ruta inicia y finaliza en origen
    mejor_distancia = evalua_ruta(mejor_ruta, coord)

    mejora = True
    while mejora:
        mejora = False
        for i in range(1, len(ciudades) - 1):
            for j in range(i + 1, len(ciudades)):
                nueva_ruta = [origen] + ciudades[:]
                nueva_ruta[i], nueva_ruta[j] = nueva_ruta[j], nueva_ruta[i]
                nueva_ruta.append(origen)  # Aseguramos que termine en la ciudad origen
                nueva_distancia = evalua_ruta(nueva_ruta, coord)

                if nueva_distancia < mejor_distancia:
                    mejor_ruta = nueva_ruta[:]
                    mejor_distancia = nueva_distancia
                    mejora = True

    return mejor_ruta, mejor_distancia

@app.route('/')
def home():
    return render_template("index.html")  # Carga el frontend correctamente

@app.route('/calcular', methods=['POST'])
def calcular_ruta():
    datos = request.json
    origen = datos.get("origen")

    if not origen or origen not in coord:
        return jsonify({"error": "Selecciona una ciudad válida"}), 400

    ruta, distancia_total = hill_climbing(origen, coord)

    return jsonify({"ruta": ruta, "distancia_total": round(distancia_total, 2)})

if __name__ == "__main__":
    app.run(debug=True)
