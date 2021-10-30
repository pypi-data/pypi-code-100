import numpy as np
from tqdm import tqdm
from numpy import dot
from numpy.linalg import norm


def save_as_vec_file(model, vec_file):
    # get all words from model
    words = model.get_words()
    print(str(len(words)) + " " + str(model.get_dimension()))
    # line by line, you append vectors to VEC file
    with open(vec_file, "w", encoding="utf-8") as file_out:
        file_out.write(
            str(len(words)) + " " + str(model.get_dimension()) + '\n')
        for w in tqdm(words):
            v = model.get_word_vector(w)
            vstr = ""
            for vi in v:
                vstr += " " + str(vi)
            try:
                file_out.write(w + vstr + '\n')
            except:
                pass


def cosine_sim(a: np.array, b: np.array):
    cos_sim = dot(a, b) / (norm(a) * norm(b))

    return cos_sim


def cosine_sim_list(a: np.array, lst: list):
    cos_sim = [cosine_sim(a, b) for b in lst]

    return cos_sim
