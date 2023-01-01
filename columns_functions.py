EMPTY = ' '

FALLER_STOPPED = 0
FALLER_MOVING = 1

MOVE_DOWN  = 0
MOVE_LEFT  = -1
MOVE_RIGHT = 1

def _maximum(a, b):
    '''
    Returns the bigger of two objects
    ''' 
    if a >= b:
        return a
    else:
        return b

class Faller:
    def __init__(self):
        '''
        Constructs a new faller object and initializes all the values
        '''
        self.active = False
        self._row = 0
        self._col = 0
        self.contents = [EMPTY, EMPTY, EMPTY]
        self.state = FALLER_MOVING
        self.inbounds = False
        self.valid = True

    def get_row(self) -> int:
        '''
        Returns the row of the Faller object
        '''
        return self._row

    def get_col(self) -> int:
        '''
        Returns the column of the Faller object
        '''
        return self._col

    def set_row(self, row: int) -> None:
        '''
        Changes the row of the Faller object
        '''
        self._row = row

    def set_col(self, col: int) -> None:
        '''
        Changes the column of the Faller object
        '''
        self._col = col

    def find_bound(self) -> bool:
        '''
        Checks if the Faller object is in the boundaries
        '''
        return self.inbounds

    def rotate(self) -> None:
        '''
        Rotates all the values in the Faller object down one where
        the bottom most value becomes the top most
        '''
        if self.state != FALLER_STOPPED_CELL:
            jewelOne = self.contents[2]
            jewelTwo = self.contents[0]
            jewelThree = self.contents[1]
            self.contents = [jewelOne, jewelTwo, jewelThree]


# State of a cell
EMPTY_CELL = 0
FALLER_MOVING_CELL = 1
FALLER_STOPPED_CELL = 2
OCCUPIED_CELL = 3
MATCHED_CELL = 4

class GameState:
    def __init__(self, columns: int, rows: int):
        '''
        Constructs a new GameState with a board using the given columns and rows
        '''
        self._rows = rows
        self._columns = columns
        self._board = []
        self._boardState = []
        self._faller = Faller()
        self.new_game(columns, rows)

    def new_game(self, columns: int, rows: int) -> None:
        '''
        Adds all the values to create an empty board
        '''
        for col in range(columns):
            self._board.append([])
            self._boardState.append([])
            for row in range(rows):
                self._board[-1].append(EMPTY)
                self._boardState[-1].append(EMPTY_CELL)

    def add_content(self, contentRow: int, content: list) -> None:
        '''
        Replaces the values in the original row with the values in the row given
        '''
        for row in range(self._rows):
            for col in range(self._columns):
                if contentRow == row:
                    self._board[col][row] = content[col]
                    if content[col] != ' ':
                        self._boardState[col][row] = OCCUPIED_CELL
                    else:
                        self._boardState[col][row] = EMPTY_CELL

    def columns(self) -> int:
        '''
        Returns the number of columns
        '''
        return self._columns

    def rows(self) -> int:
        '''
        Returns the number of rows
        '''
        return self._rows

    def get_board(self):
        '''
        Returns the board
        '''
        return self._board

    def get_cell_state(self, col: int, row: int) -> int:
        '''
        Returns the board that has the cell states
        '''
        try:    
            return self._boardState[col][row]
        except:
            None

    def set_cell_state(self, col: int, row: int, state: int) -> None:
        '''
        Replaces the cell state of a specific point on the board if valid
        '''
        if row < 0:
            return
        self._boardState[col][row] = state

    def apply_gravity(self) -> None:
        '''
        Drags cells that have empty spaces beneath until they reach the
        bottom most row or an occupied cell
        '''
        for iter in range(0, self.rows()):
            for row in range(iter, self.rows()+1):
                for col in range(self.columns()):
                    if self._board[col][-(row)+1] == ' ' and self._board[col][-(row)] != ' ' and (-(row)+1) != 0:
                        jewel = self._board[col][-(row)]
                        self._board[col][-(row)+1] = jewel
                        self._board[col][-(row)] = ' '
                        self._boardState[col][-(row)+1] = OCCUPIED_CELL
                        self._boardState[col][-(row)] = EMPTY_CELL
        
    def do_matching(self) -> None:
        '''
        Looks for lines of cells with the same value of three or more and
        deletes them, then applies gravity
        '''
        if self._faller.active == False or self._faller.state == FALLER_STOPPED:
            matching = False
            #Deletes the matched cells
            for row in range(self.rows()):
                for col in range(self.columns()):
                    if self._boardState[col][row] != EMPTY_CELL:
                        print("({},{}) has state {}".format(col, row, self._boardState[col][row]))
                    if self.get_cell_state(col, row) == MATCHED_CELL:
                        matching = True
                        self._board[col][row] = EMPTY
                        self.set_cell_state(col, row, EMPTY_CELL) 
                        print("Erase Col{}, Row{}".format(col, row))                   

            #Starts matching
            for col in range(self.columns()):
                for row in range (self.rows()):
                    self._matching_begins(col, row)
            if matching == True:
                self.apply_gravity()
                self.do_matching()
            matching = False
                        

    def get_faller(self) -> Faller:
        '''
        Returns the faller object in the GameState
        '''
        return self._faller

    def create_faller(self, column: int, faller_contents: list) -> None:
        '''
        Creates a faller using the given column and the given contents
        '''
        if self._faller.active:
            return

        self._faller.active = True
        self._faller.contents = faller_contents
        self._faller.set_row(0)
        self._faller.set_col(column - 1)
        self._faller.inbounds = False

        #Moves the bottom most cell of the faller into the board
        self._board[self._faller.get_col()][0] = self._faller.contents[0]
        self.set_cell_state(self._faller.get_col(), 0, FALLER_MOVING_CELL)        

        self._update_faller_board_state()

    def rotate_faller(self) -> None:
        '''
        Rotates the faller and updates the board
        '''
        self._faller.rotate()
        self._update_faller_board_state()

    def game_tick(self) -> bool:
        '''
        Ticks one time unit for the game
        Causes faller to move down if possible and do matching 
        '''
        if not self._faller.inbounds:
            self._faller.valid = False
        #Faller needs to be active
        if self._faller.active:
            
            if self._faller.state == FALLER_STOPPED:
                # Do another update on the faller state to see what state it is now 
                self._update_faller_board_state()

                if self._faller.state == FALLER_STOPPED:
                    value = False

                    #Freeze the faller cells on the board
                    for inx in range(3):
                        row = self._faller.get_row() - inx
                        if (row >= 0):
                            self._board[self._faller.get_col()][row] = self._faller.contents[inx]
                            # Check if this cell is in 'MATCHED' status
                            if self.get_cell_state(self._faller.get_col(), row) != MATCHED_CELL:
                                self.set_cell_state(self._faller.get_col(), row, OCCUPIED_CELL)
                    self._faller.active = False
                    if not self._faller.valid:
                        return True
                    self.do_matching()
                    return value

            #If the faller is still moving, move it down
            self.move_faller_down()

        #Handle matching
        self.do_matching()
        return False

    def move_faller_down(self) ->None:
        '''
        Attempts to move the faller object down
        '''
        if (self._has_collision(self._faller.get_col(), self._faller.get_row() + 1)):
            return
        
        rowOfFaller = self._faller.get_row()
        colOfFaller = self._faller.get_col()
        self._move_cell(colOfFaller, rowOfFaller, MOVE_DOWN)
        self._move_cell(colOfFaller, rowOfFaller - 1, MOVE_DOWN)
        self._move_cell(colOfFaller, rowOfFaller - 2,  MOVE_DOWN)
        
        #Set the faller down one row (row number increases by one)
        self._faller.set_row(rowOfFaller + 1)
        self._update_faller_board_state()
        if self._faller._row >= 2:
            self._faller.inbounds = True
            self._faller.valid = True

    def move_faller_right(self) -> None:
        '''
        Attempts to move the faller object to the right
        '''
        if (self._has_collision(self._faller.get_col() + 1, self._faller.get_row())):
            return
        
        rowOfFaller = self._faller.get_row()
        colOfFaller = self._faller.get_col()
        self._move_cell(colOfFaller, rowOfFaller, MOVE_RIGHT)
        self._move_cell(colOfFaller, rowOfFaller - 1, MOVE_RIGHT)
        self._move_cell(colOfFaller, rowOfFaller - 2,  MOVE_RIGHT)
        
        # Set the faller down one column (column number increases by one)
        if self._faller._col >= 0:
            self._faller.set_col(colOfFaller + 1)
            self._update_faller_board_state()

    def move_faller_left(self) -> None:
        '''
        Attempts to move the faller object to the left
        '''
        if (self._has_collision(self._faller.get_col() - 1, self._faller.get_row())):
            return
        
        rowOfFaller = self._faller.get_row()
        colOfFaller = self._faller.get_col()
        self._move_cell(colOfFaller, rowOfFaller, MOVE_LEFT)
        self._move_cell(colOfFaller, rowOfFaller - 1, MOVE_LEFT)
        self._move_cell(colOfFaller, rowOfFaller - 2,  MOVE_LEFT)
        
        # Set the faller up one column (column number decreases by one)
        if colOfFaller > 0:
            self._faller.set_col(colOfFaller - 1)
            self._update_faller_board_state()

    def _update_faller_board_state(self) -> None:
        '''
        Updates the state of the faller according to its current conditions.
        If the faller reaches the bottom row then the state is set to FALLER_STOPPED.
        Otherwise the state is set to FALLER_MOVING.
        The cells of the faller on the board are updated as well.
        '''
        state = None
        toRow = self._faller.get_row() + 1
        if self._has_collision(self._faller.get_col(), toRow):
            state = FALLER_STOPPED_CELL
            self._faller.state = FALLER_STOPPED
        else:
            state = FALLER_MOVING_CELL
            self._faller.state = FALLER_MOVING

        for inx in range(3):
            row = self._faller.get_row() - inx
            if row < 0:
                return

            #Update board cell
            try:
                self._board[self._faller.get_col()][row] = self._faller.contents[inx]
                if self.get_cell_state(self._faller.get_col(), row) != MATCHED_CELL:
                    self.set_cell_state(self._faller.get_col(), row, state)
            except:
                self._faller._col = self._faller._col - 1

    def _has_collision(self, col: int, row: int) -> bool:
        '''
        Checks if a cell of the given row and column has collision (touch occupied cell or the bottom row)
        Return True if the given cell has collision. False otherwise
        '''
        if row >= self.rows():
            return True

        if self.get_cell_state(col, row) == OCCUPIED_CELL:
            return True

        return False
        
    def _move_cell(self, col: int, row: int, direction: int) -> None:
        '''
        Moves a cell in the given direction
        '''
        if col >= 0 and row >= 0:

            if direction == MOVE_DOWN:
                toRow = row + 1
                if (toRow >= self.rows() or toRow < 0):
                    return

                oldValue = self._board[col][row]
                oldState = self._boardState[col][row]

                self._board[col][toRow] = oldValue
                self._boardState[col][toRow] = oldState

            elif direction == MOVE_RIGHT:
                toCol = col + 1
                if (toCol >= self.columns() or toCol < 0):
                    return

                oldValue = self._board[col][row]
                oldState = self._boardState[col][row]

                self._board[toCol][row] = oldValue
                self._boardState[toCol][row] = oldState

            elif direction == MOVE_LEFT:
                toCol = col - 1
                if (toCol >= self.columns() or toCol < 0):
                    return

                oldValue = self._board[col][row]
                oldState = self._boardState[col][row]

                self._board[toCol][row] = oldValue
                self._boardState[toCol][row] = oldState          
            if row > -1:
                self._board[col][row] = EMPTY
                self._boardState[col][row] = EMPTY_CELL
    
    def _matching_jewels(self, col: int, row: int, coldelta: int, rowdelta: int) -> bool:
        '''
        Looks the cells connected to a cell at a given point and sees if there are
        three or more of the same cell in a row
        '''
        start_cell = self._board[col][row]

        if start_cell == EMPTY:
            return False
        else:
            for i in range(1, 3):
                if not self._valid_column(col + coldelta * i) \
                        or not self._valid_row(row + rowdelta * i) \
                        or self._board[col + coldelta *i][row + rowdelta * i] != start_cell:
                    return False
            #If the cells in a direction match, mark the cells as 'MATCHED_CELL'
            #Continue to match until the matching conditions aren't satisfied
            self.set_cell_state(col, row, MATCHED_CELL)
            #print("matched col{}, row{}".format(col, row))
            for i in range(1, 3):
                self.set_cell_state(col + coldelta *i, row + rowdelta * i, MATCHED_CELL)
                #print("matched col{}, row{}".format(col + coldelta *i, row + rowdelta * i))
            largestNum = _maximum(self.rows() - rowdelta, self.columns() - coldelta)
            if (largestNum >= 4):
                for i in range(3, largestNum):
                    if self._valid_column(col + coldelta * i) \
                        and self._valid_row(row + rowdelta * i) \
                        and self._board[col + coldelta *i][row + rowdelta * i] == start_cell:
                        self.set_cell_state(col + coldelta *i, row + rowdelta * i, MATCHED_CELL)
                    else:
                        break

            return True
    
    def _valid_column(self, column_number: int) -> bool:
        '''
        Checks if a column number is positive and in range of the boards columns
        '''
        return 0 <= column_number < self.columns()

    def _valid_row(self, row_number: int) -> bool:
        '''
        Checks if a row number is positive and in range of the boards rows
        '''
        return 0 <= row_number < self.rows()
    
    def _matching_begins(self, col: int, row: int) -> bool:
        '''
        Matches jewels around a jewel at the given point
        '''
        return self._matching_jewels(col, row, 0, 1) \
                or self._matching_jewels(col, row, 1, 1) \
                or self._matching_jewels(col, row, 1, 0) \
                or self._matching_jewels(col, row, 1, -1) \
                or self._matching_jewels(col, row, 0, -1) \
                or self._matching_jewels(col, row, -1, -1) \
                or self._matching_jewels(col, row, -1, 0) \
                or self._matching_jewels(col, row, -1, 1)