from flask import Flask, render_template

app = Flask(__name__)

# Route pour l'accueil
@app.route('/')
def home():
    return render_template('index.html')

# Route pour la page de présentation
@app.route('/action')
def action():
    return render_template('presentation.html')

# Route pour la page "qsj"
@app.route('/who')
def who():
    return render_template('qsj.html')


@app.route('/move')
def move():
    return render_template('move.html')

# Route pour la page du jeu
@app.route('/game')
def game():
    return render_template('jeu.html')

# if __name__ == '__main__':
#     app.run(host='10.216.0.76', port=5000, debug=True, threaded=False)

app.run(debug=True, port=5001)

