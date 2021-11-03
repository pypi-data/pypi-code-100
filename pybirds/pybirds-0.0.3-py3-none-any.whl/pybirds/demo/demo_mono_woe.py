import numpy as np
from pprint import pprint

from pybirds.data import data_loader
from pybirds.util.model_helper import mono_woe


def main():
    # prepare data
    df_data = data_loader.DataLoader.get_credit_german_data()
    df_data.loc[df_data['age'] > 40, 'age'] = np.nan
    df_data.loc[(df_data['age'] > 35) & (df_data['age'] <= 40), 'age'] = -991001
    df_data.loc[df_data['status_account'] == 'A11', 'status_account'] = 'NA_A11'

    feature_list = ['status_account', 'duration', 'credit_history', 'purpose', 'amount',
                    'svaing_account', 'present_emp', 'income_rate', 'personal_status',
                    'other_debtors', 'residence_info', 'property', 'age', 'inst_plans',
                    'housing', 'num_credits', 'job', 'dependents', 'telephone',
                    'foreign_worker']
    label = 'target'
    categorical_features = ['status_account', 'credit_history', 'purpose', 'svaing_account',
                            'present_emp', 'personal_status', 'other_debtors', 'property', 'inst_plans',
                            'housing', 'job', 'telephone', 'foreign_worker']

    # fit WOE
    woe = mono_woe.WOE()
    woe.fit(df_data[feature_list], df_data[label],
            categorical_features=categorical_features,
            missing_values=[-991001, 'NA_A11'])

    # transform WOE
    df_woe = woe.transform(df_data, method='woe')
    df_bin = woe.transform(df_data, method='bin')

    print(df_woe)
    print(df_bin)
    print(woe.bin_info.loc[woe.bin_info['var'] == 'age'])
    print(woe.bin_info.loc[woe.bin_info['var'] == 'status_account'])

    # adding split point
    woe.update_by_insert_value(df_data['age'], df_data[label], 20)

    # get bin info
    pprint(woe.export())


if __name__ == '__main__':
    main()
