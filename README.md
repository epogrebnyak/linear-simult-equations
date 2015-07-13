# linear-simult-equations
Python functions to define a system of linear equations (formulas given as text strings) and solve it in NumPy.

Linear equations are of type ```A * x = B```, where A is square coef matrix,  x and B are column vectors.

We define A and B based on some input and find x using Numpy ```x = np.linalg.solve(a, b)```.

Matrix A and B can be defined as a dictionary of multipliers, start values and equations written as text strings.

[parse_additive_terms.py](parse_additive_terms.py) contains routines to split equations written as text strings to a matrix.

[string2sim.py](string2sim.py) contains full example. 
