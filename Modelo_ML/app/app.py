import pickle
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/v2/predict', methods=['POST'])
def predict():
    # Cargar el modelo entrenado
    model = pickle.load(open('trained_model.pkl', 'rb'))

    # Obtener los datos de entrada del cuerpo JSON de la solicitud
    data = request.get_json()

    if not data:
        return "Missing JSON data in the request body"

    # Obtener los valores de las características de entrada
    compacidad_relativa = data.get('compacidad_relativa', None)
    area_pared = data.get('area_pared', None)
    area_techo = data.get('area_techo', None)
    altura_total = data.get('altura_total', None)
    orientacion = data.get('orientacion', None)
    area_acristalamiento = data.get('area_acristalamiento', None)

    if (
        compacidad_relativa is None
        or area_pared is None
        or area_techo is None
        or altura_total is None
        or orientacion is None
        or area_acristalamiento is None
    ):
        return "Missing args, all input values are needed to predict"
    else:
        # Realizar la predicción con el modelo
        prediction = model.predict([[
            float(compacidad_relativa),
            float(area_pared),
            float(area_techo),
            float(altura_total),
            int(orientacion),
            float(area_acristalamiento)
        ]])

        # Devolver la predicción en el formato deseado en la respuesta JSON
        response = {
            'prediction': prediction[0]  # Mantener la predicción sin redondeo
        }

        return jsonify(response)


if __name__ == '__main__':
  app.run(debug = True, host = '0.0.0.0', port=os.environ.get("PORT", 5000))