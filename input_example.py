from string2sim import solve_lin_system
import pandas as pd
import numpy as np
from pprint import pprint

# TODO 1:
# read csv sheet input.tab using pandas
#     strip whitespace in second column
#     comma is decimal sign here, 1,15 is 1.15
#     separator is  \t tab
# EP: done

def read_input_dataframe_from_csv(csv_file):
     """
     Comment: the intent is to be able to switch to reading/writing xls files later.
     Not todo now.
     """
     # Dirty parse of the input file
     raw_df = pd.read_csv(csv_file, sep='\t', skip_blank_lines=True, decimal=',')
     return raw_df

def parse_input_dataframe(input_df):    
    # Remove useless rows
    input_df = input_df[input_df.ix[:, 0].notnull()]
    # Strip whitespace from second column, where formulas are located    
    input_df.ix[:, 1] = input_df.ix[:, 1].str.strip()
    return input_df

def get_input_df(csv_file):
    input_df = read_input_dataframe_from_csv(csv_file)
    return  parse_input_dataframe(input_df)    
     
     
# TODO 2:
# produce 'mutipliers', 'equations', 'values 'in data structures 
# use period 0 data
# EP: done

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

# TODO 3:
# write back 'x' to corresponding 'value' rows in period 1 in csv sheet input.tab using pandas
# EP: done

def create_output_df(values0, values1, equations, multipliers):
    """
    Returns a dataframe, replicating input.tab structure 

    Parameters:
    values0: dictionary of variable values at lag 0
    values1: dictionary of variable values at lag 1
    equations: list of strings representing relationships
    multipliers: dicionary of multipliers
    """

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
    return pd.DataFrame(fields)

def write_csv_tabfile(df, tabfile):
    """
    Write resulting dataframe to a csv file.
    
    Parameters:
    df: resulting dataframe
    tabfile: output filename
    """       
    df.to_csv(tabfile, sep='\t', decimal=',', header=False, index=False)

def dump_csv_output(values0, values1, equations, multipliers, tabfile):
    df = create_output_df(values0, values1, equations, multipliers)
    write_csv_tabfile(df, tabfile)    

def get_ref_array():
    dict1 = {	'period'	:	1
    ,	'credit'	:	115
    ,	'liq'	:	23
    ,	'capital'	:	30
    ,	'deposit'	:	99
    ,	'profit'	:	7.23
    ,	'fgap'	:	1.77
    }

    variables, vals = zip(*dict1.items())
    data1 = pd.DataFrame(np.array(vals),
                         index=variables,
                         columns=['x'])
    return data1
    
if __name__ == "__main__":

    df = get_input_df('input.tab')
    multipliers = get_multipliers_as_dict(df)
    values      = get_values_as_dict(df, 0)
    equations   = get_equations_as_list(df)

    print ('\nMultipliers:')
    pprint(multipliers)
    print ('\nValues:')
    pprint(values)
    print ('\nEquations:')
    pprint(equations)
    
    # solving the system:
    x = solve_lin_system(multipliers, equations, values)

    # CHECK 1:
    # change dict1 type to nparray
    # compare dict_1 to x

    data1 = get_ref_array()
    print("Reference data:")
    print(data1)

    print("Found solution:")
    print(x.ix[data1.index])

    # To actually assert their equality use np.allclose()
    print('Matching values?', np.allclose(data1, x.ix[data1.index]))
        
        
    result_fields = [k.replace('_lag', '') for k in values]
    result_fields_as_dict = x.ix[result_fields].to_dict()['x']
    
    dump_csv_output(values, result_fields_as_dict, equations, multipliers, 'output.tab')

#FOLLOW-UP 1: equation parser change
#                 period = period_lag + 1
#                 avg_credit = 0.5 * credit + 0.5 * credit_lag
#FOLLOW-UP 2: multi-period 
#FOLLOW-UP 3: lagged variable not shown in input file 
#FOLLOW-UP 4: xls io
