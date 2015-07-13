from string2sim import solve_lin_system

# TODO 1:
# read csv sheet input.tab using pandas
#     strip whitespace in second column
#     comma is decimal sign here, 1,15 is 1.15
#     separator is  \t tab

# TODO 2:
# produce 'mutipliers', 'equations', 'values 'in data structures similar to ones below
# use period 0 data

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

x = solve_lin_system(multipliers, equations, values)
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
