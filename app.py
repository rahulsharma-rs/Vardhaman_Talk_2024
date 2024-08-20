from flask import Flask, request, jsonify, render_template
from pycaret.classification import load_model, predict_model
import pandas as pd

app = Flask(__name__)

# Load the model
model = load_model('final_rf_iris_model')

@app.route('/')
def index():
    return render_template('prediction.html')
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract features from the POST request
        data = request.json
        df = pd.DataFrame([data])

        # Predict
        predictions = predict_model(model, data=df)

        # Prepare and send the response
        response = {
            'predicted_class': predictions['prediction_label'][0],
            'probability': predictions['prediction_score'][0]}
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)
