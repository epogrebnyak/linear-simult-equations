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

# # multiplier_directives = csvfile[csvfile.ix[:, 0] == 'multiplier']
# # multipliers = dict(multiplier_directives.ix[:,1:3].values)
# # print ('Multipliers')
# # pprint(multipliers)
# # print ('---')
# multipliers = {
	# 'liq_share':  .20
# ,	'credit_ir': .10
# ,	'deposit_ir': .05
# }

# # equation_directives = csvfile[csvfile.ix[:, 0] == 'equation']
# # equations = equation_directives.ix[:,1].values.tolist()
# # print ('Equations')
# # pprint(equations)
# # print ('--')
# equations =  [
	# 'ta = credit + liq'
# ,	'liq = credit * liq_share'
# ,	'profit = credit * credit_ir - deposit * deposit_ir'
# ,	'fgap = ta - capital - profit - deposit'
# ]

# # value_directives = csvfile[csvfile.ix[:, 0] == 'value']
# # values = dict(value_directives.ix[:,(1,2)].values)
# # print ('Values')
# # pprint(values)
# # print ('--')
# values = {
	# 'capital': 100
# ,	'credit': 500
# ,	'deposit': 300
# }

# WARNING: solve_lin_system is undefined
#x = solve_lin_system(multipliers, equations, values)
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

variables, values = zip(*dict1.items())
data1 = pd.DataFrame(np.array(values),
                     index=variables,
                     columns=['x'])

# Our result contains more variables than
# what we have in x.
print(x.ix[data1.index])
print(data1)

#TODO 3:
# write back 'x' to corresponding 'value' rows in period 1 in csv sheet input.tab using pandas

def floatcomma(f):
    return ('%.2f' % f).replace('.', ',')

def write_tabfile(values, equations, multipliers, tabfile):
    with open(tabfile, 'w') as fd:
        fd.write('\tValues\t\n')
        [fd.write('value\t%s\t%s\n' % (name, floatcomma(value)))
            for name, value in values.items()]

        fd.write('\n')
        fd.write('\tMultipliers:\t\n')
        [fd.write('multiplier\t%s\t%s\n' % (name, floatcomma(value)))
            for name, value in multipliers.items()]

        fd.write('\n')
        fd.write('\tEquations:\t\n')
        [fd.write('equation\t%s\t\n' % value) for value in equations]

write_tabfile(x['x'].to_dict(), equations, multipliers, 'tabfile')

csvfile = pd.read_csv('tabfile', sep='\t', skip_blank_lines=True, decimal=',')
print(csvfile)
