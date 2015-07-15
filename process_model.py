from string2sim import solve_lin_system
import pandas as pd
import numpy as np
from pprint import pprint
import os


def read_input_dataframe_from_csv(csv_file):
     """
     Reads csv sheet using pandas, returns dataframe.
        Comma is decimal sign here, 1,15 is 1.15
        Separator is  \t (tab)
     """
     # COMMENT (NOT TODO): the intent is to be able to switch to reading/writing xls files later.

     # Dirty parse of the input file
     raw_df = pd.read_csv(csv_file, sep='\t', skip_blank_lines=True, decimal=',')
     return raw_df

def parse_input_dataframe(input_df):
    """
    Parses raw dataframe into a cleaner one. Returns dataframe.
    """
    # Remove useless rows
    input_df = input_df[input_df.ix[:, 0].notnull()]
    # Strip whitespace from second column, where formulas are located
    input_df.ix[:, 1] = input_df.ix[:, 1].str.strip()
    return input_df

def get_input_df(csv_file):
    """
    Wrapper to get workable dataframe based on input file filename.
    Also checks if 'csv_file' exists.
    """
    if os.path.isfile(csv_file):
        input_df = read_input_dataframe_from_csv(csv_file)
        return  parse_input_dataframe(input_df)
    else:
        raise IOError("File does not exist: " + csv_file)

def get_directive_block(csv_file_df, pivot_label):
    """
    Return rows of *csv_file_df* that have *pivot_label* in their first column
    """
    return csv_file_df[csv_file_df.ix[:, 0] == pivot_label]

def get_df_block_as_dict(csv_file_df, pivot_label, period, val_col_start = 2, key_col = 1):
    """
    Generic function to read a part of dataframe (csv_file_df) into a dictionary.

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
    return dict(directives.ix[:,(key_col, val_col)].values)

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

# TODO 3:
# write back 'x' to corresponding 'value' rows in period 1 in csv sheet input.tab using pandas
# EP: done

# TODO 3+1: values and multipliers can be an array/dataframe if there are many periods.
#           create_output_df() must work with an array/dataset of 'values'
#           see also comment for TODO 3+1

# TODO 3+2: we currently supress input file structure (number of empty lines, headers, etc).
#           better - take
#              raw_df = pd.read_csv(csv_file, sep='\t', skip_blank_lines=True, decimal=',')
#          and poppulate it with new values for different periods for 'values' part
#          may leave 'equations' and 'multipliers' intact (mark as WARNING though because it hides
#          values actually used in computation)
#          This way the call will be:
#                create_output_df(values, csvfile):
#          Please comment/discuss.


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
    fields.append([None, 'Values'] + [None] * nperiods)

    names = values_list[0].keys()
    for name in names:
        fields.append(['value', name] + [values[name] for values in values_list])

    # Values Lagged section
    if write_lagged:
        fields.append(blank_line)
        fields.append([None, 'Lagged Values'] + [None] * nperiods)
        
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
    Writes results to output 'tabfile'.
    """
    df = create_output_df(values_list, equations, multipliers_list, write_lagged)
    write_csv_tabfile(df, tabfile)

def get_ref_array():
    """
    Stores hardcoded reference dictionary.
    """
    dict1 = {'period': 1
            ,'credit': 115
            ,'liq': 23
            ,'capital': 30
            ,'deposit': 99
            ,'profit': 7.23
            ,'fgap': 1.77
    }

    variables, vals = zip(*dict1.items())
    return pd.DataFrame(np.array(vals),
                         index=variables,
                         columns=['x'])
    

def check_x_against_reference(x, ref):
    """
    Checkes if result 'x' is identical to hardcoded dictionary 'ref'.
    """
    print("\nReference data:")
    print(ref)

    print("\nFound solution:")
    print(x.ix[ref.index])

    # To actually assert their equality use np.allclose()
    is_identical = np.allclose(ref, x.ix[ref.index])
    print('\nMatching values?', is_identical)
    return is_identical

def get_input_dataframes(input_csv_file, supplementary_input_csv_file = None):
    """
    High-lever wrapper to import model parameters from 'input_csv_file', 'supplementary_input_csv_file'


    Note: supplementary_input_csv_file allows to specify the model (euqations and multipliers)
          in separate file and actual data in another file.
    """
    # WARNING: must ensure that program does not stall if there are no 'equation' or 'multiplier'
             # label in input csv file, or no 'value' labels in file.
             # Script not tested with differnt input files.

    df1 = get_input_df(input_csv_file)
    if supplementary_input_csv_file is None:
        df2 = df1
    else:
        df2 = get_input_df(supplementary_input_csv_file)
    return df1, df2

def get_input_parameters(df1, df2, period):
    """
    Retrun model specification based on dataframes df1, df2
    Returns a tuple of model specification:
         values, multipliers, equations
    """
    # NOT TODO: may extend to df1, df2, df3

    values = get_values_as_dict(df1, period)
    multipliers = get_multipliers_as_dict(df1, period)
    equations   = get_equations_as_list(df1)

    print ('\nMultipliers:')
    pprint(multipliers)
    print ('\nValues:')
    pprint(values)
    print ('\nEquations:')
    pprint(equations)

    return (values, multipliers, equations)

def get_periods(df):
    '''Return declared periods in dataframe'''
    # Periods are extracted from value column
    value_df = get_directive_block(df, 'value')
    variables = value_df.ix[:, 1]
    period_ix = (variables == 'period').nonzero()[0][0]
    return (value_df
            .ix[period_ix, :]  # Select period column
            .convert_objects(convert_numeric=True) # Set strings to NaN
            .dropna() # Remove NaN
            .values
            .astype('int')) # Get them

def _get_result_as_dict(x, values):
    #result_fields = [k.replace('_lag', '') for k in values]

    # We need to filter out the lagged variables
    result_fields = [k for k in values if not k.endswith('_lag')]
    return x.ix[result_fields].to_dict()['x']

def df_has_block(df, section_name):
    '''Return True if dataframe has a block given by *section_name*'''
    return np.any(df.ix[:, 0].str.contains(section_name).values)

def process_model(input_csv_file, output_csv_file, supplementary_input_csv_file = None):

    df1, df2 = get_input_dataframes(input_csv_file, supplementary_input_csv_file)

    # TODO: periods must hold actual number of periods in the model
    periods = get_periods(df1)
    # Check if we need lag handling
    has_lags = df_has_block(df1, 'value_lag')
    
    # Period 0 is reported data, we store it and not process
    values0, multipliers0, equations = get_input_parameters(df1, df2, 0)
    # We want to know if has lags

    values_results = [values0]
    multiplier_results =[multipliers0]

    # We start processing from period 1
    for p in periods[1:]:
        print("-------- Period", p)
        values, multipliers, equations = get_input_parameters(df1, df2, p)
        
        if has_lags:
            # get system definiton
            values_lagged = get_df_block_as_dict(df1, 'value_lag', p)
        else:
            # The linear system uses lagged variables as an input
            # here we retrieve them from last period
            last_values = values_results[-1]
            values_lagged = {k + '_lag' : last_values[k]  for k in last_values}
            
        # GL: constants are encoded differently now, must change input file
        values_lagged['one'] = 1.0
        values_lagged['half'] = 0.5

        # solving the system:
        x = solve_lin_system(multipliers, equations, values_lagged)
        
        # TODO: 'x' must be saved to a new array/dataframe/list holding results for all periods
        # GL: We save into a list containing results + multipliers for the
        # current period
        values_results.append(_get_result_as_dict(x, values))
        multiplier_results.append(multipliers)

        # check against a reference solution
        # WARNING: will not work in new versions with mutiple period or need to change
        # TODO: shet down check or change
        # check_x_against_reference(x, ref = get_ref_array())

    # save results
    # TODO: must save array/dataframe/list holding results for all periods
    # TODO: dump_csv_output() should  be dump_csv_output(output_df, output_csv_file)
    # GL: our result would be a list of (value, mutliplier) for each period
    #     instead of a dataframe, is that OK?

    dump_csv_output(values_results, 
                    equations, 
                    multiplier_results, 
                    output_csv_file,
                    write_lagged=has_lags)
    values = multipliers = equations = None


if __name__ == "__main__":

    testfiles =  [
                #('input.tab', 'output.tab'), # this is baseline dataset (periods 0 and 1 only)
                                            # sheet 'input_one_period' in examples.xls
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

        process_model(_in, _out)
        print("Done processing: " + _in)
    #except:
    #   print("Cannot process: " + _in)

# 2015-07-14 04:36 PM
# FOLLOW-UP 1: equation parser change
#         1.1    period = period_lag + 1
#         1.2    avg_credit = 0.5 * credit + 0.5 * credit_lag
#            as commented in parse_additive_terms.py lines 20-50
# FOLLOW-UP 2: multi-period, different csv input file
#              upon realisation of this stage baseline dataset 'input.tab' will not work,
#              new baseline will be 'input_5periods.tab'
#              staкt calculations at period 1
#           2.5 need new checks procedure - compare results for each period with values for that period.
#
# FOLLOW-UP 3: lagged variable not shown in input file
#              process 'input_5periods_no_lag_var.tab' - it does not have '*_lag' variablesin sheet,
#                                                        must create them with proper lagging
#                                                        (values for period 0 become '*_lag' variables for  period 1)
#                                                         intent: we keep only variables, multipliers and eqations in file, to keep it neat/minmal)
# NOT TODO 4: xls io:
#                     must read input_csv_file and  supplementary_input_csv_file from Excel
#                     must write output_csv_file to Excel
#                     implement after behaviour is specified, not todo now.
#  OPTIONAL: Round values in 'values' with global PRECISION = 2
#            114.99999999999997 --> 115.00



 
