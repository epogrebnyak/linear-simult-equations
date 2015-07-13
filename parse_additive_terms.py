"""
   Functions and test case to convert text strings to 
   DataFrame-friendly dictionary.
"""
multipliers = {
	'liq_share':  0.2
,	'credit_ir': 0.1
,	'deposit_ir': 0.05
}

equations =  [
	'ta = credit + liq'
,	'liq = credit * liq_share'
# note different order of var and multiplier
,	'profit = credit * credit_ir - deposit * deposit_ir ' 
,	'fgap = ta - capital - profit - deposit'
]

# duplicate
free_term_var = 'b'

# from equations and values we must get follwoing:

structured_equations = [
    {'ta': -1,     free_term_var:0, 'credit': 1, 'liq':1}
,	{'liq': -1,    free_term_var:0, 'credit': 0.2}
,	{'profit': -1, free_term_var:0, 'credit': 0.1, 'deposit':-0.05}
,	{'fgap':-1,    free_term_var:0, 'ta':1, 'capital':-1, 'profit':-1, 'deposit': -1}
]

def split_multiplicative_term(sign, multiplicative_term, multipliers):
    """ parses a multiplicative term of form "A * B" to a tuple
    identifies which of A or B is a multiplier, then returns tuple
    where first element is the variable name and the second element
    is the numeric value of multiplier times 'sign'. multiplier is detected 
    if its variable name is in 'multipliers'
    """
    #split the multiplicative term by "*" operator
    mt = multiplicative_term.split("*")

    #check if first element is in multipliers
    if mt[0].strip() in multipliers:        
        general_var = mt[1].strip()        
        multiplier_var_name = mt[0].strip()
        # return (mt[1].strip(),sign * multipliers[mt[0].strip()])
    else:
        #otherwise the second element is the multiplier
        general_var = mt[0].strip()        
        multiplier_var_name = mt[1].strip()
        # return (mt[0].strip(),sign * multipliers[mt[1].strip()])
    return general_var, sign * multipliers[multiplier_var_name]

def split_equation_string_to_dictionary(equation, multipliers, free_term = free_term_var):
    """
    Must return a dictionary as in 'structured_equations'.
    Only parses combinations of "+ - *", variable names, members of multipliers dictionary
    Rules:
    Easy ones:
    1. left-hand side variable ('ta', 'liq') is assigned -1
    2. free_term always 0
    The gist of it:
    3. all right-hand additive terms must be split into sign, variable, and multiplier and evaluated
        Example: for "- deposit * deposit_ir"
                    sign is -1
                    variable is 'deposit'
                    multiplier is 'deposit_ir'
                    and result of evaluation is -0.05
                    -0.05  is written to resulting dictionary.
    """
    eq_dict = {free_term:0}

    # assign -1 to left-hand-side variable
    lhs = equation.split("=")[0].strip()
    eq_dict[lhs] = -1

    # decompose right-hand-side of equation
    rhs = equation.split("=")[1].strip()

    # add a sign before first term
    if rhs[0] not in "+-":
        rhs = "+"+rhs

    # split everything to check for minus
    for i in rhs.split("-"):

        # split the rest of the terms for plus
        j = i.split("+")

        # j[0] is a negative term
        if "*" in j[0]:
            # has multiplier
            key, val = split_multiplicative_term(-1, j[0], multipliers)
            eq_dict[key] = val
        else:
            # no multiplier
            k = j[0].strip()
            if k != "":
                eq_dict[k] = -1

        # other ones j[1+] are positive
        if len(j)>1:
            for k in j[1:]:
               if "*" in k:
                    # has multiplier
                    key, val = split_multiplicative_term(1, k, multipliers)
                    eq_dict[key] = val
               else:
                    # no multiplier
                    eq_dict[k.strip()] = 1
    return eq_dict

if __name__ == "__main__":
  flag = [split_equation_string_to_dictionary(eq, multipliers) for eq in equations] == structured_equations
  print (flag)
