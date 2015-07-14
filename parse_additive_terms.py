"""
   Functions and test case to convert text strings to
   DataFrame-friendly dictionary.
"""
import re


multipliers = {
	'liq_share':  0.2
,	'credit_ir': 0.1
,	'deposit_ir': 0.05
}

equations =  [
	'ta = credit + liq'
,	'liq = credit * liq_share'
# note different order of var and multiplier
,	'profit = credit * credit_ir - deposit_ir * deposit'
,	'fgap = ta - capital - profit - deposit'
]


# TODO: must change parsing so that 'new_equations' can be parsed


# can be parsed to
# new_structured_equations = [
#    {free_term_var:-1, 'period_lag': 1, 'period': -1}
#,	{'avg_credit': -1, free_term_var:0, 'credit': 0.5, 'credit':0.5}]
#

# This is hopefully done through: 1 and 2 below

# 1. must change split_multiplicative_term(sign, multiplicative_term, multipliers, ...)
# to accept 'avg_credit = 0.5 * credit + 0.5 * credit_lag'
# 'avg_credit = 0.5 * credit + 0.5 * credit_lag'
# split_multiplicative_term(1, '0.5 * credit_lag', ...) must
# return  'credit_lag', 0.5

# 2. split_multiplicative_term(1, '1', ...) must return
# return free_term_var, -1


# , ...) denotes extra arguments that split_multiplicative_term() might need.
# I think that should be a proper list of variables

# Overall there can be differetn strategies for split_multiplicative_term:
# Implemented:
#    pass a list of muiltipliers, everything else near * sign is a variable name
# Possible:
#    pass a list of muiltipliers, apss a list of variable name, try if everything else is an int/float
#
# please comment/discuss





# duplicate
free_term_var = 'b'

# from equations and values we must get follwoing:

structured_equations = [
    {'ta': -1,     free_term_var:0, 'credit': 1, 'liq':1}
,	{'liq': -1,    free_term_var:0, 'credit': 0.2}
,	{'profit': -1, free_term_var:0, 'credit': 0.1, 'deposit':-0.05}
,	{'fgap':-1,    free_term_var:0, 'ta':1, 'capital':-1, 'profit':-1, 'deposit': -1}
]

new_equations = [
'period = period_lag + 1',
'avg_credit = 0.5 * credit + 0.5 * credit_lag']

new_structured_equations = [
    {free_term_var:-1, 'period_lag': 1, 'period': -1}
,	{'avg_credit': -1, free_term_var:0, 'credit': 0.5, 'credit_lag':0.5}]


def is_number(s):
    '''Test if str "s" is a number'''
    try:
        float(s)
        return True
    except ValueError:
        return False

def assign_type(s, multipliers):
    '''Assign type for variable between number, multiplier, variable'''
    if is_number(s):
        return 'constant'
    elif s in multipliers:
        return 'multiplier'
    else:
        return 'variable'


def split_multiplicative_term(sign, multiplicative_term, multipliers):
    """ parses a multiplicative term of form "A * B" to a tuple
    identifies which of A or B is a multiplier or a constant, then returns tuple
    where first element is the variable name and the second element
    is the numeric value of multiplier (or the constant) times 'sign'. multiplier is detected
    if its variable name is in 'multipliers'.

    Special case is when multiplicative_term is '1', in this case
    we return the free_term_var with value sign * 1
    """
    # Special case: 1
    if multiplicative_term.strip() == '1':
        return free_term_var, -1

    # Split the multiplicative term by "*" operator
    o1, o2 = [o.strip() for o  in multiplicative_term.split("*")]

    o1_t = assign_type(o1, multipliers)
    o2_t = assign_type(o2, multipliers)

    # Assign each variable to its type: variable, constant or multiplier
    term = { o1_t : o1,
             o2_t : o2 }

    # Assert input is well-formed
    if 'variable' not in term or len(term) == 1:
        raise ValueError('Variable not in term: %s' % multiplicative_term)

    # Cast multiplier or constants
    if 'multiplier' in term:
        term['value'] = multipliers[term['multiplier']]
    if 'constant' in term:
        term['value'] = float(term['constant'])

    return term['variable'], sign * term['value']

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

    # Split string into tokens, terms and operations
    tokens = [i.strip() for i in re.split(r'([+-])', rhs) if i]
    sign = 1 # Default sign
    while tokens:
        token = tokens.pop(0)

        if token == '+':
            sign = 1
        elif token == '-':
            sign = -1
        elif token == '1':
            key, val = split_multiplicative_term(sign, token, multipliers)
            eq_dict[key] = val
            sign = 1
        elif '*' in token:
            key, val = split_multiplicative_term(sign, token, multipliers)
            print(key, val)
            eq_dict[key] = val
            sign = 1
        else:
            eq_dict[token] = sign
            sign = 1

    return eq_dict

    # if rhs[0] not in "+-":
    #     rhs = "+"+rhs
    #
    # # split everything to check for minus
    # for i in rhs.split("-"):
    #
    #     # split the rest of the terms for plus
    #     j = i.split("+")
    #
    #     # j[0] is a negative term
    #     if "*" in j[0] or j[0].strip() == '1':
    #         # has multiplier
    #         key, val = split_multiplicative_term(-1, j[0], multipliers)
    #         eq_dict[key] = val
    #     else:
    #         # no multiplier
    #         k = j[0].strip()
    #         if k != "":
    #             eq_dict[k] = -1
    #
    #     # other ones j[1+] are positive
    #     if len(j)>1:
    #         for k in j[1:]:
    #            if "*" in k or k.strip() == '1':
    #                 # has multiplier
    #                 key, val = split_multiplicative_term(1, k, multipliers)
    #                 eq_dict[key] = val
    #            else:
    #                 # no multiplier
    #                 eq_dict[k.strip()] = 1
    # return eq_dict

if __name__ == "__main__":
  from pprint import pprint
  flag = [split_equation_string_to_dictionary(eq, multipliers) for eq in equations] == structured_equations
  pprint([split_equation_string_to_dictionary(eq, multipliers) for eq in equations])
  pprint(structured_equations)
  print('Old equations', flag)
  flag = [split_equation_string_to_dictionary(eq, multipliers) for eq in new_equations] == new_structured_equations
  pprint([split_equation_string_to_dictionary(eq, multipliers) for eq in new_equations])
  pprint(new_structured_equations)
  print('New equations', flag)
