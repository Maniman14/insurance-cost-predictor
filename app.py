from flask import Flask, render_template, request, redirect, url_for, session
import joblib
import numpy as np

app = Flask(__name__)
app.secret_key = 'change-this-to-any-random-string'  # needed for session to work
model = joblib.load('model.pkl')

@app.route('/')
def home():
    # pop, not get, so the result only shows once and clears on the next reload
    prediction_text = session.pop('prediction_text', None)
    return render_template('index.html', prediction_text=prediction_text)

@app.route('/predict', methods=['POST'])
def predict():
    age = float(request.form['age'])
    bmi = float(request.form['bmi'])
    children = int(request.form['children'])
    smoker = 1 if request.form['smoker'] == 'yes' else 0
    sex = 1 if request.form['sex'] == 'male' else 0
    region = int(request.form['region'])
    features = np.array([[age, bmi, children, smoker, sex, region]])
    prediction = model.predict(features)[0]

    session['prediction_text'] = f'Estimated Cost: ${prediction:.2f}'
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)