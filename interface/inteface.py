from flask import Flask, render_template, request, jsonify
import random

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

# Route pour la page du jeu de morpion
@app.route('/morpion')
def morpion():
    return render_template('morpion.html')

# Route API pour gérer le jeu et l'IA
@app.route('/play', methods=['POST'])
def play():
    data = request.json
    board = data['board']
    
    # Vérifier si le joueur humain a gagné
    winner = check_winner(board)
    if winner:
        return jsonify({"winner": winner, "board": board})

    # Tour de l'IA (si le jeu n'est pas terminé)
    ia_move = get_best_move(board, "O")  
    if ia_move is not None:
        board[ia_move] = "O"

    # Vérifier si l'IA a gagné après son coup
    winner = check_winner(board)
    return jsonify({"winner": winner, "board": board})

def check_winner(board):
    """Vérifie si un joueur a gagné"""
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Lignes
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Colonnes
        [0, 4, 8], [2, 4, 6]              # Diagonales
    ]
    
    for condition in win_conditions:
        a, b, c = condition
        if board[a] == board[b] == board[c] and board[a] != "":
            return board[a]
    
    if "" not in board:
        return "draw"  # Match nul
    
    return None  # Le jeu continue

def get_best_move(board, player):
    """Retourne le meilleur coup pour l'IA"""
    empty_cells = [i for i in range(9) if board[i] == ""]

    # Si l'IA peut gagner en un coup, elle le joue
    for move in empty_cells:
        board_copy = board[:]
        board_copy[move] = player
        if check_winner(board_copy) == player:
            return move

    # Si l'adversaire peut gagner en un coup, l'IA bloque
    opponent = "X" if player == "O" else "O"
    for move in empty_cells:
        board_copy = board[:]
        board_copy[move] = opponent
        if check_winner(board_copy) == opponent:
            return move

    # Si aucune menace immédiate, choisir une case au hasard
    return random.choice(empty_cells) if empty_cells else None

# if __name__ == '__main__':
#     app.run(host='10.216.0.76', port=5000, debug=True, threaded=False)

app.run(debug=True, port=5001)

