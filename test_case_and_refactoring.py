multipliers = {
	'liq_share':  0.2
,	'credit_ir': 0.1
,	'deposit_ir': 0.05
}


def split_multiplicative_term(sign,multiplicativeterm,multipliers):
    """ parses a multiplicative term of form "A * B" to a tuple

    identifies which of A or B is a multiplier, then returns tuple
    where first element is the variable name and the second element
    is the numeric value of multiplier times sign
    """
    #split the multiplicative term by "*" operator
    mt = multiplicativeterm.split("*")

    #check if first element is in multipliers
    if mt[0].strip() in multipliers:
        return (mt[1].strip(),sign*multipliers[mt[0].strip()])
    else:
        #otherwise the second element is the multiplier
        return (mt[0].strip(),sign*multipliers[mt[1].strip()])



equation = 'profit = credit * credit_ir - deposit_ir * deposit'

free_term = 'b'

eq_dict = {free_term:0}

# Must note in docstring: parsing only terms ( + - a * b )


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

print (eq_dict)
