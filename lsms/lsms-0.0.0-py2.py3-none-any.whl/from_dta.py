import pandas as pd

def from_dta(fn):
    sr=pd.io.stata.StataReader(fn)
    values = sr.value_labels()

    var_to_label = dict(zip(sr.varlist,sr.lbllist))    

    df = sr.read(convert_categoricals=False)

    for var in sr.varlist: # Check mapping for each variable with values
        if len(var_to_label[var]):
            code2label = values[var_to_label[var]]
            try:
                df[var] = df[var].map(code2label)
            except KeyError:
                print('Extra categorical mapping: %s' % var)

    return df
