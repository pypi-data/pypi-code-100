def log_to_dataframe(dataframe, index, log_dict):
    """
    Logs data to dataframe.

    :param dataframe: Dataframe to log to.
    :param index: The indices to log to.
    :param log_dict: The dictionary containing data to log
    :return: updated dataframe.
    """
    for key in list(log_dict.keys()):
        if key not in dataframe.columns:
            if type(log_dict[key])==list:
                dataframe[key] = [[] for i in range(len(dataframe))]
            else:
                dataframe[key] = ""
            dataframe[key].astype("object")
        if type(log_dict[key]) == list:
            for idx in range(len(list(index))):
                for val in log_dict[key][idx]:
                    dataframe.loc[index[idx], key].append(val)

        else:
            dataframe.loc[index, key] = log_dict[key]
    return dataframe
