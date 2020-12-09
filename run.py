from nnf import Var
from lib204 import Encoding
from nnf import true

# Global variables

# size of grid (4 is an 4x4 grid)
# Note: higher grid sizes above 4 take REALLY long to calculate the number of solutions for
# If attempting to use a higher grid size, try commenting out the count_solutions() call in display_solution()
size = 4

DEBUG = True

# Function to create grids for each chess pieces
def init_vars(name):
  grid = []
  for i in range(size):
    row = []
    for j in range(size):
      row.append(Var(f'{name}_{i}_{j}'))
    grid.append(row)
  return grid

# Create the variables
K = init_vars('K') #King
s = init_vars('s') #not safe square
b = init_vars('b') #enemy bishop
r = init_vars('r') #enemy rook
k = init_vars('k') #enemy king
n = init_vars('n') #enemy knight
q = init_vars('q') #enemy queen
p = init_vars('p') #enemy pawn

# Sets the propositions based on the board configuration given
def set_board(grid):
  f = true
  # For every grid position, set the proposition for the piece in that position to true
  # It also ensures that no other pieces occupy the same spot (every other piece is set to false for that spot)
  for i in range(size):
    for j in range(size):
      if (grid[i][j] == 'K'):
        f &= K[i][j]
        f &= ~b[i][j]
        f &= ~r[i][j]
        f &= ~k[i][j]
        f &= ~q[i][j]
        f &= ~n[i][j]
        f &= ~p[i][j]
      elif (grid[i][j] == 'b'):
        f &= b[i][j]
        f &= ~K[i][j]
        f &= ~r[i][j]
        f &= ~k[i][j]
        f &= ~q[i][j]
        f &= ~n[i][j]
        f &= ~p[i][j]
      elif (grid[i][j] == 'r'):
        f &= r[i][j]
        f &= ~b[i][j]
        f &= ~K[i][j]
        f &= ~k[i][j]
        f &= ~q[i][j]
        f &= ~n[i][j]
        f &= ~p[i][j]
      elif (grid[i][j] == 'k'):
        f &= k[i][j]
        f &= ~b[i][j]
        f &= ~r[i][j]
        f &= ~K[i][j]
        f &= ~q[i][j]
        f &= ~n[i][j]
        f &= ~p[i][j]
      elif (grid[i][j] == 'n'):
        f &= n[i][j]
        f &= ~b[i][j]
        f &= ~r[i][j]
        f &= ~k[i][j]
        f &= ~q[i][j]
        f &= ~K[i][j]
        f &= ~p[i][j]
      elif (grid[i][j] == 'q'):
        f &= q[i][j]
        f &= ~n[i][j]
        f &= ~b[i][j]
        f &= ~r[i][j]
        f &= ~k[i][j]
        f &= ~K[i][j]
        f &= ~p[i][j]
      elif (grid[i][j] == 'p'):
        f &= p[i][j]
        f &= ~n[i][j]
        f &= ~b[i][j]
        f &= ~r[i][j]
        f &= ~k[i][j]
        f &= ~K[i][j]
        f &= ~q[i][j]
      else:
        f &= ~K[i][j]
  return f

#Checks if the given space is in the constraint array
def is_constraint(x, y, counters):
  for i in range(len(counters)):
    if (x == counters[i]//size and y == counters[i]%size):
      return True
  return False

def add_piece_constraints(starting_grid, num_pieces, proposition, letter):
  f = true
  
  counters = []
  #set the counters
  for i in range(num_pieces):
    counters.append(0)

  #if the counter exists then start counting
  if (len(counters) >= 1):
    all_cases_found = False
    while(not all_cases_found):
      #Print the current set if in debug mode
      if (DEBUG):
        for i in range(len(counters)):
          print(counters[i]//size, counters[i]%size, end=", ")
        print()

      #Make sure that any pieces already placed on the board are ignored in the new constraints
      no_old_pieces = True
      for i in range(len(counters)):
        if (starting_grid[counters[i]//size][counters[i]%size] == letter):
          no_old_pieces = False
      
      if (no_old_pieces):
        #Add the current set as a constraint
        constraints = true
        not_constraints = true
        for i in range(len(counters)):
          constraints &= proposition[counters[i]//size][counters[i]%size]
        #Ensure that if the current set is "chosen", no other "pieces" can be placed
        for x in range(size):
          for y in range(size):
            #Make sure the "piece" isn't already in that spot, and isn't part of the current set
            if ((not starting_grid[x][y] == letter) and (not is_constraint(x,y,counters))):
              not_constraints &= ~proposition[x][y]
        f &= (constraints.negate() | not_constraints) #the true constraints imply the false ones

        #Print the added constaint if in debug mode
        if (DEBUG):
          print(constraints)

      #increment the count
      counters[-1] += 1

      #if a counter reaches the end, increase the previous by one (like a binary counter in base 'size') and
      #reset the current to one more than the previous counter (no repetition)
      #for i in range(len(k_counters)-1, -1, -1):
      for i in range(-1, -(len(counters)+1), -1):
        if (counters[0] >= size*size):
          all_cases_found = True
          if (DEBUG):
            print("All cases found.")
          break
        elif (counters[i] > size*size+i):
          counters[i-1] += 1
          #if the previous has grown too large
          if (counters[i-1] >= size*size+i):
            digt_limit = 0
            #check how far back the digits have reached their limit (consecutively)
            for j in range(i-1, -(len(counters)+1), -1):
              if (counters[j] >= size*size+j):
                digt_limit += 1
              else:
                break
            if (i-(digt_limit+1) < -len(counters)):
              all_cases_found = True
              if (DEBUG):
                print("All cases found.")
              break
            else:
              #set the current counter according to the last digit that can still be incremented
              counters[i] = counters[i-(digt_limit+1)] + (digt_limit+2)
          else:
            counters[i] = counters[i-1] + 1
  #If there are no additional pieces, restrict any additional pieces from being added
  else:
    not_constraints = true
    for x in range(size):
      for y in range(size):
        #Make sure the "piece" isn't already in that spot
        if (not starting_grid[x][y] == letter):
          not_constraints &= ~proposition[x][y]
    f &= not_constraints 
  #Return the new constraints
  return f

#Adds restrictions for the number of each piece that can be placed
def add_pieces(starting_grid, num_k, num_q, num_r, num_b, num_n, num_p):
  f = true
  f &= add_piece_constraints(starting_grid, num_k, k, "k")
  f &= add_piece_constraints(starting_grid, num_q, q, "q")
  f &= add_piece_constraints(starting_grid, num_r, r, "r")
  f &= add_piece_constraints(starting_grid, num_b, b, "b")
  f &= add_piece_constraints(starting_grid, num_n, n, "n")
  f &= add_piece_constraints(starting_grid, num_p, p, "p")
  return f

#Prints the solution
def display_solution(sol):
  # If the model is satisfied, that means we found a checkmate solution
  if T.is_satisfiable():
    print("Checkmate")
    # it may take a while to calculate the solutions
    print("solutions: " + str(T.count_solutions()))

    # Print the grids for each of our variables
    string_grid("K", sol)
    string_grid("s", sol)
    string_grid("r", sol)
    string_grid("k", sol)
    string_grid("n", sol)
    string_grid("q", sol)
    string_grid("p", sol)
  
  # Otherwise, there is no possible checkmate configuration
  else:
    print("No Checkmate Found")

# Return a string of 0s and 1s for each proposition grid
def string_grid(piece, sol):
  grid = ''
  for i in range(size):
    for j in range(size):
      grid += {True: '1', False: '0'}[sol.get(f'{piece}_{i}_{j}', False)]
    grid += '\n'
  print(f'{piece}_grid:\n' + grid)

# Helper function for creating if and only if statements
def iff(left, right):
  return (left.negate() | right) & (right.negate() | left)

# Temporary example theory
def final_theory():
    E = Encoding()
    
    # Add constraints to every square in the grid
    for i in range(size):
      for j in range(size):
        # 😂😂😂😂😂😂😂😂😂😂😂😂😂😂😂😂😂😂😂😂😂😂😂😂😂😂😂😂😂😂😂😂

        #
        # First: Create the constraint that says a square is safe if and only if there are no pieces in the way
        #

        no_danger = true

        # Check if there are no pawns that can move into this square
        if (i+1 < size):
          if (j-1 >= 0):
            no_danger &= ~p[i+1][j-1]
          if (j+1 < size):
            no_danger &= ~p[i+1][j+1]
        
        # Check if there are no bishops that can move into this square
        for x in range(1, size):
          # diagonal going up right
          if (i+x < size) and (j+x < size):
            no_danger &= ~b[i+x][j+x]
          # diagonal going down right
          if (i+x < size) and (j-x >= 0):
            no_danger &= ~b[i+x][j-x]
          # diagonal going up left
          if (i-x >= 0) and (j+x < size):
            no_danger &= ~b[i-x][j+x]
          # diagonal going down left
          if (i-x >= 0) and (j-x >= 0):
            no_danger &= ~b[i-x][j-x]
        
        # Check if there are no rooks that can move into this square
        safe_j = j
        safe_i = i
        for x in range(size):
          if (x != safe_j):
            no_danger &= ~r[i][x]
          if (x != safe_i):
            no_danger &= ~r[x][j]

        # Check if there are no queens that can move into this square
        safe_j = j
        safe_i = i
        for x in range(size):
          # Ignore the current position of the queen for diagonals
          if x != 0:
            # diagonal going up right
            if (i+x < size) and (j+x < size):
              no_danger &= ~q[i+x][j+x]
            # diagonal going down right
            if (i+x < size) and (j-x >= 0):
              no_danger &= ~q[i+x][j-x]
            # diagonal going up left
            if (i-x >= 0) and (j+x < size):
              no_danger &= ~q[i-x][j+x]
            # diagonal going down left
            if (i-x >= 0) and (j-x >= 0):
              no_danger &= ~q[i-x][j-x]
          
          # Ignore the current position of the queen rows & cols
          if (x != safe_j):
            no_danger &= ~q[i][x]
          if (x != safe_i):
            no_danger &= ~q[x][j]

        # Check if there are no knights that can move into this square
        if((i+2 < size)and(j+1 < size)): 
          no_danger &= ~n[i+2][j+1]
        if((i+2 < size)and(j-1 >= 0)): 
          no_danger &= ~n[i+2][j-1]
        if((i-2 >= 0)and(j+1 < size)): 
          no_danger &= ~n[i-2][j+1]
        if((i-2 >= 0)and(j-1 >= 0)): 
          no_danger &= ~n[i-2][j-1]
        if((i+1 < size)and(j+2 < size)): 
          no_danger &= ~n[i+1][j+2]
        if((i-1 >= 0)and(j+2 < size)): 
          no_danger &= ~n[i-1][j+2]
        if((i+1 < size)and(j-2 >= 0)):      
          no_danger &= ~n[i+1][j-2]
        if((i-1 >= 0)and(j-2 >= 0)): 
          no_danger &= ~n[i-1][j-2]

        # Check if there are no enemy kings that can move into this square
        if (i-1 >= 0 and j-1 >= 0):
          no_danger &= ~k[i-1][j-1]
        if (i-1 >= 0):
          no_danger &= ~k[i-1][j]
        if (i-1 >= 0 and j+1 < size):
          no_danger &= ~k[i-1][j+1]
        if (i+1 < size and j-1 >= 0):
          no_danger &= ~k[i+1][j-1]
        if (i+1 < size):
          no_danger &= ~k[i+1][j]
        if (i+1 < size and j+1 < size):
          no_danger &= ~k[i+1][j+1]
        if (j-1 >= 0):
          no_danger &= ~k[i][j-1]
        if (j+1 < size):
          no_danger &= ~k[i][j+1]

        # Finally add the constraint that says a square is safe if and only if there are no pieces can move into it
        E.add_constraint(iff(no_danger, ~s[i][j]))

        #
        # Next: Add constraints that will determine when a square is not safe
        #

        # Check if a rook can move into the square
        not_safe = true
        safe_j = j
        safe_i = i
        for x in range(size):
          if (x != safe_j):
            not_safe &= s[i][x]
          if (x != safe_i):
            not_safe &= s[x][j]
        E.add_constraint(~r[i][j] | not_safe)

        # Check if a bishop can move into the square
        not_safe = true
        for x in range(1, size):
          # diagonal going up right
          if (i+x < size) and (j+x < size):
            not_safe &= s[i+x][j+x]
          # diagonal going down right
          if (i+x < size) and (j-x >= 0):
            not_safe &= s[i+x][j-x]
          # diagonal going up left
          if (i-x >= 0) and (j+x < size):
            not_safe &= s[i-x][j+x]
          # diagonal going down left
          if (i-x >= 0) and (j-x >= 0):
            not_safe &= s[i-x][j-x]
        E.add_constraint(~b[i][j] | not_safe)

        # Check if a queen can move into the square
        not_safe = true
        safe_j = j
        safe_i = i
        for x in range(size):
          # Ignore the current position of the queen for diagonals
          if x != 0:
            # diagonal going up right
            if (i+x < size) and (j+x < size):
              not_safe &= s[i+x][j+x]
            # diagonal going down right
            if (i+x < size) and (j-x >= 0):
              not_safe &= s[i+x][j-x]
            # diagonal going up left
            if (i-x >= 0) and (j+x < size):
              not_safe &= s[i-x][j+x]
            # diagonal going down left
            if (i-x >= 0) and (j-x >= 0):
              not_safe &= s[i-x][j-x]
          
          # Ignore the current position of the queen
          if (x != safe_j):
            not_safe &= s[i][x]
          if (x != safe_i):
            not_safe &= s[x][j]

        E.add_constraint(~q[i][j] | not_safe)

        # Check if a pawn can move into the square
        not_safe = true
        if (i-1 >= 0):
          if (j-1 >= 0):
            not_safe &= s[i-1][j-1]
          if (j+1 < size):
            not_safe &= s[i-1][j+1]
        E.add_constraint(~p[i][j] | not_safe)

        # Check if an enemy king can move into the square
        not_safe = true
        if (i-1 >= 0 and j-1 >= 0):
          not_safe &= s[i-1][j-1]
        if (i-1 >= 0):
          not_safe &= s[i-1][j]
        if (i-1 >= 0 and j+1 < size):
          not_safe &= s[i-1][j+1]
        if (i+1 < size and j-1 >= 0):
          not_safe &= s[i+1][j-1]
        if (i+1 < size):
          not_safe &= s[i+1][j]
        if (i+1 < size and j+1 < size):
          not_safe &= s[i+1][j+1]
        if (j-1 >= 0):
          not_safe &= s[i][j-1]
        if (j+1 < size):
          not_safe &= s[i][j+1]
        E.add_constraint(~k[i][j] | not_safe)

        # Check if an knight can move into the square
        not_safe = true
        if((i+2 < size)and(j+1 < size)): 
          not_safe &= s[i+2][j+1]
        if((i+2 < size)and(j-1 >= 0)): 
          not_safe &= s[i+2][j-1]
        if((i-2 >= 0)and(j+1 < size)): 
          not_safe &= s[i-2][j+1]
        if((i-2 >= 0)and(j-1 >= 0)): 
          not_safe &= s[i-2][j-1]
        if((i+1 < size)and(j+2 < size)): 
          not_safe &= s[i+1][j+2]
        if((i-1 >= 0)and(j+2 < size)): 
          not_safe &= s[i-1][j+2]
        if((i+1 < size)and(j-2 >= 0)):      
          not_safe &= s[i+1][j-2]
        if((i-1 >= 0)and(j-2 >= 0)): 
          not_safe &= s[i-1][j-2]
        E.add_constraint(~n[i][j] | not_safe)

        #
        # Next: Check if the squares around the friendly king are not safe
        # Our constraint says that the friendly king must be in checkmate
        #

        around_king = true
        around_king &= s[i][j]

        if (i-1 >= 0 and j-1 >= 0):
          around_king &= s[i-1][j-1]
        if (i-1 >= 0):
          around_king &= s[i-1][j]
        if (i-1 >= 0 and j+1 < size):
          around_king &= s[i-1][j+1]
        if (i+1 < size and j-1 >= 0):
          around_king &= s[i+1][j-1]
        if (i+1 < size):
          around_king &= s[i+1][j]
        if (i+1 < size and j+1 < size):
          around_king &= s[i+1][j+1]
        if (j-1 >= 0):
          around_king &= s[i][j-1]
        if (j+1 < size):
          around_king &= s[i][j+1]
        E.add_constraint(~K[i][j] | around_king)
    
    #Return theory
    return E

# Start of file when run
if __name__ == "__main__":
    # Create a board configuration
    starting_grid = [
      ['k','-','-','-'],
      ['-','r','-','-'],
      ['-','-','-','-'],
      ['K','-','-','-']
    ]

    #list how many excess pieces there are that can be placed anywhere on the board
    #(so long as the spot isn't already taken)
    #Note: These counts do not include pieces already on the board (in the starting_grid)
    num_k = 1 #number of enemy kings
    num_q = 0 #number of enemy queens
    num_r = 0 #number of enemy rooks
    num_b = 0 #number of enemy bishops
    num_n = 0 #number of enemy knights
    num_p = 0 #number of enemy pawns
    
    # Configure the constraints given the initial board configuration (starting_grid)
    props = set_board(starting_grid)

    # Configure the constraints that allow the model to place pieces the given pieces on the board
    props &= add_pieces(starting_grid, num_k, num_q, num_r, num_b, num_n, num_p)
    
    T = final_theory()
    T.add_constraint(props)

    sol = T.solve()
    display_solution(sol)
