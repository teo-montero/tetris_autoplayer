from board import *
from random import Random
import time


INFINITY = 10**15


class Player:
    def choose_action(self, board):
        raise NotImplementedError


class HeuristicPlayer(Player):
    def __init__(self, seed=None):
        self.random = Random(seed)
        
        
    def print_board(self, board):
        for y in range(24):
            for x in range(10):
                print(board[y][x], end = "")
            print()


    def get_board_representation(self, board):
        board_representation = []
        for y in range(24):
            row = []
            for x in range(10):
                if (x,y) in board.cells:
                    row.append(1)
                else:
                    row.append(0)
            board_representation.append(row)
        return board_representation
                
                
    def choose_action(self, board):
        best_score = -INFINITY
        best_moves = []
        
        if board.falling.shape == Shape.I:
            moves = self.process_i_piece(board.clone())
            if moves is not None:
                return moves
        
        for orientation in range(0,4):
            board_with_orientation = board.clone()
            
            orientation_moves = self.orientate_block(board_with_orientation, orientation)
            board_simulation = board_with_orientation.clone()
            if board_simulation.falling is not None:
                prev = board_simulation.score
                pos = board_simulation.falling.left
                board_simulation.move(Direction.Drop)
                current_score = self.calculate_board_score(board_simulation, self.calculate_completed(board_simulation.score - prev), pos) * 0.6 + self.check_next(board_simulation) * 0.4
                if current_score > best_score:
                    best_score = current_score
                    best_moves = orientation_moves.copy()

            current_moves = orientation_moves.copy()
            board_to_left = board_with_orientation.clone()
            while board_to_left.falling.left > (1 if max(self.calculate_height_of_columns(self.get_board_representation(board_to_left))) < 7 else 0): 
                board_to_left.move(Direction.Left)
                current_moves.append(Direction.Left)
                board_simulation = board_to_left.clone()
                if board_simulation.falling is not None:
                    prev = board_simulation.score
                    pos = board_simulation.falling.left
                    board_simulation.move(Direction.Drop)
                    current_score = self.calculate_board_score(board_simulation, self.calculate_completed(board_simulation.score - prev), pos) * 0.6 + self.check_next(board_simulation) * 0.4
                    if current_score > best_score:
                        best_score = current_score
                        best_moves = current_moves.copy()
                else:
                    break
                
            current_moves = orientation_moves.copy()
            board_to_right = board_with_orientation.clone()
            while board_to_right.falling.right < 9: 
                board_to_right.move(Direction.Right)
                current_moves.append(Direction.Right)
                board_simulation = board_to_right.clone()
                if board_simulation.falling is not None:
                    prev = board_simulation.score
                    pos = board_simulation.falling.left
                    board_simulation.move(Direction.Drop)
                    current_score = self.calculate_board_score(board_simulation, self.calculate_completed(board_simulation.score - prev), pos) * 0.6 + self.check_next(board_simulation) * 0.4
                    if current_score >= best_score:
                        best_score = current_score
                        best_moves = current_moves.copy()
                else:
                    break
        return best_moves + [Direction.Drop] 
    
    
    def process_i_piece(self, board):
        moves = []
        previous_score = board.score
        for _ in range(5):
            if board.falling is None:
                return None
            board.move(Direction.Left)
            moves.append(Direction.Left)
        if board.falling is None:
            return None
        board.move(Direction.Drop)
        return moves + [Direction.Drop] if board.score - previous_score >= 400 else None  
    
    
    def check_next(self, board):
        best_score = -INFINITY
        for orientation in range(0,4):
            board_with_orientation = board.clone()
                
            self.orientate_block(board_with_orientation, orientation)
            board_simulation = board_with_orientation.clone()
            if board_simulation.falling is not None:
                prev = board_simulation.score
                pos = board_simulation.falling.left
                board_simulation.move(Direction.Drop)
                current_score = self.calculate_board_score(board_simulation, self.calculate_completed(board_simulation.score - prev), pos)
                best_score = max(best_score, current_score)
            else:
                return best_score

            board_to_left = board_with_orientation.clone()
            while board_to_left.falling.left > (1 if max(self.calculate_height_of_columns(self.get_board_representation(board_to_left))) < 7 else 0): 
                board_to_left.move(Direction.Left)
                board_simulation = board_to_left.clone()
                if board_simulation.falling is not None:
                    prev = board_simulation.score
                    pos = board_simulation.falling.left
                    board_simulation.move(Direction.Drop)
                    current_score = self.calculate_board_score(board_simulation, self.calculate_completed(board_simulation.score - prev), pos)
                    best_score = max(best_score, current_score)
                else:
                    break
                    
            board_to_right = board_with_orientation.clone()
            while board_to_right.falling.right < 9: 
                board_to_right.move(Direction.Right)
                board_simulation = board_to_right.clone()
                if board_simulation.falling is not None:
                    prev = board_simulation.score
                    pos = board_simulation.falling.left
                    board_simulation.move(Direction.Drop)
                    current_score = self.calculate_board_score(board_simulation, self.calculate_completed(board_simulation.score - prev), pos)
                    best_score = max(best_score, current_score)
                else:
                    break
        return best_score

            
    def orientate_block(self, board, orientation):
        if orientation == 0:
            return []       
        elif orientation == 1:
            board.falling.rotate(Rotation.Clockwise, board)
            return [Rotation.Clockwise]
        elif orientation == 2:
            board.falling.rotate(Rotation.Clockwise, board)
            board.falling.rotate(Rotation.Clockwise, board)
            return [Rotation.Clockwise, Rotation.Clockwise]
        elif orientation == 3:
            board.falling.rotate(Rotation.Anticlockwise, board)
            return [Rotation.Anticlockwise]
                
    
    def calculate_board_score(self, board, completed_rows, pos):
        danger = 13
        
        weight_height = 0
        weight_difference = - 1
        weight_maximum = - 10
        weight_rows = 10
        weight_holes = - 10 ** 10
        weight_wells = - 10
        weight_position = 5
        
        danger_height = 0
        danger_difference = - 10
        danger_maximum = - 10 ** 5
        danger_rows = 10
        danger_holes = - 10 ** 10
        danger_wells = - 10
        danger_position = 0
        
        representation = self.get_board_representation(board)
        
        height, difference, maximum, wells = self.calculate_height(representation)
        rows = self.calculate_completed_score(completed_rows, maximum > danger)
        holes = self.calculate_number_of_holes(representation)
        position = pos == 9
        
        if maximum < danger:
            total = height * weight_height + difference * weight_difference + maximum * weight_maximum + rows * weight_rows + holes * weight_holes + wells * weight_wells + position * weight_position
        else:
            total = height * danger_height + difference * danger_difference + maximum * danger_maximum + rows * danger_rows + holes * danger_holes + wells * danger_wells + position * danger_position
            
        return total


    def calculate_height(self, board):
        height = self.calculate_height_of_columns(board)
        return sum(height), self.calculate_difference_in_height_between_adjacent_columns(height), max(height), self.calculate_wells(height)
        
        
    def calculate_height_of_columns(self, board):
        height = []
        for column in range(10):
            current = 0
            for row in range(24):
                if board[row][column]:
                    current = 24 - row
                    break
            height.append(current)
        return height
    
    
    def calculate_difference_in_height_between_adjacent_columns(self, height):
        difference = 0
        for column in range(0, 9):
            if height[column] > height[column+1]:
                difference += (height[column] - height[column+1])**2
            else:
                difference += -1 + (height[column+1] - height[column])
        return difference
    
    
    def calculate_completed(self, difference):
        if 0 <= difference <= 24:
            return 0
        else:
            if 25 <= difference <= 99:
                return 1
            elif 100 <= difference <= 399:
                return 2
            elif 399 <= difference <= 1599:
                return 3
            else:
                return 4
            
    
    def calculate_completed_score(self, rows, danger):
        if rows == 0:
            return 0
        elif rows == 1:
            return 1 if danger else -5
        elif rows == 2:
            return 2 if danger else -3
        elif rows == 3:
            return 5 if danger else -1
        elif rows == 4:
            return INFINITY
    
    
    def calculate_number_of_holes(self, board):
        number_of_holes = 0
        for column in range(0,10):
            holes_in_column = 0
            hole_buffer = 0
            for row in range(23, -1, -1):
                if board[row][column]:
                    holes_in_column += hole_buffer
                    hole_buffer = 0
                else:
                    hole_buffer += 1
            number_of_holes += holes_in_column
        return number_of_holes
    

    def calculate_wells(self, height):
        wells = 0
        for column in range(1,9):
            if height[column] + 1 < height[column-1] and height[column] + 1 < height[column+1]:
                wells += (height[column-1] - height[column]) + (height[column-1] - height[column])
        wells += (height[8] - height[9])**6 if height[9] + 1 < height[8] else 0
        if max(height) == height[9]:
            wells -= 10**4
        if max(height) > 15 and height.index(max(height)) < 4:
            wells += 10**4
        return wells
                    
                    
    def calculate_position_score(self, position):
        if position < 5:
            return 3 - position
        else:
            return position - 3
        
                    
SelectedPlayer = HeuristicPlayer
