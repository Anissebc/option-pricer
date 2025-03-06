from flask import Flask, request, render_template_string
import numpy as np
from scipy.stats import norm

app = Flask(__name__)

def calculate_bs_price(S, K, T, r, sigma, option_type):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type == "call":
        return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == "put":
        return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    
    return "Invalid option type"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Option Pricer</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .container { max-width: 600px; margin: auto; }
        h1 { text-align: center; }
        form { display: flex; flex-direction: column; gap: 15px; }
        label { font-weight: bold; }
        input, select, button { padding: 10px; font-size: 16px; }
        button { background-color: #4CAF50; color: white; border: none; cursor: pointer; }
        button:hover { background-color: #45a049; }
        .result { margin-top: 20px; font-size: 18px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Option Pricer</h1>
        <form method="post">
            <label>Prix actuel (S) :</label>
            <input type="number" name="spot_price" step="0.01" required>
            
            <label>Prix d'exercice (K) :</label>
            <input type="number" name="strike_price" step="0.01" required>
            
            <label>Échéance (jours) :</label>
            <input type="number" name="maturity" required>
            
            <label>Taux sans risque (r) :</label>
            <input type="number" name="risk_free_rate" step="0.0001" value="0.03" required>
            
            <label>Volatilité (σ) :</label>
            <input type="number" name="volatility" step="0.0001" required>
            
            <label>Type d'option :</label>
            <select name="option_type">
                <option value="call">Call</option>
                <option value="put">Put</option>
            </select>
            
            <button type="submit">Calculer</button>
        </form>
        
        {% if result %}
        <div class="result">
            <p><strong>Résultat :</strong> {{ result }}</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def option_pricer():
    result = None
    if request.method == 'POST':
        try:
            S = float(request.form['spot_price'])
            K = float(request.form['strike_price'])
            T = int(request.form['maturity']) / 365  # Conversion en années
            r = float(request.form['risk_free_rate'])
            sigma = float(request.form['volatility'])
            option_type = request.form['option_type']
            
            price = calculate_bs_price(S, K, T, r, sigma, option_type)
            result = f'Le prix de l\'option {option_type} est : {price:.2f}'
        except Exception as e:
            result = f"Erreur : {e}"
    
    return render_template_string(HTML_TEMPLATE, result=result)

if __name__ == '__main__':
    app.run(debug=True)

