from nnf import Var
from lib204 import Encoding
from nnf import true, false

#Global variables
size = 5 #size of grid (8 is an 8x8 grid)

# Function to create grids for each chess pieces
# If disp is true, it will return an array of strings
# If disp is false, it will return an array of Var objs
def init_vars(name, disp):
  grid = []
  for i in range(size):
    row = []
    for j in range(size):
      if (disp):
        row.append(f'{name}_{i}_{j}')
      else:
        row.append(Var(f'{name}_{i}_{j}'))
    grid.append(row)
  return grid

# Create the variables
checkmate = Var("checkmate")
K = init_vars('K', False) #King
s = init_vars('s', False) #not safe square
b = init_vars('b', False) #enemy bishop
r = init_vars('r', False) #enemy rook
k = init_vars('k', False) #enemy king
n = init_vars('n', False) #enemy knight
q = init_vars('q', False) #enemy queen
p = init_vars('p', False) #enemy pawn
K_d = init_vars('K', True) #_d is the display copy of each array
s_d = init_vars('s', True) 
b_d = init_vars('b', True) 
r_d = init_vars('r', True) 
k_d = init_vars('k', True) 
n_d = init_vars('n', True) 
q_d = init_vars('q', True) 
p_d = init_vars('p', True)

#
# Build an example full theory for your setting and return it.
#
#  There should be at least 10 variables, and a sufficiently large formula to describe it (>50 operators).
#  This restriction is fairly minimal, and if there is any concern, reach out to the teaching staff to clarify
#  what the expectations are.

# Sets the propositions based on the dict given
def set_board(grid):
  f = true
  #For every position recorded, set the proposition for the piece in that 
  #position to true
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
        f &= ~n[i][j]
        f &= ~b[i][j]
        f &= ~r[i][j]
        f &= ~k[i][j]
        f &= ~q[i][j]
        f &= ~K[i][j]
        f &= ~p[i][j]
  return f

#Prints the solution
def display_solution(sol):
  if T.is_satisfiable():
    print("Checkmate")
    # it may take a while to calculate the solutions
    print("solutions: " + str(T.count_solutions()))
    K_grid = string_grid(K_d, sol)
    s_grid = string_grid(s_d, sol)
    r_grid = string_grid(r_d, sol)
    k_grid = string_grid(k_d, sol)
    n_grid = string_grid(n_d, sol)
    q_grid = string_grid(q_d, sol)
    p_grid = string_grid(p_d, sol)
    
    print("K_grid:\n"+ K_grid)
    print("s_grid:\n"+ s_grid)
    print("r_grid:\n"+ r_grid)
    print("k_grid:\n"+ k_grid)
    print("n_grid:\n"+ n_grid)
    print("q_grid:\n"+ q_grid)
    print("p_grid:\n"+ p_grid)
  else:
    print("No Checkmate")

# Return a string of 0s and 1s for each proposition grid
def string_grid(prop_grid, sol):
  grid = ''
  for i in range(size):
    for j in range(size):
      grid += {True: '1', False: '0'}[sol.get(prop_grid[i][j], False)]
    grid += '\n'
  return grid

def iff(left, right):
  return (left.negate() | right) & (right.negate() | left)

# Temporary example theory
def example_theory():
    E = Encoding()

    # Add constraints
    # rook constraints
    for i in range(size):
      for j in range(size):
        not_safe = true

        # constraint that says this square is safe if and only if there are no pieces in the way
        # this is horrible
        no_danger = true

        # 😂😂😂😂😂😂😂😂😂😂😂😂😂😂😂😂😂😂😂😂😂😂😂😂😂😂😂😂😂😂😂😂
        # check if pawn is not in the way
        if (i+1 < size):
          if (j-1 >= 0):
            no_danger &= ~p[i+1][j-1]
          if (j+1 < size):
            no_danger &= ~p[i+1][j+1]
        
        # check if bishop is not in the way
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
        
        # check if rook is not in the way
        safe_j = j
        safe_i = i
        for x in range(size):
          if (x != safe_j):
            no_danger &= ~r[i][x]
          if (x != safe_i):
            no_danger &= ~r[x][j]

        # check if queen is not in the way
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

        # check if knight is not in the way
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

        # check if enemy king is not in the way
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

        E.add_constraint(iff(no_danger, ~s[i][j]))

        # rook constraints
        safe_j = j
        safe_i = i
        for x in range(size):
          if (x != safe_j):
            not_safe &= s[i][x]
          if (x != safe_i):
            not_safe &= s[x][j]
        E.add_constraint(~r[i][j] | not_safe)

      #bishop constraints
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

      # queen constraints
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
          
          # Ignore the current position of the queen rows & cols
          if (x != safe_j):
            not_safe &= s[i][x]
          if (x != safe_i):
            not_safe &= s[x][j]

        E.add_constraint(~q[i][j] | not_safe)

      # pawn constraints
        not_safe = true
        # Make sure the attack spots are in bounds
        if (i-1 >= 0):
          if (j-1 >= 0):
            not_safe &= s[i-1][j-1]
          if (j+1 < size):
            not_safe &= s[i-1][j+1]
        E.add_constraint(~p[i][j] | not_safe)

      # enemy king constraints
        not_safe = true
        # check if corners are in bounds
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

      #knight constraints
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

      # check spaces around king for checkmate
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

    """
    T = example_theory()

    print("\nSatisfiable: %s" % T.is_satisfiable())
    print("# Solutions: %d" % T.count_solutions())
    print("   Solution: %s" % T.solve())

    print("\nVariable likelihoods:")
    for v,vn in zip([a,b,c,x,y,z], 'abcxyz'):
        print(" %s: %.2f" % (vn, T.likelihood(v)))
    print()
    """

    starting_grid = [
      ['-','-','K','-','-'],
      ['-','-','p','-','-'],
      ['-','-','q','-','-'],
      ['-','-','-','-','-'],
      ['-','-','-','-','-']
    ]
    
    props = set_board(starting_grid)
    print(props)
    
    T = example_theory()
    T.add_constraint(props)

    sol = T.solve()
    display_solution(sol)
