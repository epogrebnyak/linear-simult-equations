# linear-simult-equations
Python functions to define a system of linear equations (formulas given as text strings) and solve it in NumPy.

Linear equations are of type ```A * x = B```, where A is square coef matrix,  x and B are column vectors.

We define A and B based on some input and find x using Numpy ```x = np.linalg.solve(a, b)```.

Matrix A and B can be defined as a dictionary of multipliers, start values and equations written as text strings.

[parse_additive_terms.py](parse_additive_terms.py) contains routines to split equations written as text strings to a matrix.

[string2sim.py](string2sim.py) contains full example. 

##Why bother?

Intent of end-use: in bank bakance sheet projections - parse simple equations which relate current period balance sheet items to previous period balance sheet items, control parameters and text-string equations.

Example:
```
Start values:
credit_0   = 100
liq_0      = 20
capital_0  = 30
deposit_0  = 90
profit_0   = 0
fgap       = 0 

Multipliers:
credit_rog    = 1.15
deposit_rog   = 1.1
credit_ir     = 1.12
deposit_ir    = 1.08
liq_to_credit = 0.2
half = 0.5

Equations:
credit_1 = credit_0 * credit_rog 
deposit_1 = deposit_0 * deposit_rog 
liq_1    = credit_1 * liq_to_credit
ta_1     = credit_1 + liq_1
# avg_credit = 0.5 * credit_1 + 0.5 * credit_0
# must use a 'half' constant below due to simplistic parser
avg_credit = half * credit_1 + half * credit_0  
avg_deposit = half * deposit_1 + half * deposit_0  
profit_1 = avg_credit * credit_ir - avg_deposit * deposit_ir
fgap_1 = ta_1 - capital_1 - profit_1 - deposit_1
```
