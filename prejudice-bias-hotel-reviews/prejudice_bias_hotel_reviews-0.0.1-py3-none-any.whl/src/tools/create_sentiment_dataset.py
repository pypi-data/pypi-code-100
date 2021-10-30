import os
import sys
import ast
import argparse
import fasttext
import fasttext.util
import nltk
import pyfiglet
import pandas as pd

from pathlib import Path
from textblob_de.lemmatizers import PatternParserLemmatizer

from src.utils.utils_console import bcolors, clear
from src.dataset.utils import load_ethnicities

my_parser = argparse.ArgumentParser(description='Creates a dataset for sentiment analysis')
my_parser.add_argument('--data_path',
                       type=str,
                       required=True,
                       help='path to the cleaned dataset to load.')
my_parser.add_argument('--save_file',
                       type=str,
                       required=True,
                       help='path to the save file, if existing this will be loaded.')
my_parser.add_argument('--ethnicities_file',
                       type=str,
                       required=True,
                       help='path to the ethnicities file.')
args = my_parser.parse_args()

if __name__ == "__main__":
    # clear the entire console
    clear(line=False)

    # display a header :)
    res = pyfiglet.figlet_format('Sentiment Dataset Creation')
    print(res)

    # get the arguments
    data_path = Path(args.data_path)
    save_path = Path(args.save_file)
    ethnien_path = Path(args.ethnicities_file)

    # check the arguments
    if not data_path.is_file():
        print(f'{bcolors.FAIL}The specified dataset does not exist.{bcolors.ENDC}')
        sys.exit()
    print(f'{bcolors.OKGREEN}Loading dataset from: {bcolors.ENDC}{data_path}')

    if save_path.is_file():
        print(f'{bcolors.OKGREEN}Loading existing dataset from: {bcolors.ENDC}{save_path}')
        df_dataset = pd.read_csv(save_path, index_col=0)
    else:
        print(f'{bcolors.OKGREEN}Creating new dataset at: {bcolors.ENDC}{save_path}')
        df_dataset = pd.DataFrame()

    if not ethnien_path.is_file():
        print(f'{bcolors.FAIL}Ethnien dataset does not exist.{bcolors.ENDC}')
        sys.exit()
    print(f'{bcolors.OKGREEN}Loading ethnicities file from: {bcolors.ENDC}{ethnien_path}')
    print()

    # create the helpers
    fasttext.FastText.eprint = lambda x: None
    fasttext.util.download_model('de', if_exists='ignore')
    model = fasttext.load_model('cc.de.300.bin')
    lemmatizer = PatternParserLemmatizer()
    counter = 0

    # load the datasets
    df = pd.read_csv(data_path, index_col=0)
    demonyme = load_ethnicities(ethnien_path, model)

    # information about the labeling
    print(f'{bcolors.WARNING}Press Q to quit and save the file{bcolors.ENDC}\n')

    # start the annotation loop
    while True:
        # randomly sample 100 rows
        df_annot = df.sample(n=1000)
        df_annot.tokens = df_annot.tokens.apply(ast.literal_eval)

        # lemmatize the tokens
        df_annot['lemma'] = df_annot.tokens.apply(lambda tokens: [lemmatizer.lemmatize(x) for x in tokens])
        df_annot['lemma'] = df_annot.lemma.apply(lambda lst: [x[0][0] for x in lst if len(x) > 0])

        # check which review a nation contains
        df_annot['nations'] = df_annot.lemma.apply(lambda lst: [x for x in lst if x in demonyme])
        nationality = df_annot[df_annot['nations'].apply(len) > 0]

        # loop over all the reviews contains nationality
        for i, row in nationality.iterrows():
            # check if it's not alrady in the labeled dataset
            if len(df_dataset) > 0:
                labelled = ((df_dataset.bid == row.bid) &
                            (df_dataset.id == row.id) &
                            (df_dataset.text == row.text)).all()
                if labelled:
                    continue

            print(f'Labeled so far: {counter}\n')
            print(f'{row.text}\n')
            prediction = input('Is the sentence positive (P), negative (N), neutral (E) or set marker (X): ')
            if str(prediction).lower() == 'q':
                break
            row['prediction'] = prediction
            df_dataset = df_dataset.append(row)
            counter += 1

            # calculate how many clears are necessary
            lines_printed = int(len(row.text) / os.get_terminal_size().columns) + 5
            for _ in range(lines_printed):
                clear(line=True)

        # pass the break signal along
        if str(prediction).lower() == 'q':
            break

    df_dataset.to_csv(str(save_path))
    print(f'{bcolors.OKGREEN}Saved dataset to: {bcolors.ENDC}{save_path}')
