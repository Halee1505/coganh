def minimax_score(board, depth, maximizing_player):
    if depth == 0 or game_over(board):
        return evaluate_board(board)

    if maximizing_player:
        best_value = -float('inf')
        for move in get_possible_moves(board):
            new_board = make_move(board, move)
            value = minimax_score(new_board, depth - 1, False)
            best_value = max(best_value, value)
        return best_value
    else:
        best_value = float('inf')
        for move in get_possible_moves(board):
            new_board = make_move(board, move)
            value = minimax_score(new_board, depth - 1, True)
            best_value = min(best_value, value)
        return best_value


def get_best_move(board, depth):
    best_value = -float('inf')
    best_move = None
    for move in get_possible_moves(board):
        new_board = make_move(board, move)
        value = minimax_score(new_board, depth - 1, False)
        if value > best_value:
            best_value = value
            best_move = move
    return best_move
