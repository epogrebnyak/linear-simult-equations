"""
   Import linear model specification from CSV file, iterate model by period and write output CSV file.
   Model defined by 'multipliers', 'equations', 'values'
   
   Main entry:  process_model(input_csv_file, output_csv_file)

"""

import pandas as pd
import numpy as np
import os


from string2sim import solve_lin_system
from pprint import pprint
from collections import OrderedDict

def read_input_dataframe_from_csv(csv_file):
    """
     Reads csv sheet using pandas, returns dataframe.
        Comma is decimal sign here, 1,15 is 1.15
        Separator is  \t (tab)
    """

    # Dirty parse of the input file
    return pd.read_csv(csv_file, sep='\t', skip_blank_lines=True, decimal=',')


def parse_input_dataframe(input_df):
    """
    Parses raw dataframe into a cleaner one. Returns dataframe.
    """
    # Remove useless rows
    input_df = input_df[input_df.ix[:, 0].notnull()]
    # Strip whitespace from second column, where formulas are located

    # Pandas temporary disable false-positive warning
    pd.set_option('mode.chained_assignment', None)
    input_df.ix[:, 1] = input_df.ix[:, 1].str.strip()
    pd.set_option('mode.chained_assignment', 'warn')
    return input_df

def get_input_df(csv_file):
    """
    Get workable dataframe based on input file filename.
    Also checks if provided 'csv_file' exists.
    """
    if os.path.isfile(csv_file):
        input_df = read_input_dataframe_from_csv(csv_file)
        return  parse_input_dataframe(input_df)
    else:
        raise IOError("File does not exist: " + csv_file)

def get_directive_block(csv_file_df, pivot_label):
    """
    Return rows of *csv_file_df* that have *pivot_label* in their first column
    Pivot labels are 'value', 'equation', etc.
    """
    return csv_file_df[csv_file_df.ix[:, 0] == pivot_label]

def get_df_block_as_dict(csv_file_df, pivot_label, period, val_col_start = 2, key_col = 1):
    """
    Generic function to read a part of 'csv_file_df' dataframe  into a dictionary.

    Assumptions:
       pivot_label is in first column: csv_file_df.ix[:, 0]
       keys are in second column: key_col = 1
       values start in third column: val_col_start = 2
       column (val_col_start + period) is read as values
       period is zero-based (0, 1, ...)
    """
    # get actual column to import
    val_col = period + val_col_start
    # directive is a subset of csv_file_df
    directives = get_directive_block(csv_file_df, pivot_label)
    # return columns key_col, val_col of 'directives' as dictionary
    return OrderedDict(directives.ix[:,(key_col, val_col)].values)

def get_multipliers_as_dict(csv_file_df, period):
    """
    Returns multipliers for 'period' as dictionary
    """
    return get_df_block_as_dict(csv_file_df, 'multiplier', period)

def get_values_as_dict(csv_file_df, period):
    """
    Returns values for 'period' as dictionary
    """
    return get_df_block_as_dict(csv_file_df, 'value', period)

def get_value_lag_as_dict(csv_file_df, period):
    """
    Returns lagged values for 'period' as dictionary
    """
    return get_df_block_as_dict(csv_file_df, 'value_lag', period)

def get_equations_as_list(csv_file_df):
    """
    Returns equations
    """
    return list(get_df_block_as_dict(csv_file_df, 'equation', 0).keys())

def create_output_df(values_list, equations, multipliers_list, write_lagged=True):
    """
    Returns a dataframe, replicating input.tab structure

    Parameters:
    values_list: list of values (dict) for each period
    equations: list of strings representing relationships
    multipliers_list: list of multipliers (dict) for each period
    """

    nperiods = len(values_list)

    blank_line = [None] * (nperiods + 2)

    # Values section
    fields = []
    fields.append([None, 'Variables'] + [None] * nperiods)

    names = values_list[0].keys()
    for name in names:
        fields.append(['value', name] + [values[name] for values in values_list])

    # Values Lagged section
    if write_lagged:
        fields.append(blank_line)
        fields.append([None, 'Lagged Variables'] + [None] * nperiods)

        # We write lagged values in the appropriate column...
        names = values_list[0].keys()
        for name in names:
            fields.append(['value_lag', name, None] + [values[name] for values in values_list[:-1]])
    else:
        # Blank
        [fields.append(blank_line) for i in range(len(names) + 2)]

    # Multipliers section
    fields.append(blank_line)
    fields.append([None, 'Multipliers:'] + [None] * nperiods)
    names = multipliers_list[0].keys()
    for name in names:
        fields.append(['multiplier', name] + [mutlipliers[name]
                       for mutlipliers in multipliers_list])

    # Equations section
    fields.append(blank_line)
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


def dump_csv_output(values_list, equations, multipliers_list, tabfile, write_lagged=True):
    """
    Writes results to output *tabfile*.    
    """
    df = create_output_df(values_list, equations, multipliers_list, write_lagged)
    write_csv_tabfile(df, tabfile)

def get_input_dataframes(input_csv_file, supplementary_input_csv_file = None):
    """
    High-lever wrapper to import model parameters from 'input_csv_file', 'supplementary_input_csv_file'

    Note: supplementary_input_csv_file allows to specify the model (euqations and multipliers)
          in separate file and actual data in another file.
    """
    # WARNING: must ensure that program does not stall if there are no 'equation' or 'multiplier'
    #          label in input csv file, or no 'value' labels in file.
    #          Script not tested with different input files.

    df1 = get_input_df(input_csv_file)
    if supplementary_input_csv_file is None:
        df2 = df1
    else:
        df2 = get_input_df(supplementary_input_csv_file)
    return df1, df2

def get_input_parameters(df1, df2, period):
    """
    Provide a model specification based on dataframes df1, df2
    Returns a tuple of model specification:
         values, multipliers, equations
    """
    # NOT TODO: may extend to df1, df2, df3

    values = get_values_as_dict(df1, period)
    multipliers = get_multipliers_as_dict(df2, period)
    equations   = get_equations_as_list(df2)

    # NOT TODO: may print in some tabular format one next to another. 
    print ('\nMultipliers:')
    pprint(multipliers)
    print ('\nValues:')
    pprint(values)
    print ('\nEquations:')
    pprint(equations)

    return (values, multipliers, equations)

def get_row_from_csv_dataframe(df, group, label): 
    """
    Returns a row of values (as a list) given *group* in first column and label in second.
    """    
    value_df = get_directive_block(df, group)
    labels_in_df = value_df.ix[:, 1]
    row_ix = (labels_in_df == label).nonzero()[0][0]
    return (value_df
            .ix[row_ix, :]  # Select period column
            .convert_objects(convert_numeric=True) # Set strings to NaN
            .dropna() # Remove NaN
            .values
            .astype('int')) # Get them
    
def get_periods_as_list(df):
    '''Returns list of periods declared. 
    Expected return [0, 1, 2, n]'''
    return get_row_from_csv_dataframe(df, 'value', 'period')
    

def _get_result_as_dict(x, values):
    # We need to filter out the lagged variables
    result_fields = [k for k in values if not k.endswith('_lag')]
    return x.ix[result_fields].to_dict()['x']

def df_has_block(df, section_name):
    '''Return True if dataframe has a block given by *section_name*'''
    return np.any(df.ix[:, 0].str.contains(section_name).values)

def process_model(input_csv_file, output_csv_file, supplementary_input_csv_file = None):

    df1, df2 = get_input_dataframes(input_csv_file, supplementary_input_csv_file)

    # 'periods' hold actual number of periods in the model
    periods = get_periods_as_list(df1)
    # check if we need lag handling
    has_lags = df_has_block(df1, 'value_lag')

    # Period 0 is reported data, we store it and not process
    values0, multipliers0, equations = get_input_parameters(df1, df2, 0)
    values_holder_list = [values0]
    # we put multipliers in holder list, because we want to write them down in ouput csv by period
    multiplier_holder_list = [multipliers0]

    # We start processing from period 1
    for p in periods[1:]:
        print("-------- Period", p)
        values, multipliers, equations = get_input_parameters(df1, df2, p)

        if has_lags:
            # get system definiton
            values_lagged = get_df_block_as_dict(df1, 'value_lag', p)
        else:
            # The linear system uses lagged variables as an input
            # here we construct them from last period
            previous_period_values = values_holder_list[-1]
            values_lagged = {k + '_lag' : previous_period_values[k]  for k in last_values}

        # solving the system:
        x = solve_lin_system(multipliers, equations, values_lagged)

        # 'x' must be saved to a new array/dataframe/list holding results for all periods
        # GL: We save into a list containing results + multipliers for the
        # current period
        values_holder_list.append(_get_result_as_dict(x, values))
        multiplier_holder_list.append(multipliers)

    # save results
    # must save array/dataframe/list holding results for all periods
    # dump_csv_output() should  be dump_csv_output(output_df, output_csv_file)
    # GL: we pass lists of values and multipliers
    
    dump_csv_output(values_holder_list,
                    equations,
                    multiplier_holder_list,
                    output_csv_file,
                    write_lagged=has_lags)
    

if __name__ == "__main__":

    testfiles =  [
        ('input2.tab', 'output2.tab'),
            # this is dataset with several periods
            # sheet 'input_multiple_period' in examples.xls
        ('input3.tab', 'output3.tab')
            # this is dataset with several periods and no lag virables
            # sheet 'input_multiple_period_nolag' in examples.xls
    ]

    for pair in testfiles:
        _in  = pair[0]
        _out = pair[1]
        try: 
            process_model(_in, _out)
            print("Done processing: " + _in)
        # WARNING: 'except' shuts down error messages
        except:
            print("Cannot process: " + _in)

#
# Next stage (not-todo): 
#
# - need new checks procedure - compare results for each period with values for that period in 
# - dump_csv_output depends on formatting within the function, not input.csv file
# - round values in 'values' with global PRECISION = 2 114.99999999999997 --> 115.00
#
# Not todo: 
# - xls io:
#      must read input_csv_file and supplementary_input_csv_file from Excel
#      must write output_csv_file to Excel
#      implement after behaviour is specified, not todo now.
#