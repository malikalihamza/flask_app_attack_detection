# import json
#
# from flask import Flask, request, jsonify
# import joblib
# import numpy as np
# import pandas as pd
# from flask_cors import CORS
#
# app = Flask(__name__)
# CORS(app)
#
# # Load the pre-trained model
# model = joblib.load('model/isolation_forest_model.joblib')  # Replace with your model's path
#
#
# @app.route('/predict', methods=['POST'])
# def predict():
#     try:
#         # Get the JSON data from the request
#         data = request.get_json()
#         df = pd.DataFrame([data])
#         df = df.rename(columns={
#             'eye_gaze_time_diff': 'TimeBetweenEyegazeChanges',
#             'fps': 'fps',
#             'cpu_jitter_time': 'CPU Total Frame Time Jitter'
#         })
#
#         # Get the model's prediction
#         prediction = model.predict(df)
#         prediction = prediction.tolist()
#
#         # Create a response dictionary
#         response = {
#             'prediction': prediction[0]  # Assuming the model returns a single prediction
#         }
#
#         return json.dumps(response)
#
#     except KeyError as e:
#         return jsonify({'error': f'Missing parameter: {str(e)}'}), 400
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
#
#
# if __name__ == '__main__':
#     app.run(debug=True)

# socket code
import json
from flask import Flask, jsonify
import joblib
import pandas as pd
from flask_socketio import SocketIO, emit

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    # Implement necessary checks to confirm application health
    return jsonify(status="healthy"), 200


socketio = SocketIO(app, async_mode='eventlet', cors_allowed_origins="*")

# Load the pre-trained model
model = joblib.load('model/isolation_forest_model.joblib')  # Replace with your model's path


@socketio.on('sudo')
def handle_predict(data):
    try:
        df = pd.DataFrame([data])
        df = df.rename(columns={
            'eye_gaze_time_diff': 'TimeBetweenEyegazeChanges',
            # 'fps': 'fps',
            'cpu_jitter_time': 'CPU Total Frame Time Jitter'
        })

        # Get the model's prediction
        prediction = model.predict(df)
        prediction = prediction.tolist()

        # Emit the prediction result back to the client
        emit('prediction_result', {'prediction': prediction[0]})

    except KeyError as e:
        emit('prediction_error', {'error': f'Missing parameter: {str(e)}'})
    except Exception as e:
        emit('prediction_error', {'error': str(e)})


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)


