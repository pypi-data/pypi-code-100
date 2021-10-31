from mammut.common.indexer import NGramIndexer
import smtplib
from mammut.data.download import *
import os
import time


class Agenda:
    def __init__(self):
        self.ngram_indexer = NGramIndexer()
        self.ngram_data_path = ""
        self.set1_chars = [
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
            "g",
            "h",
            "i",
            "j",
            "k",
            "l",
            "m",
            "n",
            "o",
            "other",
            "p",
            "pos",
            "punctuation",
            "q",
            "r",
            "s",
            "t",
            "u",
            "v",
            "w",
            "x",
            "y",
            "z",
        ]

        self.set2_chars_1 = [
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "_ADJ_",
            "_ADP_",
            "_ADV_",
            "_CONJ_",
            "_DET_",
            "_NOUN_",
            "_NUM_",
            "_PRON_",
            "_PRT_",
            "_VERB_",
            "a_",
            "aa",
            "ab",
            "ac",
            "ad",
            "ae",
            "af",
            "ag",
            "ah",
            "ai",
            "aj",
            "ak",
            "al",
            "am",
            "an",
            "ao",
            "ap",
            "aq",
            "ar",
            "as",
            "at",
            "au",
            "av",
            "aw",
            "ax",
            "ay",
            "az",
            "b_",
        ]
        self.set2_chars_2 = [
            "ba",
            "bb",
            "bc",
            "bd",
            "be",
            "bf",
            "bg",
            "bh",
            "bi",
            "bj",
            "bk",
            "bl",
            "bm",
            "bn",
            "bo",
            "bp",
            "bq",
            "br",
            "bs",
            "bt",
            "bu",
            "bv",
            "bw",
            "bx",
            "by",
            "bz",
            "c_",
            "ca",
            "cb",
            "cc",
            "cd",
            "ce",
            "cf",
            "cg",
            "ch",
            "ci",
            "cj",
            "ck",
            "cl",
            "cm",
            "cn",
            "co",
            "cp",
            "cq",
            "cr",
            "cs",
            "ct",
            "cu",
            "cv",
            "cw",
            "cx",
            "cy",
            "cz",
            "d_",
            "da",
            "db",
        ]
        self.set2_chars_3 = [
            "dc",
            "dd",
            "de",
            "df",
            "dg",
            "dh",
            "di",
            "dj",
            "dk",
            "dl",
            "dm",
            "dn",
            "do",
            "dp",
            "dq",
            "dr",
            "ds",
            "dt",
            "du",
            "dv",
            "dw",
            "dx",
            "dy",
            "dz",
            "e_",
            "ea",
            "eb",
            "ec",
            "ed",
            "ee",
            "ef",
            "eg",
            "eh",
            "ei",
            "ej",
            "ek",
            "el",
            "em",
            "en",
            "eo",
            "ep",
            "eq",
            "er",
            "es",
            "et",
            "eu",
            "ev",
            "ew",
            "ex",
            "ey",
            "ez",
            "f_",
        ]
        self.set2_chars_4 = [
            "fa",
            "fb",
            "fc",
            "fd",
            "fe",
            "ff",
            "fg",
            "fh",
            "fi",
            "fj",
            "fk",
            "fl",
            "fm",
            "fn",
            "fo",
            "fp",
            "fq",
            "fr",
            "fs",
            "ft",
            "fu",
            "fv",
            "fw",
            "fx",
            "fy",
            "fz",
            "g_",
            "ga",
            "gb",
            "gc",
            "gd",
            "ge",
            "gf",
            "gg",
            "gh",
            "gi",
            "gj",
            "gk",
            "gl",
            "gm",
            "gn",
            "go",
            "gp",
            "gq",
            "gr",
            "gs",
            "gt",
            "gu",
            "gv",
            "gw",
            "gx",
            "gy",
            "gz",
            "h_",
            "ha",
            "hb",
        ]
        self.set2_chars_5 = [
            "hc",
            "hd",
            "he",
            "hf",
            "hg",
            "hh",
            "hi",
            "hj",
            "hk",
            "hl",
            "hm",
            "hn",
            "ho",
            "hp",
            "hq",
            "hr",
            "hs",
            "ht",
            "hu",
            "hv",
            "hw",
            "hx",
            "hy",
            "hz",
            "i_",
            "ia",
            "ib",
            "ic",
            "id",
            "ie",
            "if",
            "ig",
            "ih",
            "ii",
            "ij",
            "ik",
            "il",
            "im",
            "in",
            "io",
            "ip",
            "iq",
            "ir",
            "is",
            "it",
            "iu",
            "iv",
            "iw",
            "ix",
            "iy",
            "iz",
            "j_",
            "ja",
            "jb",
        ]
        self.set2_chars_6 = [
            "jc",
            "jd",
            "je",
            "jf",
            "jg",
            "jh",
            "ji",
            "jj",
            "jk",
            "jl",
            "jm",
            "jn",
            "jo",
            "jp",
            "jq",
            "jr",
            "js",
            "jt",
            "ju",
            "jv",
            "jw",
            "jx",
            "jy",
            "jz",
            "k_",
            "ka",
            "kb",
            "kc",
            "kd",
            "ke",
            "kf",
            "kg",
            "kh",
            "ki",
            "kj",
            "kk",
            "kl",
            "km",
            "kn",
            "ko",
            "kp",
            "kq",
            "kr",
            "ks",
            "kt",
            "ku",
            "kv",
            "kw",
            "kx",
            "ky",
            "kz",
            "l_",
            "la",
            "lb",
        ]
        self.set2_chars_7 = [
            "lc",
            "ld",
            "le",
            "lf",
            "lg",
            "lh",
            "li",
            "lj",
            "lk",
            "ll",
            "lm",
            "ln",
            "lo",
            "lp",
            "lq",
            "lr",
            "ls",
            "lt",
            "lu",
            "lv",
            "lw",
            "lx",
            "ly",
            "lz",
            "m_",
            "ma",
            "mb",
            "mc",
            "md",
            "me",
            "mf",
            "mg",
            "mh",
            "mi",
            "mj",
            "mk",
            "ml",
            "mm",
            "mn",
            "mo",
            "mp",
            "mq",
            "mr",
            "ms",
            "mt",
            "mu",
            "mv",
            "mw",
            "mx",
            "my",
            "mz",
            "n_",
            "na",
            "nb",
        ]
        self.set2_chars_8 = [
            "nc",
            "nd",
            "ne",
            "nf",
            "ng",
            "nh",
            "ni",
            "nj",
            "nk",
            "nl",
            "nm",
            "nn",
            "no",
            "np",
            "nq",
            "nr",
            "ns",
            "nt",
            "nu",
            "nv",
            "nw",
            "nx",
            "ny",
            "nz",
            "o_",
            "oa",
            "ob",
            "oc",
            "od",
            "oe",
            "of",
            "og",
            "oh",
            "oi",
            "oj",
            "ok",
            "ol",
            "om",
            "on",
            "oo",
            "op",
            "oq",
            "or",
            "os",
            "ot",
            "other",
            "ou",
            "ov",
            "ow",
            "ox",
            "oy",
            "oz",
            "p_",
        ]
        self.set2_chars_9 = [
            "pa",
            "pb",
            "pc",
            "pd",
            "pe",
            "pf",
            "pg",
            "ph",
            "pi",
            "pj",
            "pk",
            "pl",
            "pm",
            "pn",
            "po",
            "pp",
            "pq",
            "pr",
            "ps",
            "pt",
            "pu",
            "punctuation",
            "pv",
            "pw",
            "px",
            "py",
            "pz",
            "q_",
            "qa",
            "qb",
            "qc",
            "qd",
            "qe",
            "qf",
            "qg",
            "qh",
            "qi",
            "qj",
        ]
        self.set2_chars_10 = ["qk"]
        self.set2_chars_11 = [
            "ql",
            "qm",
            "qn",
            "qo",
            "qp",
            "qq",
            "qr",
            "qs",
            "qt",
            "qu",
            "qv",
            "qw",
            "qx",
            "qy",
        ]
        self.set2_chars_12 = [
            "qz",
            "r_",
            "ra",
            "rb",
            "rc",
            "rd",
            "re",
            "rf",
            "rg",
            "rh",
            "ri",
            "rj",
            "rk",
            "rl",
            "rm",
            "rn",
            "ro",
            "rp",
            "rq",
            "rr",
            "rs",
            "rt",
            "ru",
            "rv",
            "rw",
            "rx",
            "ry",
            "rz",
            "s_",
            "sa",
            "sb",
            "sc",
            "sd",
            "se",
            "sf",
            "sg",
            "sh",
            "si",
            "sj",
            "sk",
            "sl",
            "sm",
            "sn",
            "so",
            "sp",
            "sq",
            "sr",
            "ss",
            "st",
            "su",
            "sv",
            "sw",
            "sx",
            "sy",
        ]
        self.set2_chars_13 = [
            "sz",
            "t_",
            "ta",
            "tb",
            "tc",
            "td",
            "te",
            "tf",
            "tg",
            "th",
            "ti",
            "tj",
            "tk",
            "tl",
            "tm",
            "tn",
            "to",
            "tp",
            "tq",
            "tr",
            "ts",
            "tt",
            "tu",
            "tv",
            "tw",
            "tx",
            "ty",
            "tz",
            "u_",
            "ua",
            "ub",
            "uc",
            "ud",
            "ue",
            "uf",
            "ug",
            "uh",
            "ui",
            "uj",
            "uk",
            "ul",
            "um",
            "un",
            "uo",
            "up",
            "uq",
            "ur",
            "us",
            "ut",
            "uu",
            "uv",
            "uw",
            "ux",
            "uy",
        ]
        self.set2_chars_14 = [
            "uz",
            "v_",
            "va",
            "vb",
            "vc",
            "vd",
            "ve",
            "vf",
            "vg",
            "vh",
            "vi",
            "vj",
            "vk",
            "vl",
            "vm",
            "vn",
            "vo",
            "vp",
            "vq",
            "vr",
            "vs",
            "vt",
            "vu",
            "vv",
            "vw",
            "vx",
            "vy",
            "vz",
            "w_",
            "wa",
            "wb",
            "wc",
            "wd",
            "we",
            "wf",
            "wg",
            "wh",
            "wi",
            "wj",
            "wk",
            "wl",
            "wm",
            "wn",
            "wo",
            "wp",
            "wq",
            "wr",
            "ws",
            "wt",
            "wu",
            "wv",
            "ww",
            "wx",
            "wy",
        ]
        self.set2_chars_15 = [
            "wz",
            "x_",
            "xa",
            "xb",
            "xc",
            "xd",
            "xe",
            "xf",
            "xg",
            "xh",
            "xi",
            "xj",
            "xk",
            "xl",
            "xm",
            "xn",
            "xo",
            "xp",
            "xq",
            "xr",
            "xs",
            "xt",
            "xu",
            "xv",
            "xw",
            "xx",
            "xy",
            "xz",
            "y_",
            "ya",
            "yb",
            "yc",
            "yd",
            "ye",
            "yf",
            "yg",
            "yh",
            "yi",
            "yj",
            "yk",
            "yl",
            "ym",
            "yn",
            "yo",
            "yp",
            "yq",
            "yr",
            "ys",
            "yt",
            "yu",
            "yv",
            "yw",
            "yx",
            "yy",
        ]
        self.set2_chars_16 = [
            "yz",
            "z_",
            "za",
            "zb",
            "zc",
            "zd",
            "ze",
            "zf",
            "zg",
            "zh",
            "zi",
            "zj",
            "zk",
            "zl",
            "zm",
            "zn",
            "zo",
            "zp",
            "zq",
            "zr",
            "zs",
            "zt",
            "zu",
            "zv",
            "zw",
            "zx",
            "zy",
            "zz",
        ]

        self.set3_chars = [
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "_ADJ_",
            "_ADP_",
            "_ADV_",
            "_CONJ_",
            "_DET_",
            "_NOUN_",
            "_NUM_",
            "_PRON_",
            "_PRT_",
            "_VERB_",
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
            "g",
            "h",
            "i",
            "j",
            "k",
            "l",
            "m",
            "n",
            "o",
            "other",
            "p",
            "punctuation",
            "q",
            "r",
            "s",
            "t",
            "u",
            "v",
            "w",
            "x",
            "y",
            "z",
        ]

        DATA_LOCATION_KEY = NGramIndexer.DEFAULT_DATA_LOCATION_KEY
        if (
            os.system(
                "cd "
                + os.path.join(
                    os.path.expanduser("~"),
                    self.ngram_indexer.configurations[
                        NGramIndexer.DEFAULT_DEFAULTNGRAM_KEY
                    ][DATA_LOCATION_KEY],
                )
            )
            == 0
        ):
            os.chdir(os.path.expanduser("~"))
            self.ngram_data_path = (
                "./"
                + self.ngram_indexer.configurations[
                    NGramIndexer.DEFAULT_DEFAULTNGRAM_KEY
                ][DATA_LOCATION_KEY]
            )
        else:
            os.chdir(os.path.expanduser("~"))
            self.ngram_data_path = (
                "./"
                + self.ngram_indexer.configurations[NGramIndexer.DEFAULT_USERNGRAM_KEY][
                    DATA_LOCATION_KEY
                ]
            )

    """1-grams-------------------------------------------------------------------------------------------------------"""

    def stage_1(self):
        responses = []
        for char in self.set1_chars:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-1gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-1gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 1)

    """2-grams-------------------------------------------------------------------------------------------------------"""

    def stage_2(self):
        responses = []
        for char in self.set2_chars_1:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-2gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-1gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 2)

    def stage_3(self):
        responses = []
        for char in self.set2_chars_2:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-2gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-2gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 3)

    def stage_4(self):
        responses = []
        for char in self.set2_chars_3:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-2gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-2gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 4)

    def stage_5(self):
        responses = []
        for char in self.set2_chars_4:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-2gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-2gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 5)

    def stage_6(self):
        responses = []
        for char in self.set2_chars_5:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-2gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-2gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 6)

    def stage_7(self):
        responses = []
        for char in self.set2_chars_6:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-2gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-2gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 7)

    def stage_8(self):
        responses = []
        for char in self.set2_chars_7:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-2gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-2gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 8)

    def stage_9(self):
        responses = []
        for char in self.set2_chars_8:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-2gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-2gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 9)

    def stage_10(self):
        responses = []
        for char in self.set2_chars_9:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-2gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-2gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 10)

    def stage_11(self):
        responses = []
        for char in self.set2_chars_10 + self.set2_chars_11:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-2gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-2gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 11)

    def stage_12(self):
        responses = []
        for char in self.set2_chars_12:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-2gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-2gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 12)

    def stage_13(self):
        responses = []
        for char in self.set2_chars_13:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-2gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-2gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 13)

    def stage_14(self):
        responses = []
        for char in self.set2_chars_14:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-2gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-2gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 14)

    def stage_15(self):
        responses = []
        for char in self.set2_chars_15:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-2gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-2gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 15)

    def stage_16(self):
        responses = []
        for char in self.set2_chars_16:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-2gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-2gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 16)

    """3-grams-------------------------------------------------------------------------------------------------------"""

    def stage_17(self):
        responses = []
        for char in self.set2_chars_1:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-3gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-3gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 17)

    def stage_18(self):
        responses = []
        for char in self.set2_chars_2:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-3gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-3gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 18)

    def stage_19(self):
        responses = []
        for char in self.set2_chars_3:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-3gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-3gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 19)

    def stage_20(self):
        responses = []
        for char in self.set2_chars_4:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-3gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-3gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 20)

    def stage_21(self):
        responses = []
        for char in self.set2_chars_5:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-3gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-3gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 21)

    def stage_22(self):
        responses = []
        for char in self.set2_chars_6:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-3gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-3gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 22)

    def stage_23(self):
        responses = []
        for char in self.set2_chars_7:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-3gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-3gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 23)

    def stage_24(self):
        responses = []
        for char in self.set2_chars_8:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-3gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-3gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 24)

    def stage_25(self):
        responses = []
        for char in self.set2_chars_9:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-3gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-3gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 25)

    def stage_26(self):
        responses = []
        for char in self.set2_chars_10 + self.set2_chars_11:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-3gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-3gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 26)

    def stage_27(self):
        responses = []
        for char in self.set2_chars_12:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-3gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-3gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 27)

    def stage_28(self):
        responses = []
        for char in self.set2_chars_13:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-3gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-3gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 28)

    def stage_29(self):
        responses = []
        for char in self.set2_chars_14:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-3gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-3gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 29)

    def stage_30(self):
        responses = []
        for char in self.set2_chars_15:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-3gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-3gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 30)

    def stage_31(self):
        responses = []
        for char in self.set2_chars_16:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-3gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-3gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 31)

    """4-grams-------------------------------------------------------------------------------------------------------"""

    def stage_32(self):
        responses = []
        for char in self.set2_chars_1:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-4gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-4gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 32)

    def stage_33(self):
        responses = []
        for char in self.set2_chars_2:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-4gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-4gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 33)

    def stage_34(self):
        responses = []
        for char in self.set2_chars_3:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-4gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-4gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 34)

    def stage_35(self):
        responses = []
        for char in self.set2_chars_4:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-4gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-4gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 35)

    def stage_36(self):
        responses = []
        for char in self.set2_chars_5:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-4gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-4gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 36)

    def stage_37(self):
        responses = []
        for char in self.set2_chars_6:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-4gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-4gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 37)

    def stage_38(self):
        responses = []
        for char in self.set2_chars_7:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-4gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-4gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 38)

    def stage_39(self):
        responses = []
        for char in self.set2_chars_8:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-4gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-4gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 39)

    def stage_40(self):
        responses = []
        for char in self.set2_chars_9:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-4gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-4gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 40)

    def stage_41(self):
        responses = []
        for char in self.set2_chars_10 + self.set2_chars_11:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-4gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-4gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 41)

    def stage_42(self):
        responses = []
        for char in self.set2_chars_12:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-4gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-4gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 42)

    def stage_43(self):
        responses = []
        for char in self.set2_chars_13:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-4gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-4gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 43)

    def stage_44(self):
        responses = []
        for char in self.set2_chars_14:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-4gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-4gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 44)

    def stage_45(self):
        responses = []
        for char in self.set2_chars_15:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-4gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-4gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 45)

    def stage_46(self):
        responses = []
        for char in self.set2_chars_16:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-4gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-4gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 46)

    """5-grams-------------------------------------------------------------------------------------------------------"""

    def stage_47(self):
        responses = []
        for char in self.set2_chars_1:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-5gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-5gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 47)

    def stage_48(self):
        responses = []
        for char in self.set2_chars_2:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-5gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-5gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 48)

    def stage_49(self):
        responses = []
        for char in self.set2_chars_3:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-5gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-5gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 49)

    def stage_50(self):
        responses = []
        for char in self.set2_chars_4:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-5gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-5gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 50)

    def stage_51(self):
        responses = []
        for char in self.set2_chars_5:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-5gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-5gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 51)

    def stage_52(self):
        responses = []
        for char in self.set2_chars_6:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-5gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-5gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 52)

    def stage_53(self):
        responses = []
        for char in self.set2_chars_7:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-5gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-5gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 53)

    def stage_54(self):
        responses = []
        for char in self.set2_chars_8:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-5gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-5gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 54)

    def stage_55(self):
        responses = []
        for char in self.set2_chars_9:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-5gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-5gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 55)

    def stage_56(self):
        responses = []
        for char in self.set2_chars_11:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-5gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-5gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 56)

    def stage_57(self):
        responses = []
        for char in self.set2_chars_12:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-5gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-5gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 57)

    def stage_58(self):
        responses = []
        for char in self.set2_chars_13:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-5gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-5gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 58)

    def stage_59(self):
        responses = []
        for char in self.set2_chars_14:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-5gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-5gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 59)

    def stage_60(self):
        responses = []
        for char in self.set2_chars_15:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-5gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-5gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 60)

    def stage_61(self):
        responses = []
        for char in self.set2_chars_16:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-5gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-5gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 61)

    """dependencies--------------------------------------------------------------------------------------------------"""

    def stage_62(self):
        responses = []
        for char in self.set3_chars:
            file_url = (
                "https://storage.googleapis.com/books/ngrams/books/googlebooks-eng-all-0gram-20120701-"
                + char
                + ".gz"
            )
            file_name = "googlebooks-eng-all-0gram-20120701-" + char
            file(file_url, self.ngram_data_path)
            decompress_gz(self.ngram_data_path + "/" + file_name + ".gz")
            response_tuple = self.ngram_indexer.index_ngram_file_bulk(
                file_name, "stats"
            )
            response = list(response_tuple[1])
            self.monitoring_file(response, file_name)
            responses = responses + response

        self.monitoring_stage(responses, 62)

    def execute(self):
        time.sleep(2)
        self.stage_1()
        time.sleep(2)
        self.stage_2()
        time.sleep(2)
        self.stage_3()
        time.sleep(2)
        self.stage_4()
        time.sleep(2)
        self.stage_5()
        time.sleep(2)
        self.stage_6()
        time.sleep(2)
        self.stage_7()
        time.sleep(2)
        self.stage_8()
        time.sleep(2)
        self.stage_9()
        time.sleep(2)
        self.stage_10()
        time.sleep(2)
        self.stage_11()
        time.sleep(2)
        self.stage_12()
        time.sleep(2)
        self.stage_13()
        time.sleep(2)
        self.stage_14()
        time.sleep(2)
        self.stage_15()
        time.sleep(2)
        self.stage_16()
        time.sleep(2)
        self.stage_17()
        time.sleep(2)
        self.stage_18()
        time.sleep(2)
        self.stage_19()
        time.sleep(2)
        self.stage_20()
        time.sleep(2)
        self.stage_21()
        time.sleep(2)
        self.stage_22()
        time.sleep(2)
        self.stage_23()
        time.sleep(2)
        self.stage_24()
        time.sleep(2)
        self.stage_25()
        time.sleep(2)
        self.stage_26()
        time.sleep(2)
        self.stage_27()
        time.sleep(2)
        self.stage_28()
        time.sleep(2)
        self.stage_29()
        time.sleep(2)
        self.stage_30()
        time.sleep(2)
        self.stage_31()
        time.sleep(2)
        self.stage_32()
        time.sleep(2)
        self.stage_33()
        time.sleep(2)
        self.stage_34()
        time.sleep(2)
        self.stage_35()
        time.sleep(2)
        self.stage_36()
        time.sleep(2)
        self.stage_37()
        time.sleep(2)
        self.stage_38()
        time.sleep(2)
        self.stage_39()
        time.sleep(2)
        self.stage_40()
        time.sleep(2)
        self.stage_41()
        time.sleep(2)
        self.stage_42()
        time.sleep(2)
        self.stage_43()
        time.sleep(2)
        self.stage_44()
        time.sleep(2)
        self.stage_45()
        time.sleep(2)
        self.stage_46()
        time.sleep(2)
        self.stage_47()
        time.sleep(2)
        self.stage_48()
        time.sleep(2)
        self.stage_49()
        time.sleep(2)
        self.stage_50()
        time.sleep(2)
        self.stage_51()
        time.sleep(2)
        self.stage_52()
        time.sleep(2)
        self.stage_53()
        time.sleep(2)
        self.stage_54()
        time.sleep(2)
        self.stage_55()
        time.sleep(2)
        self.stage_56()
        time.sleep(2)
        self.stage_57()
        time.sleep(2)
        self.stage_58()
        time.sleep(2)
        self.stage_59()
        time.sleep(2)
        self.stage_60()
        time.sleep(2)
        self.stage_61()
        time.sleep(2)
        self.stage_62()
        time.sleep(2)

    def monitoring_file(self, response, file_name):
        if len(response) == 0:
            return
        else:
            content = (
                "Something is wrong with file "
                + file_name
                + ", file gave following responses\n\n"
                + str(response)
            )
            mail = smtplib.SMTP("smtp.gmail.com", 587)
            mail.ehlo()
            mail.starttls()
            mail.login("juan@mammut.io", "13692468$/")
            mail.sendmail("juan@mammut.io", "juan@mammut.io", content)
            mail.close()

    def monitoring_stage(self, responses, stage_num):
        if len(responses) == 0:
            content = (
                "Everything OK with stage "
                + str(stage_num)
                + "next stages will start in seconds!"
            )
            mail = smtplib.SMTP("smtp.gmail.com", 587)
            mail.ehlo()
            mail.starttls()
            mail.login("juan@mammut.io", "13692468$/")
            mail.sendmail("juan@mammut.io", "juan@mammut.io", content)
            mail.close()
        else:
            content = (
                "Something went wrong with "
                + stage_num
                + " file reports should have arrived already, "
                "please check your inbox"
            )
            mail = smtplib.SMTP("smtp.gmail.com", 587)
            mail.ehlo()
            mail.starttls()
            mail.login("juan@mammut.io", "13692468$/")
            mail.sendmail("juan@mammut.io", "juan@mammut.io", content)
            mail.close()
