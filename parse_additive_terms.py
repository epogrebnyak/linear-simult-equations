
multipliers = {		
	'liq_share':  0.2	
,	'credit_ir ': 0.1	
,	'deposit_ir': 0.05	
}	
		
equations =  [		
	'ta = credit + liq'	
,	'liq = credit * liq_share'	
,	'profit = credit * credit_ir - deposit * deposit_ir'	
,	'fgap = ta - capital - profit - deposit'	
]	

# from equations and values we must get follwoing:
free_term = 'b'

structured_equations = [   
    {'ta': -1,     free_term:0, 'credit': 1, 'liq':1}
,	{'liq': -1,    free_term:0, 'credit': 0.2}	
,	{'profit': -1, free_term:0, 'credit': 0.1, 'deposit':-0.05}	
,	{'fgap':-1,    free_term:0, 'ta':1, 'capital':-1, 'profit':-1, 'deposit': -1}
]

def split_equation_string_to_dictionary(equation, multipliers, free_term = 'b'):
    """
    Must return a dictionary as in 'structured_equations'. Rules:
    
    Easy ones
    1. left-hand side variable ('ta', 'liq') is assigned -1
    2. free_term always 0
    
    The gist of it 
    3. all right-hand additive terms must be split into sign, variable, and multiplier and evaluated 
        Example: for "- deposit * deposit_ir"
                    sign is -1
                    variable is 'deposit'
                    multiplier is '' 
                    and result of evaluation is -0.05
                    -0.05  is written to resulting dictionary. 
    """
    pass
    

flag = [split_equation_string_to_dictionary(eq, multipliers) for eq in equations] == structured_equations
print (flag)
