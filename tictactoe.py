"""
Tic Tac Toe Player
"""

import numpy as np
from re import I
from numpy import append

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Devuelve el estado inicial del tablero.
    """

    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Devuelve el jugador que juega el turno.
    """

    # Contamos las celdas vacias en el tablero
    celdas_vacias = cuentaHuecos(board) 

    # Si son pares, juega X. Si son impares, juega O
    if celdas_vacias%2==0:
        return O
    else:
        return X


def actions(board):
    """
    Devuelve todos los posibles movimientos (i, j) disponibles en el tablero.
    """
    coords = []

    # Recorremos el tablero y en caso de que haya una celda vacia, la agregamos a la lista
    for i in range(0,3):
        for j in range(0,3):
            if board[i][j] == None: 
                coords.append([i,j]) 

    return coords


def result(board, action):
    """
    Devuelve el tablero resultante de hacer la accion (i, j) sobre el tablero que entra como parametro.
    """
    # Llamamos a player() para ver a quien le toca jugar
    player_now = player(board)

    # Hacemos una copia del tablero que entra por parametro
    newBoard = duplicaBoards(board)

    i=action[0]
    j=action[1]
    newBoard[i][j] = player_now
    
    return newBoard


def winner(board):
    """
    Devuelve el ganador del juego, en caso de que lo haya.
    """
    for i in range(0,3):
        # Comprobamos filas
        if(board[i][0] == board[i][1] and board[i][1] == board[i][2] and board[i][0] != EMPTY): 
            return board[i][0]

        # Comprobamos las columnas
        elif(board[0][i] == board[1][i] and board[1][i] == board[2][i] and board[0][i] != EMPTY): 
            return board[0][i]

    # Comprobamos diagonales
    if(board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[1][1] != EMPTY): 
        return board[1][1]

    elif(board[2][0] == board[1][1] and board[1][1] == board[0][2] and board[1][1] != EMPTY): 
        return board[1][1]

    else: return None


def terminal(board):
    """
    Devuelve True si el juego ha acabado, y False en caso contrario.
    """
    # Llamamos a winner() para ver si hay un ganador
    ganador = winner(board)

    if ganador == None: # Si no hay ganador, comprobamos si ha habido empate
        if hay_empate(board):
            return True

        else: 
            return False

    else: return True
    

def utility(board):
    """
    Devuelve 1 si X ha ganado la partida, -1 si ha ganado O, y 0 en caso contrario.
    """
    ganador = winner(board)

    if ganador == X: 
        return 1

    elif ganador == O: 
        return -1
    else: 
        return 0


def minimax(board):
    """
    Devuelve el mejor movimiento para el jugador y tablero actuales.
    """
    if terminal(board):
       return None

    elif player(board) == X:
        movimientos = []
        for mov in actions(board):
            pseudo_board = result(board, mov) # Obtenemos el escenario en caso de hacer el movimiento mov
            valor_min = minValue(pseudo_board)
            movimientos.append([valor_min, mov]) # Almacenamos en una lista los pares de movimientos posibles asi como sus puntuaciones asociadas

        return sorted(movimientos, key=lambda x: x[0], reverse=True)[0][1]

    elif player(board) == O:
        movimientos = []
        for mov in actions(board):
            pseudo_board = result(board, mov) # Obtenemos el escenario en caso de hacer el movimiento mov
            valor_max = maxValue(pseudo_board)
            movimientos.append([valor_max, mov]) # Almacenamos en una lista los pares de movimientos posibles asi como sus puntuaciones asociadas

        return sorted(movimientos, key=lambda x: x[0])[0][1]

def maxValue(board):
    # Comprobamos si el juego ha acabado con terminal() y devolvemos el valor que nos da utility()
    if terminal(board):         
        return utility(board)  

    v = float("-inf")
    # Recorremos todos los posibles movimientos y nos quedamos con el que tenga maximo valor
    for position in actions(board):
        valor_min = minValue(result(board, position))
        v = max(v, valor_min)

    return v

def minValue(board):
    # Comprobamos si el juego ha acabado con terminal() y devolvemos el valor que nos da utility()
    if terminal(board):
        return utility(board)

    v = float("inf")
    # Recorremos todos los posibles movimientos y nos quedamos con el que tenga menor valor
    for position in actions(board):
        valor_max = maxValue(result(board, position))
        v = min(v, valor_max)

    return v

# funcion auxiliar
def duplicaBoards(board):
    '''
    Devuelve una copia del tablero que recibe por parametro sin enlazar ambos tableros
    '''
    newBoard = initial_state()

    for i in range(0,3):
        for j in range(0,3):
            newBoard[i][j] = board[i][j]

    return newBoard

# funcion auxiliar
def hay_empate(board):
    '''
    Devuelve True si hay empate, False en caso contrario
    '''
    celdas_vacias = cuentaHuecos(board)

    if celdas_vacias == 0: 
        return True
    else: 
        return False
    
# funcion auxiliar
def cuentaHuecos(board):
    '''
    Devuelve el numero de celdas vacias    
    '''
    celdas_vacias = 0

    for i in range(0,3):
        for j in range(0,3):
            if board[i][j] == EMPTY: 
                celdas_vacias += 1

    return celdas_vacias