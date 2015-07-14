#from string2sim import solve_lin_system
import pandas as pd
import numpy as np
from pprint import pprint

# TODO 1:
# read csv sheet input.tab using pandas
#     strip whitespace in second column
#     comma is decimal sign here, 1,15 is 1.15
#     separator is  \t tab

# Dirty parse of the input file
csvfile = pd.read_csv('input.tab', sep='\t', skip_blank_lines=True, decimal=',')
# Remove useless rows
csvfile = csvfile[csvfile.ix[:, 0].notnull()]
# Strip whitespace from second column
csvfile.ix[:, 1] = csvfile.ix[:, 1].str.strip()

# TODO 2:
# produce 'mutipliers', 'equations', 'values 'in data structures similar to ones below
# use period 0 data

def get_csv_block_as_dict(csvfile, pivot_label, val_col = 2, key_col = 1):
    directives = csvfile[csvfile.ix[:, 0] == pivot_label]
    value_dict = dict(directives.ix[:,(key_col,val_col)].values)
    return  value_dict

def get_multipliers_as_dict(csvfile):
    return get_csv_block_as_dict(csvfile, 'multiplier')

def get_values_as_dict(csvfile, period):
    return get_csv_block_as_dict(csvfile, 'value', val_col = 2 + period)

def get_equations_as_list(csvfile):
    return list(get_csv_block_as_dict(csvfile, 'equation').keys())

multipliers = get_multipliers_as_dict(csvfile)
values      = get_values_as_dict(csvfile, 0)
equations   = get_equations_as_list(csvfile)

print ('\nMultipliers:')
pprint(multipliers)
print ('\nValues:')
pprint(values)
print ('\nEquations:')
pprint(equations)

# multipliers = {
	# 'liq_share':  .20
# ,	'credit_ir': .10
# ,	'deposit_ir': .05
# }

# equations =  [
	# 'ta = credit + liq'
# ,	'liq = credit * liq_share'
# ,	'profit = credit * credit_ir - deposit * deposit_ir'
# ,	'fgap = ta - capital - profit - deposit'
# ]

# values = {
	# 'capital': 100
# ,	'credit': 500
# ,	'deposit': 300
# }

from string2sim import make_full_dict_list, get_x_solution
full_equation_set =  make_full_dict_list(multipliers, equations, values)
print ('Equation set')
pprint(full_equation_set)
print ('--')
x = get_x_solution(full_equation_set)
print (x)

dict1 = {	'period'	:	1
,	'credit'	:	115
,	'liq'	:	23
,	'capital'	:	30
,	'deposit'	:	99
,	'profit'	:	7.23
,	'fgap'	:	1.77
,	'one'	:	1	}

# CHECK 1:
# change dict1 type to nparray
# compare dict_1 to x

variables, vals = zip(*dict1.items())
data1 = pd.DataFrame(np.array(vals),
                     index=variables,
                     columns=['x'])


# Our result contains more variables than
# what we have in x, do we need to match them?

# WARNING we need to add one, because it is not present
x.ix['one'] = 1.000

print(x.ix[data1.index])
print(data1)
# To actually assert their equality use np.allclose()
print('Matching values?', np.allclose(data1, x.ix[data1.index]))

#TODO 3:
# write back 'x' to corresponding 'value' rows in period 1 in csv sheet input.tab using pandas

def write_tabfile(values0, values1, equations, multipliers, tabfile):
    '''Write result to csv file.

    Parameters:
    values0: dictionary of variable values at lag 0
    values1: dictionary of variable values at lag 1
    equations: list of strings representing relationships
    multipliers: dicionary of multipliers
    tabfile: output filename
    '''
    fields = []
    fields.append([None, 'Values', None, None])
    [fields.append(['value', name, values0[name], values1[name.replace('_lag', '')]])
                      for name in values0]

    fields.append([None, None, None, None])
    fields.append([None, 'Multipliers:', None, None])
    [fields.append(['multiplier', name, value, None])
                       for name, value in multipliers.items()]

    fields.append([None, None, None, None])
    fields.append([None, 'Equations:', None, None])
    [fields.append(['equation', name, None, None])
                    for name in equations]

    df = pd.DataFrame(fields)
    df.to_csv(tabfile, sep='\t', decimal=',', header=False, index=False)

result_fields = [k.replace('_lag', '') for k in values]
write_tabfile(values, x.ix[result_fields].to_dict()['x'], equations, multipliers, 'output.tab')
