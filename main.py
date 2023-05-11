from flask import Flask, render_template, request, redirect, url_for
import yfinance as yf
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/grafico', methods=['POST'])
def gerar_grafico():
    acao = request.form['acao']
    dados = yf.download(acao+'.SA', period='1y')
    plt.figure()
    plt.plot(dados['Close'])
    plt.xlabel('Data')
    plt.ylabel('Preço de fechamento (R$)')
    plt.title('Gráfico de preços de fechamento dos últimos 12 meses')
    img = BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    grafico_url = base64.b64encode(img.getvalue()).decode()
    return render_template('grafico.html', grafico_url=grafico_url)

if __name__ == '__main__':
    app.run(debug=True)