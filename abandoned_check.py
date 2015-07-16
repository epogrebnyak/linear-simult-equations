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