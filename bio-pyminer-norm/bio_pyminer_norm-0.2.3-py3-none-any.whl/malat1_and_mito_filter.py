#!/usr/local/env python3
import seaborn as sns
from matplotlib import pyplot as plt
import pandas as pd


def get_individual_malat_mito_scatter(in_file, col_counts_df, col_sums_df, base_dir_dict):
    plt.clf()
    f, ax = plt.subplots(figsize=(6, 6))
    df = pd.DataFrame({"malat1_pcnt": col_counts_df[in_file],
                       "mito_pcnt": col_sums_df[in_file]})
    sns.jointplot(x="col_counts", y="col_sums", data=df, kind="kde")
    plt.savefig(base_dir_dict[in_file] + "/malat1_mito_percentages.png", dpi=600)
    plt.clf()
    return



def get_mal_mito_gene_dict(species):
    mal_mito_dict={}
    mal_mito_dict["mmusculus"]={"malat1":"ENSMUSG00000092341","mito":set(["ENSMUSG00000064336",
                "ENSMUSG00000064337",
                "ENSMUSG00000064338",
                "ENSMUSG00000064339",
                "ENSMUSG00000064340",
                "ENSMUSG00000064341",
                "ENSMUSG00000064342",
                "ENSMUSG00000064343",
                "ENSMUSG00000064344",
                "ENSMUSG00000064345",
                "ENSMUSG00000064346",
                "ENSMUSG00000064347",
                "ENSMUSG00000064348",
                "ENSMUSG00000064349",
                "ENSMUSG00000064350",
                "ENSMUSG00000064351",
                "ENSMUSG00000064352",
                "ENSMUSG00000064353",
                "ENSMUSG00000064354",
                "ENSMUSG00000064355",
                "ENSMUSG00000064356",
                "ENSMUSG00000064357",
                "ENSMUSG00000064358",
                "ENSMUSG00000064359",
                "ENSMUSG00000064360",
                "ENSMUSG00000064361",
                "ENSMUSG00000065947",
                "ENSMUSG00000064363",
                "ENSMUSG00000064364",
                "ENSMUSG00000064365",
                "ENSMUSG00000064366",
                "ENSMUSG00000064367",
                "ENSMUSG00000064368",
                "ENSMUSG00000064369",
                "ENSMUSG00000064370",
                "ENSMUSG00000064371",
                "ENSMUSG00000064372"])}
    mal_mito_dict["hsapiens"]={"malat1":"","mito":set(["ENSG00000210049",
                "ENSG00000211459",
                "ENSG00000210077",
                "ENSG00000210082",
                "ENSG00000209082",
                "ENSG00000198888",
                "ENSG00000210100",
                "ENSG00000210107",
                "ENSG00000210112",
                "ENSG00000198763",
                "ENSG00000210117",
                "ENSG00000210127",
                "ENSG00000210135",
                "ENSG00000210140",
                "ENSG00000210144",
                "ENSG00000198804",
                "ENSG00000210151",
                "ENSG00000210154",
                "ENSG00000198712",
                "ENSG00000210156",
                "ENSG00000228253",
                "ENSG00000198899",
                "ENSG00000198938",
                "ENSG00000210164",
                "ENSG00000198840",
                "ENSG00000210174",
                "ENSG00000212907",
                "ENSG00000198886",
                "ENSG00000210176",
                "ENSG00000210184",
                "ENSG00000210191",
                "ENSG00000198786",
                "ENSG00000198695",
                "ENSG00000210194",
                "ENSG00000198727",
                "ENSG00000210195",
                "ENSG00000210196"])}
    assert species in mal_mito_dict
    if species in mal_mito_dict:
        return(mal_mito_dict[species])
    else:
        return(None)


def get_mal_mito_idxs(genes, mal_mito_dict):
    mal_idx = None
    mito_idxs = []
    for i in range(len(genes)):
        if genes[i]==mal_mito_dict["malat1"]:
            mal_idx = i
        if genes[i] in mal_mito_dict["mito"]:
            mito_idxs.append(i)
    return(mal_idx, np.array(mito_idxs))


def plot_single_mal_mito(mal, mito, colsums, out_dir):
    plt.clf()
    df = pd.DataFrame({"percent_malat1":mal,"percent_mito":mito,"log_colsums":np.log10(colsums+1)})
    sns.jointplot(x="percent_malat1", y="percent_mito", data=df, kind="kde")
    cmap = sns.color_palette("flare", as_cmap=True)
    plt.scatter(df.percent_malat1, df.percent_mito, c=df.log_colsums, cmap="flare")#, data=df, kind="scatter", cmap="flare")
    plt.tight_layout()
    out_file = os.path.join(out_dir, "percent_malat1_mito.png")
    print(out_file)
    plt.savefig(out_file, dpi=600)
    return



def get_mal_mito_percent(mat, barcodes, genes, in_file, colsums, species="mmusculus"):
    mal_mito_dict = get_mal_mito_gene_dict(species)
    mal_idx, mito_idxs = get_mal_mito_idxs(genes, mal_mito_dict)
    if mal_idx is None:
        mal_percent=None
    else:
        mal_percent = mat[mal_idx,:]/colsums
    if mito_idxs is None:
        mito_percent = None
    else:
        mito_percent = np.sum(mat[mito_idxs,:], axis=0)/colsums
    return(np.array(mal_percent).squeeze(), np.array(mito_percent).squeeze())

