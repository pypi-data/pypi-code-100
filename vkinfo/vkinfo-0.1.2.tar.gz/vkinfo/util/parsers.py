import logging
import pandas as pd


pd.options.mode.chained_assignment = None  # default='warn'

def parse_friends_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Function for reshaping given dataframe to desired format

    Args:
        df: pandas dataframe with raw response from api

    """
    logging.info("Putting collected data in order..")
    # Rename columns to get rid of levels
    df.rename(columns={"city.title": "city",
                    "country.title": "country"}, inplace=True)
    # rearrange columns & delete redundant
    df = df[['id', 'first_name', 'last_name',
                        'country', 'city', 'bdate', 'sex']]
    
    # NB! Чтобы правильно обработать дату рождения нужно учитывать, что не все заполняют её
    # полностью. Для этого создаем доп колонку format и через регулярное выражение отмечаем варианты ввода:
    # format = 1 if bdate == '%d.%m'
    # format = 2 if bdate == '%d.%m.%Y'
    # Затем, в зависимости от format преобазуем дату в datetime object и приводим к ISO виду
    logging.info("formatting birth date to ISO..")
    df['format'] = 1
    df.loc[df.bdate.str.match(r'\d{1,2}\.\d{1,2}\.\d{4}', na=False), 'format'] = 2
    # ! leap year problem
    df.loc[df.format == 1, 'bdate'] = pd.to_datetime(df.loc[df.format == 1, 'bdate'] + '.2000', format = '%d.%m.%Y').dt.strftime('%m-%d')
    df.loc[df.format == 2, 'bdate'] = pd.to_datetime(df.loc[df.format == 2, 'bdate'], format = '%d.%m.%Y').dt.strftime('%Y-%m-%d')
    df.drop(columns=['format'], inplace=True)
    
    # remove rows w/ deleted users
    logging.info("Removing deleted accounts..")
    logging.debug(f"Deactivated objects count: {df[df['first_name'] == 'DELETED']['first_name'].count()}")
    df = df[df.first_name != 'DELETED']
    
    # sort rows by first_name
    df.sort_values(by=['first_name'], inplace=True)
    
    return df