import pandas as pd

def convert_columns(df, column_dict):
    new_df = df.rename(columns=column_dict)
    new_df = new_df[column_dict.values()]
    return new_df


# 对比两个df的体系数据差异
def get_diff_df(left_df, right_df, subset, id_key='Id'):
    def report_diff(x):
        return x[0] if x[0] == x[1] else '{} → {}'.format(*x)

    left_df.fillna('', inplace=True)  # 去掉excel的空：nan
    right_df.fillna('', inplace=True)
    left_df['version'] = "left"
    right_df['version'] = "right"
    old_accts_all = set(left_df[id_key])
    new_accts_all = set(right_df[id_key])

    dropped_accts = old_accts_all - new_accts_all
    added_accts = new_accts_all - old_accts_all
    # 合并两个项目列表
    all_data = pd.concat([left_df, right_df], ignore_index=True)
    # 去除重复的项目（没有变化的项目）subset里不包含version
    changes = all_data.drop_duplicates(subset=subset, keep='last')

    # 查找duplicated的id 生成一个list
    dupe_accts = changes[changes[id_key].duplicated() == True][id_key].tolist()
    # 检索出所有在id重复列表中的row
    dupes = changes[changes[id_key].isin(dupe_accts)]

    # Pull out the old and new data into separate dataframes
    change_new = dupes[(dupes["version"] == "right")]
    change_old = dupes[(dupes["version"] == "left")]

    # Drop the temp columns - we don't need them now
    change_new = change_new.drop(['version'], axis=1)
    change_old = change_old.drop(['version'], axis=1)

    # Index on the account numbers
    change_new.set_index(id_key, inplace=True)
    change_old.set_index(id_key, inplace=True)

    # Combine all the changes together
    df_all_changes = pd.concat([change_old, change_new],
                               axis='columns',
                               keys=['left', 'right'],
                               join='outer')

    df_all_changes = df_all_changes.swaplevel(axis='columns')[change_new.columns[0:]]
    df_changed = df_all_changes.groupby(level=0, axis=1).apply(lambda frame: frame.apply(report_diff, axis=1))
    df_changed = df_changed.reset_index()

    df_removed = changes[changes[id_key].isin(dropped_accts)]
    df_added = changes[changes[id_key].isin(added_accts)]

    return df_changed, df_removed, df_added

# old = pd.read_excel(old_file_name, 'Sheet1', na_values=['NA'])
# new = pd.read_excel(new_file_name, 'Sheet1', na_values=['NA']) # reload from excel
# subset = old.columns
# df_changed, df_removed, df_added = get_diff_df(old, new, subset)