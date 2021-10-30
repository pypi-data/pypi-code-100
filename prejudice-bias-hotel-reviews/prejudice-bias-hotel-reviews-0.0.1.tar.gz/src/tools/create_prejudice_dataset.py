import os
import sys
import ast
import argparse
import spacy
import swifter
import fasttext
import fasttext.util
import nltk
import pyfiglet
import pandas as pd

from pathlib import Path
from transformers import AutoTokenizer, AutoModel

from src.utils.utils_console import bcolors, clear
from src.embedding.bert_embedder import BERTEmbedder
from src.utils.nlp_augmentation import NLPAugmenter

my_parser = argparse.ArgumentParser(description='Creates a dataset for detecting prejudice')
my_parser.add_argument('--data_path',
                       type=str,
                       required=True,
                       help='path to the cleaned dataset to load.')
my_parser.add_argument('--save_file',
                       type=str,
                       required=True,
                       help='path to the save file, if existing this will be loaded.')
args = my_parser.parse_args()


if __name__ == "__main__":
    # clear the entire console
    clear(line=False)

    # display a header :)
    res = pyfiglet.figlet_format('Prejudice Dataset Creation')
    print(res)

    # get the arguments
    data_path = Path(args.data_path)
    save_path = Path(args.save_file)

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
    print()

    # create the NLP augmentator
    nlp_augmenter = NLPAugmenter(ft_model=None)

    # load the embedded dataset
    df_bert = pd.read_csv(data_path, index_col=0)
    df_bert.embed = df_bert.embed.swifter.progress_bar(False).apply(ast.literal_eval)

    # load model from HuggingFace Hub
    tokenizer = AutoTokenizer.from_pretrained('FabianGroeger/HotelBERT')
    model = AutoModel.from_pretrained('FabianGroeger/HotelBERT')
    # define the embedder
    embedder = BERTEmbedder(model, tokenizer, df_bert)
    # define the spacy model for POS tagging
    nlp = spacy.load("de_core_news_sm")

    # information about the labeling
    print(f'{bcolors.WARNING}Press Q to quit and save the file{bcolors.ENDC}\n')

    # start the annotation loop
    while True:
        seed_sentence = input('Please enter a seed sentence: ')
        if str(seed_sentence).lower() == 'q':
            break
        # check the POS tags of the nearest neighbors
        df_neigh = embedder.get_neighbors(seed_sentence, n=10)
        df_neigh['pos'] = df_neigh.text.apply(lambda x: [(t.orth_, t.pos_, t.tag_) for t in nlp(x)])
        df_neigh['pos_fil'] = df_neigh.pos.apply(lambda x: [t for t in x if t[1] in ['VERB'] or t[2] in ['ADJD', 'PDS']])
        df_neigh.drop(columns=['id', 'bid', 'embed'])

        # filter the sentences for ones that have compatible POS tags
        df_neigh_filtered = df_neigh[df_neigh.pos_fil.apply(len) > 0]
        neigh_sentences = list(df_neigh_filtered.text)

        # loop over all possible prejudice and check them
        for poss_prejudice in neigh_sentences:
            print(poss_prejudice)

        # randomly sample 100 rows
        df_annot = df.sample(n=100)
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
