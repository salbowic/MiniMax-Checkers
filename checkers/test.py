import pygame
from config import *
from minimax import *
from game import Game
from pawn import Pawn
from king import King
from copy import deepcopy


class Test:
    
    def status_line(board, eval):
        moves_a_c = board.moves_after_capture_or_new_king
        if eval == 1:
            h_s = board.evaluate()
        elif eval == 2:
            h_s = board.tight_evaluate(False)
        elif eval == 3:
            h_s = board.half_evaluate()
        elif eval == 4:
            h_s = board.closer_better_evaluate()
        white_pawns = 0
        white_kings = 0
        blue_pawns = 0
        blue_kings = 0
        for row in range(BOARD_WIDTH):
                for col in range((row+1) % 2, BOARD_WIDTH, 2):
                    field = board.board[row][col]

                    if field.is_white():
                        if isinstance(field, Pawn):
                            if isinstance(field, King):
                                white_kings += 1
                            else:
                                white_pawns += 1

                    elif field.is_blue():
                        if isinstance(field, Pawn):
                            if isinstance(field, King):
                                blue_kings += 1
                            else:
                                blue_pawns += 1

        h_s = round(h_s, 3)
        status_line = f"\rWhite: {white_pawns} ♙  {white_kings} ♔  | Blue: {blue_pawns} ♙  {blue_kings} ♔  | Moves to draw: {50 - moves_a_c} | h(s): {h_s}    "
        print(status_line, end="", flush=True)

    def determinate_winner(board):
        h_s = board.evaluate()

        if h_s == -1000:
            winner_text = "\nWhite wins!" 
        elif h_s == 1000:
            winner_text = "\nBlue wins!"
        elif h_s == 0:
            winner_text = "\nDraw (Noone can force the win)"
        else:
            winner_text = "error"
        
        return winner_text

    def play_against_ai(play_white, ai_depth):
        window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        is_running = True
        clock = pygame.time.Clock()
        game = Game(window)

        while is_running:
            clock.tick(FPS)
            Test.status_line(deepcopy(game.board), 1)

            if game.board.end():
                is_running = False
                winner_text = Test.determinate_winner(deepcopy(game.board))

                print(winner_text)
                pygame.time.delay(2000)
                break

            if play_white:
                if not game.board.white_turn:
                    move = minimax_a_b(deepcopy(game.board), ai_depth)
                    game.board.make_ai_move(move)
            else:
                if game.board.white_turn:
                    move = minimax_a_b(deepcopy(game.board), ai_depth)
                    game.board.make_ai_move(move)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    game.clicked_at(pos)

            game.update()

        pygame.quit()
        return(winner_text)
    
    def ai_vs_ai_visualisation(white_depth, blue_depth):
        window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        is_running = True
        clock = pygame.time.Clock()
        game = Game(window)

        while is_running:
            clock.tick(FPS)
            Test.status_line(deepcopy(game.board), 2)

            if game.board.end():
                is_running = False
                winner_text = Test.determinate_winner(deepcopy(game.board))

                pygame.time.delay(2000)
                break

            elif not game.board.white_turn:
                move = minimax_a_b(deepcopy(game.board), blue_depth)
                game.board.make_ai_move(move)
                game.update()
                pygame.time.delay(500)

            elif game.board.white_turn:
                move = minimax_a_b(deepcopy(game.board), white_depth)
                game.board.make_ai_move(move)
                game.update()
                pygame.time.delay(500)

        pygame.quit()
        return(winner_text)

    def depth(white_depth, blue_depth):
        game = Game(None)
        starting_moves = game.board.get_possible_moves(False)

        blue_wins = 0
        white_wins = 0
        draws = 0
        
        for start_move in starting_moves:
            
            is_running = True
            game = Game(None)
            game.board.make_ai_move(start_move)

            while is_running:
                #Test.status_line(game.board, 2)

                if game.board.end():
                    is_running = False

                    result = Test.determinate_winner(deepcopy(game.board))
                    if result == "\nBlue wins!":
                        blue_wins+=1
                    elif result == "\nWhite wins!":
                        white_wins+=1
                    elif result == "\nDraw (Noone can force the win)":
                        draws+=1

                    print(result)
                    break

                elif not game.board.white_turn:
                    move = minimax_a_b( deepcopy(game.board), blue_depth)
                    game.board.make_ai_move(move)

                elif game.board.white_turn:
                    move = minimax_a_b( deepcopy(game.board), white_depth)
                    game.board.make_ai_move(move)
  
        podsumowanie = str(white_wins) + "-" + str(draws) + "-" + str(blue_wins)
        return podsumowanie

    def eval(white_depth, blue_depth, h_s):
        game = Game(None)
        starting_moves = game.board.get_possible_moves(False)

        blue_wins = 0
        white_wins = 0
        draws = 0
        
        for start_move in starting_moves:
            
            is_running = True
            game = Game(None)
            game.board.make_ai_move(start_move)

            while is_running:
                #Test.status_line(game.board, 2)

                if game.board.end():
                    is_running = False

                    result = Test.determinate_winner(deepcopy(game.board))
                    if result == "\nBlue wins!":
                        blue_wins+=1
                    elif result == "\nWhite wins!":
                        white_wins+=1
                    elif result == "\nDraw (Noone can force the win)":
                        draws+=1

                    print(result)
                    break

                elif not game.board.white_turn:
                    move = minimax_a_b_dif_eval( deepcopy(game.board), blue_depth, 1)
                    game.board.make_ai_move(move)

                elif game.board.white_turn:
                    move = minimax_a_b_dif_eval( deepcopy(game.board), white_depth, h_s)
                    game.board.make_ai_move(move)
  
        podsumowanie = str(white_wins) + "-" + str(draws) + "-" + str(blue_wins)
        return podsumowanie

    def save_depth_results(white_depth_start, white_depth_end, blue_depth):
        results = [] 
        for white_depth in range(white_depth_start, white_depth_end + 1):
            summary = Test.depth(white_depth, blue_depth)
            results.append({
                "depth": white_depth,
                "summary": summary,
            })

            print("live record (W - draw - B): ", summary)

        results_df = pd.DataFrame(results)
        results_df.to_excel(f"results_depth_test.xlsx", index=False)

    def save_eval_results():
        results = [] 
        for h_s in range(1,5):
            summary = Test.eval(5, 5, h_s)
            results.append({
                "evaluation function": h_s,
                "summary": summary,
            })

            print("live record (W - draw - B): ", summary)

        results_df = pd.DataFrame(results)
        results_df.to_excel(f"results_eval_test.xlsx", index=False)
