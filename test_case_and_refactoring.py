multipliers = {
	'liq_share':  0.2
,	'credit_ir': 0.1
,	'deposit_ir': 0.05
}

# this works well:
# equation = 'profit = credit * credit_ir - deposit * deposit_ir'

# todo: must work on this: 
equation = 'profit = credit * credit_ir - deposit_ir * deposit'

free_term = 'b'

eq_dict = {free_term:0}

# Must note in docstring: parsing only terms ( + - a * b ) 

## rhs = equation.split("=")

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
        k = j[0].split("*")

        # todo:        
        # error: here you are not guaranteed that first
        #        term is always a variable and second term is always
        #        a multiplier, can be other way around,
        #        this code will fail on  'credit_ir * credit' 
        #        must use list of variables and list of multipliers to
        #        perform proper substitution 
        eq_dict[k[0].strip()] = -1*multipliers[k[1].strip()]

        # todo: must obtain 'varnames' as left-hand side parts of all equations
        # todo: create split_multiplicative_term()
        # key, val = split_multiplicative_term(-1, j[0], multipliers, varnames)
        # eq_dict[key] = val
    else:
        k = j[0].strip()
        if k != "":
            eq_dict[k] = -1

    # other ones j[1+] are positive
    if len(j)>1:
        for k in j[1:]:
           if "*" in k:
                z = k.split("*")
                # same error here: 'credit_ir * credit' will fail.
                eq_dict[z[0].strip()] = multipliers[z[1].strip()]
                # todo:
                # key, val = split_multiplicative_term(1, k, multipliers, varnames)
                # eq_dict[key] = val                
           else:
                eq_dict[k.strip()] = 1
                
print (eq_dict)
