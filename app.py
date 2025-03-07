
import json
from flask import Flask, jsonify
import joblib
import pandas as pd
from flask_socketio import SocketIO, emit
import logging

app = Flask(__name__)

is_attack = False


@app.route('/toggle_attack', methods=['POST'])
def toggle_attack():
    print("Im from toggle_attack")
    global is_attack
    is_attack = not is_attack  # Toggle the value of is_attack
    return jsonify(IsAttack=is_attack), 200


@app.route('/health', methods=['GET'])
def health():
    # Implement necessary checks to confirm application health
    return jsonify(status="healthy"), 200


socketio = SocketIO(app, cors_allowed_origins="*")

# Load the pre-trained model
model = joblib.load('model/isolation_forest_int_model.joblib')


@socketio.on('connect')
def handle_connect():
    logging.debug("Client connected")
    emit('connection_response', {'message': 'Connected to the server'})


@socketio.on('predict')
def handle_predict(data):
    try:
        if isinstance(data, str):
            data = json.loads(data)
        df = pd.DataFrame([data])
        df = df.astype(int)
        # Get the model's prediction
        prediction = model.predict(df)
        prediction = prediction.tolist()

        # Emit the prediction result back to the client
        emit('prediction_result', {'prediction': prediction[0], 'IsAttack': is_attack})

    except KeyError as e:
        logging.debug({'error': f'Missing parameter: {str(e)}'})
        emit('prediction_error', {'error': f'Missing parameter: {str(e)}'})
    except Exception as e:
        logging.debug({'error': f'Missing parameter: {str(e)}'})
        emit('prediction_error', {'error': str(e)})

@socketio.on('get_attack_status')
def handle_get_attack_status(garbage):
    # Emit the current IsAttack status
    try:
        emit('attack_status', {'IsAttack': is_attack})
    except KeyError as e:
        emit('attack_error', {'error': f'Missing parameter: {str(e)}'})
    except Exception as e:
        emit('attack_error', {'error': str(e)})

    
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)


