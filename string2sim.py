from parse_additive_terms import split_equation_string_to_dictionary
from pprint import pprint
import numpy  as np
import pandas as pd

# http://pandas.pydata.org/pandas-docs/stable/dsintro.html#from-a-list-of-dicts

vars = ['ta'	, 'liq'	, 'profit'	, 'fgap'	, 'capital'	, 'credit'	, 'deposit'	]

multipliers = {		
	'liq_share':  20/100	
,	'credit_ir': 10/100	
,	'deposit_ir': 5/100	
}		
		
equations =  [		
	'ta = credit + liq'	
,	'liq = credit * liq_share'	
,	'profit = credit * credit_ir - deposit * deposit_ir'	
,	'fgap = ta - capital - profit - deposit'	
]	

values = {		
	'capital': 100	
,	'credit': 500	
,	'deposit': 300	
}		

# risk of a duplicate
FREE_TERM= 'b'

# from equations and values we must get follwoing:
structured_equations = [   
    {'ta': -1,     FREE_TERM:0, 'credit': 1, 'liq':1}
,	{'liq': -1,    FREE_TERM:0, 'credit': 20/100}	
,	{'profit': -1, FREE_TERM:0, 'credit': 10/100, 'deposit':-5/100}	
,	{'fgap':-1,    FREE_TERM:0, 'ta':1, 'capital':-1, 'profit':-1, 'deposit': -1}
]

structured_values = [		
	 {'capital':1, FREE_TERM:100}
   , { 'credit':1, FREE_TERM:500}
   , {'deposit':1, FREE_TERM:300}	
]

def make_full_dict_list(multipliers, equations, values, free_term = FREE_TERM):
    """
    Makes a list of dictionaries, each dictionary containing matrix elements 
    (key is variable name, val is matrix element). Each dictionary is matrix row.
    """
    eq_dict_list  = [split_equation_string_to_dictionary(eq, multipliers) for eq in equations]
    val_dict_list = [ {key:1, free_term :val} for key, val in values.items()]
    eq_dict_list.extend(val_dict_list)
    return eq_dict_list
    
def diagnose(a):
        print()
        print("Number of equations: ", a.shape[0])
        print("Number of variables: ", len(a.columns) - 1)
        print("Rank: ",                np.linalg.matrix_rank(a))         
    
def check_rank(a):
    # omit free term from 'num_vars' count 
    num_vars = len(a.columns) - 1
    
    rank = np.linalg.matrix_rank(a)
    diagnose(a)
    if rank != num_vars:                  
         raise ValueError("Matix does not have full rank")
    else:
         pass

    
def get_axb_parameters(full_equation_set, free_term  = FREE_TERM):
    """
    Returns A, B and column names in A as defined by 'full_equation_set'
    """
    a = pd.DataFrame(full_equation_set)
    
    # kill NaN, put 0 instead
    index = np.isnan(a)
    a[index] = 0
    
    check_rank(a)
    
    b = a[free_term]    
    a = a.drop(free_term, 1)    
    names = a.columns.values    
    return a, b, names 

def get_x_solution(full_equation_set, verbose=False):
    """
    Solves 'full_equation_set' for x.
    """
    a, b, names = get_axb_parameters(full_equation_set)
    
    # solves AX=B for X
    x = np.linalg.solve(a, b)
    
    # make Dataframe out of 'x'
    x = pd.DataFrame(x)
    x.index = list(names)
    x.columns = ['x']
    
    if verbose is True:
       pprint(x)
       
    return x
    
def print_x_solution(x, names):
    # 
    for name, value in zip(names, x):
        print(name, "=", value)

def solve_lin_system(multipliers, equations, values):
    """
    Returns X that solves linear system.  Main entry point.
    See above lines 10-27 for arg types.
    """    
    full_equation_set =  make_full_dict_list(multipliers, equations, values)
    return get_x_solution(full_equation_set)    
    

if __name__ == "__main__":
    full_equation_set =  make_full_dict_list(multipliers, equations, values)
    pprint(full_equation_set)    
    
    x = get_x_solution(full_equation_set)        
    
    for lst in (['liq', 'credit', 'ta'],
                ['capital', 'profit', 'deposit', 'fgap', 'ta']):
        pprint( x.loc[lst,:]) 
