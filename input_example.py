#from string2sim import solve_lin_system
import pandas as pd
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

multiplier_directives = csvfile[csvfile.ix[:, 0] == 'multiplier']
multipliers = dict(multiplier_directives.ix[:,1:3].values)
print ('Multipliers')
pprint(multipliers)
print ('---')
#multipliers = {
#	'liq_share':  .20
#,	'credit_ir': .10
#,	'deposit_ir': .05
#}

equation_directives = csvfile[csvfile.ix[:, 0] == 'equation']
equations = equation_directives.ix[:,1].values.tolist()
print ('Equations')
pprint(equations)
print ('--')
#equations =  [
#	'ta = credit + liq'
#,	'liq = credit * liq_share'
#,	'profit = credit * credit_ir - deposit * deposit_ir'
#,	'fgap = ta - capital - profit - deposit'
#]

value_directives = csvfile[csvfile.ix[:, 0] == 'value']
values = dict(value_directives.ix[:,(1,2)].values)
print ('Values')
pprint(values)
print ('--')
#values = {
#	'capital': 100
#,	'credit': 500
#,	'deposit': 300
#}

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
print (dict1)
# CHECK 1:
# change dict1 type to nparray
# compare dict_1 to x

#TODO 3:
# write back 'x' to corresponding 'value' rows in period 1 in csv sheet input.tab using pandas
