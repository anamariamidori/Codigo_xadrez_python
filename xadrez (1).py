import chess
import chess.engine
import time

# import das bibliotecas

# Configurações do tabuleiro e algoritmo de minimax
# criando um novo tabulheiro de xadrez padrão
game = chess.Board()


def minimax_root(depth, game, is_maximising_player):
    # essa função avalia a melhor jogada do estado atual do tabuleiro
    # usando o algoritmo Alfa-Beta, ela é chamada a cada jogada
    new_game_moves = list(game.legal_moves)
    best_move = -9999
    best_move_found = None
    inicio = time.time()

    for move in new_game_moves:
        # aqui ele verifica se é a melhor a jogada
        # se for a melhor jogada ele armazena e ve as proximas
        game.push(move)
        value = minimax(depth - 1, game, -10000, 10000, not is_maximising_player)
        game.pop()
        if value >= best_move:
            best_move = value
            best_move_found = move
            fim = time.time()
        if (fim - inicio) > 120:
            print("ia demorou mais de 2 minutos para pensar")
            game.is_game_over() == True
            break
    return best_move_found  # ele retorna a melhor jogada encontrada


def minimax(depth, game, alpha, beta, is_maximising_player):
    # avalia a posição do tabuleiro se o final da profundidade do algoritmo
    # alfa-beta chega a zero ele chama a função evaluate se não ele utiliza o algoritmo
    # para melhorar o processo de busca
    if depth == 0:
        return -evaluate_board(game)

    new_game_moves = list(game.legal_moves)

    if is_maximising_player:
        best_move = -9999
        for move in new_game_moves:
            game.push(move)
            best_move = max(best_move, minimax(depth - 1, game, alpha, beta, not is_maximising_player))
            game.pop()
            alpha = max(alpha, best_move)
            if beta <= alpha:
                return best_move
        return best_move
    else:
        best_move = 9999
        for move in new_game_moves:
            game.push(move)
            best_move = min(best_move, minimax(depth - 1, game, alpha, beta, not is_maximising_player))
            game.pop()
            beta = min(beta, best_move)
            if beta <= alpha:
                return best_move
        return best_move


def evaluate_board(board):
    total_evaluation = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        total_evaluation += get_piece_value(piece, square)
    return total_evaluation


# Avaliações de posição para diferentes peças
# Define tabelas de avaliação para cada tipo de peça.
# Essas tabelas atribuem um valor específico para cada posição no tabuleiro
# dependendo do tipo e cor da peça.
# As tabelas são usadas para avaliar a vantagem estratégica de cada posição (tirado do artigo "xadrez com ia").
pawn_eval_white = [
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
    [1.0, 1.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0],
    [0.5, 0.5, 1.0, 2.5, 2.5, 1.0, 0.5, 0.5],
    [0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0],
    [0.5, -0.5, -1.0, 0.0, 0.0, -1.0, -0.5, 0.5],
    [0.5, 1.0, 1.0, -2.0, -2.0, 1.0, 1.0, 0.5],
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
]

pawn_eval_black = list(reversed(pawn_eval_white))

knight_eval = [
    [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
    [-4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0],
    [-3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0],
    [-3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 0.5, -3.0],
    [-3.0, 0.0, 1.5, 2.0, 2.0, 1.5, 0.0, -3.0],
    [-3.0, 0.5, 1.0, 1.5, 1.5, 1.0, 0.5, -3.0],
    [-4.0, -2.0, 0.0, 0.5, 0.5, 0.0, -2.0, -4.0],
    [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]
]

bishop_eval_white = [
    [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
    [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
    [-1.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0, -1.0],
    [-1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, -1.0],
    [-1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0],
    [-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0],
    [-1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, -1.0],
    [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]
]

bishop_eval_black = list(reversed(bishop_eval_white))

rook_eval_white = [
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5],
    [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
    [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
    [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
    [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
    [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
    [0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0]
]

rook_eval_black = list(reversed(rook_eval_white))

eval_queen = [
    [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
    [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
    [-1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
    [-0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
    [0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
    [-1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
    [-1.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, -1.0],
    [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]
]

king_eval_white = [
    [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
    [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
    [2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0],
    [2.0, 3.0, 1.0, 0.0, 0.0, 1.0, 3.0, 2.0]
]

king_eval_black = list(reversed(king_eval_white))


def get_piece_value(piece, square):
    # determina o valor de uma peça com base em seu tipo, cor e posição no tabuleiro
    # utilizando as tabelas de avaliação definidas anteriormente.
    if piece is None:
        return 0

    value = 0
    piece_type = piece.piece_type
    color = piece.color

    if piece_type == chess.PAWN:
        value = 10 + (pawn_eval_white[chess.square_rank(square)][chess.square_file(square)] if color == chess.WHITE else
                      pawn_eval_black[chess.square_rank(square)][chess.square_file(square)])
    elif piece_type == chess.KNIGHT:
        value = 30 + knight_eval[chess.square_rank(square)][chess.square_file(square)]
    elif piece_type == chess.BISHOP:
        value = 30 + (
            bishop_eval_white[chess.square_rank(square)][chess.square_file(square)] if color == chess.WHITE else
            bishop_eval_black[chess.square_rank(square)][chess.square_file(square)])
    elif piece_type == chess.ROOK:
        value = 50 + (rook_eval_white[chess.square_rank(square)][chess.square_file(square)] if color == chess.WHITE else
                      rook_eval_black[chess.square_rank(square)][chess.square_file(square)])
    elif piece_type == chess.QUEEN:
        value = 90 + eval_queen[chess.square_rank(square)][chess.square_file(square)]
    elif piece_type == chess.KING:
        value = 900 + (
            king_eval_white[chess.square_rank(square)][chess.square_file(square)] if color == chess.WHITE else
            king_eval_black[chess.square_rank(square)][chess.square_file(square)])

    return value if color == chess.WHITE else -value


# Função para imprimir o tabuleiro
def print_board(board):
    print(board)
    print("\n")


# Loop principal do jogo
while not game.is_game_over():
    print_board(game)

    if game.turn == chess.WHITE:
        # Movimento do usuário
        user_move = input("Digite seu movimento (ex: e2e4 ou 'resign' para abandonar): ")
        if user_move == "resign":
            print("Você desistiu! A IA venceu.")
            break
        try:
            move = chess.Move.from_uci(user_move)
            if move in game.legal_moves:
                game.push(move)
                print("Movimento do jogador:", move)
            else:
                print("Movimento inválido, tente novamente.")
        except:
            print("Entrada inválida, tente novamente.")
    else:
        # Movimento da IA
        print("A IA está pensando...")
        best_move = minimax_root(3, game, True)
        game.push(best_move)
        print(f"A IA jogou: {best_move}")

if not game.is_game_over():
    print("Fim de jogo!")