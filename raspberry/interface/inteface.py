#!/bin/python3

from flask import Flask, render_template, request, jsonify, Response
import random
import cv2
import serial
import time

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

# # URL du flux vidéo (à adapter si nécessaire)
# url = "http://127.0.0.1:4747/video"
# cap = cv2.VideoCapture(url)

# def generate_frames():
#     while True:
#         success, frame = cap.read()
#         if not success:
#             break
#         else:
#             # Encodage en JPEG
#             ret, buffer = cv2.imencode('.jpg', frame)
#             frame = buffer.tobytes()

#             # Génération des frames en format MJPEG
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            
# # Route qui envoie le flux vidéo
# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
# Connexion au port série de l'Arduino


arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)

# Dictionnaire des commandes
mouvements = {
    "Stop": "1", "Go_Forward": "2", "Go_Backward": "3",
    "Go_Turnright": "4", "Go_Turnleft": "5", "Up_tab": "u", "Down_Tab": "d"
}

def envoie_donnee(mouvement):
    if mouvement in mouvements:
        message = str(mouvements[mouvement])
        arduino.write((message + '\n').encode())
        print(f"Commande envoyée: {mouvement} ({message})")
        
        reponse = arduino.readline().decode().strip()
        if reponse:
            print("Réponse de l'Arduino:", reponse)
        return reponse
    return "Commande inconnue"

@app.route('/robot/<action>', methods=['POST'])
def robot_action(action):
    envoie_donnee(action)  # On envoie la commande sans retourner une réponse bloquante
    return ('', 204)  # Réponse HTTP 204 : No Content (évite toute pop-up)


if __name__ == '__main__':
    app.run(host='192.168.42.10', port=5000, debug=True, threaded=False)

# app.run(debug=True, port=5001)

