#!/usr/bin/env python3.7

# Author: Roujia Li
# email: Roujia.li@mail.utoronto.ca

# Making fasta reference for different input reference sequences

import pandas as pd
import os
#from legacy import # Padding sequences used
# Padding sequences are the same for human and yeast
# DB down tags
DB_Dn1 = "TCGATAGGTGCGTGTGAAGG"
DB_Dn2 = "CCTCAGTCGCTCAGTCAAG"
# DB up tags
DB_Up1 = "CCATACGAGCACATTACGGG"
DB_Up2 = "CTAACTCGCATACCTCTGATAAC"

# AD down tags
AD_Dn1 = "CTCCAGGGTTAGGCAGATG"
AD_Dn2 = "CAATCGCACTATCCCGCTG"
# AD up tags
AD_Up1 = "CCCTTAGAACCGAGAGTGTG"
AD_Up2 = "CACTCCGTTCGTCACTCAATAA"


def reverse_complement(seq):
    """
    return the reverse complement of seq
    """
    alt_map = {'ins':'0'}
    complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
    for k,v in alt_map.iteritems():
        seq = seq.replace(k,v)
    bases = list(seq)
    bases = reversed([complement.get(base,base) for base in bases])
    bases = ''.join(bases)
    for k,v in alt_map.iteritems():
        bases = bases.replace(v,k)
    return bases


def create_fasta(AD_summary, DB_summary, output_path, group_spec=False, AD="G0", DB="G0", mode=None, wnull=None):
    """
    Generate fasta file from summary
    See example_summary as templete
    """
    # set summary in py
    if group_spec: # make a group specific fasta file
        
        if not wnull:
            AD_summary = pd.read_csv(AD_summary, sep="\t")
            DB_summary = pd.read_csv(DB_summary, sep="\t")

            # select the group from AD and DB
            AD_summary = AD_summary[AD_summary.Group==AD]
            DB_summary = DB_summary[DB_summary.Group==DB]
            # fasta filename
            # h for human
            # change to y for yeast
            if mode == "human":
                f_ad = "h_AD_"+AD+".fasta" 
                f_db = "h_DB_"+DB+".fasta"

            if mode == "yeast":
                f_ad = "y_AD_"+AD+".fasta" 
                f_db = "y_DB_"+DB+".fasta"


        else:
            AD_summary = pd.read_csv(AD_summary, sep=",")
            DB_summary = pd.read_csv(DB_summary, sep=",")

            AD_summary = AD_summary[(AD_summary.Group==AD) | (AD_summary.Group=="null_setD")]
            DB_summary = DB_summary[(DB_summary.Group==DB) | (DB_summary.Group=="null_setD")]
            if mode == "human":
                f_ad = "h_AD_wnull_"+AD+".fasta" 
                f_db = "h_DB_wnull_"+DB+".fasta"
            if mode == "yeast":
                f_ad = "y_AD_wnull_"+AD+".fasta" 
                f_db = "y_DB_wnull_"+DB+".fasta"

    else:
        AD_summary = pd.read_csv(AD_summary, sep=",")
        DB_summary = pd.read_csv(DB_summary, sep=",")

        if mode == "human":
            # can't use G0 for human
            f_ad = "h_ADall.fasta"
            f_db = "h_DBall.fasta"
        if mode == "yeast":
            # can't use G0 for human
            f_ad = "y_ADall.fasta"
            f_db = "y_DBall.fasta"

    with open(os.path.join(output_path,f_ad), "w") as ad:
        # grep sequence and sequence name from summary file
        # >G1;YDL169C_BC-1;7;up
        # CCCTTAGAACCGAGAGTGTGGGTTAAATGGGTGAATTCAGGGATTCACTCCGTTCGTCACTCAATAA
        for index, row in AD_summary.iterrows():
            up_seq_name = ">"+row.Group+";"+str(row.Locus)+";"+str(row.Index)+";AD;"+"up"
            ad.write(up_seq_name+"\n")
            ad.write(AD_Up1 + row.UpTag_Sequence + AD_Up2 + "\n") # add padding sequences
            dn_seq_name = ">"+row.Group+";"+str(row.Locus)+";"+str(row.Index)+";AD;"+"dn"
            ad.write(dn_seq_name+"\n")
            
            if mode == "human": # for human AD barcode, take the RC
                rc = reverse_complement(row.DnTag_Sequence)
                ad.write(AD_Dn1 + rc + AD_Dn2 + "\n")
            else:
                ad.write(AD_Dn1 + row.DnTag_Sequence + AD_Dn2 + "\n")

    DB_summary = DB_summary.dropna(how="all")
    print(DB_summary)
    with open(os.path.join(output_path, f_db), "w") as db:
            
        for index, row in DB_summary.iterrows():
            up_seq_name = ">"+str(row.Group)+";"+str(row.Locus)+";"+str(row.Index)+";DB;"+"up"
            db.write(up_seq_name+"\n")
            db.write(DB_Up1 + row.UpTag_Sequence + DB_Up2 + "\n")

            dn_seq_name = ">"+str(row.Group)+";"+str(row.Locus)+";"+str(row.Index)+";DB;"+"dn"
            db.write(dn_seq_name+"\n")
            db.write(DB_Dn1 + row.DnTag_Sequence + DB_Dn2 + "\n")

# make fasta files for virus collection
def create_fasta_virus(vADNC, vAD2u, vDBNC, vADall, output_path):
    """
    create fasta reference for these three sets of barcode
    """
    vADNC_df = pd.read_csv(vADNC)
    vADNC_fasta = "v_ADNC.fasta"

    with open(os.path.join(output_path,vADNC_fasta), "w") as adnc:
        # grep sequence and sequence name from summary file
        # >ADNC;NSP2;up
        # CCCTTAGAACCGAGAGTGTGGGTTAAATGGGTGAATTCAGGGATTCACTCCGTTCGTCACTCAATAA
        for index, row in vADNC_df.iterrows():
            up_seq_name = ">ADNC;"+str(row.ORF)+";"+"up"
            adnc.write(up_seq_name+"\n")
            adnc.write(AD_Up1 + row.UP + AD_Up2 + "\n") # add padding sequences
            dn_seq_name = ">ADNC;"+str(row.ORF)+";"+"dn"
            adnc.write(dn_seq_name+"\n")
            adnc.write(AD_Dn1 + row.DN + AD_Dn2 + "\n")
    
    vAD2u_df = pd.read_csv(vAD2u)
    vAD2u_fasta = "v_AD2u.fasta"

    with open(os.path.join(output_path, vAD2u_fasta), "w") as ad2u:
            
        for index, row in vAD2u_df.iterrows():
            up_seq_name = ">AD2u;"+str(row.ORF)+";"+"up"
            ad2u.write(up_seq_name+"\n")
            ad2u.write(AD_Up1 + row.UP + AD_Up2 + "\n")

            dn_seq_name = ">AD2u;"+str(row.ORF)+";"+"dn"
            ad2u.write(dn_seq_name+"\n")
            ad2u.write(AD_Dn1 + row.DN + AD_Dn2 + "\n")

    vADall_df = pd.read_csv(vADall)
    vADall_fasta = "v_ADall.fasta"

    with open(os.path.join(output_path, vADall_fasta), "w") as adall:

        for index, row in vADall_df.iterrows():
            up_seq_name = ">ADall;" + str(row.ORF) + ";" + "up"
            adall.write(up_seq_name + "\n")
            adall.write(AD_Up1 + row.UP + AD_Up2 + "\n")

            dn_seq_name = ">ADall;" + str(row.ORF) + ";" + "dn"
            adall.write(dn_seq_name + "\n")
            adall.write(AD_Dn1 + row.DN + AD_Dn2 + "\n")

    vDBNC_df = pd.read_csv(vDBNC)
    vDBNC_fasta = "v_DBNC.fasta"
 
    with open(os.path.join(output_path, vDBNC_fasta), "w") as dbnc:
            
        for index, row in vDBNC_df.iterrows():
            up_seq_name = ">DBNC;"+str(row.ORF)+";"+"up"
            dbnc.write(up_seq_name+"\n")
            dbnc.write(DB_Up1 + row.UP + DB_Up2 + "\n")

            dn_seq_name = ">DBNC;"+str(row.ORF)+";"+"dn"
            dbnc.write(dn_seq_name+"\n")
            dbnc.write(DB_Dn1 + row.DN + DB_Dn2 + "\n")

# Modified version to make fasta files for all yeast ORFs with null. 
# for both AD and DB
def create_fasta_all_yeast(AD_summary, DB_summary, output_path):
    AD_summary = pd.read_csv(AD_summary)
    DB_summary = pd.read_csv(DB_summary)
    
    f_ad = "y_AD_withnull_all.fasta"
    f_db = "y_DB_withnull_all.fasta"
    with open(os.path.join(output_path,f_ad), "w") as ad:
        for index, row in AD_summary.iterrows():
            up_seq_name = ">"+row.Group+";"+row.Locus+";"+str(row.Index)+";"+"up"
            ad.write(up_seq_name+"\n")
            ad.write(AD_Up1 + row.UpTag_Sequence + AD_Up2 + "\n") # add padding sequences
            dn_seq_name = ">"+row.Group+";"+row.Locus+";"+str(row.Index)+";"+"dn"
            ad.write(dn_seq_name+"\n")
            ad.write(AD_Dn1 + row.DnTag_Sequence + AD_Dn2 + "\n")

    with open(os.path.join(output_path, f_db), "w") as db:
        for index, row in DB_summary.iterrows():
            up_seq_name = ">"+row.Group+";"+row.Locus+";"+str(row.Index)+";"+"up"
            db.write(up_seq_name+"\n")
            db.write(DB_Up1 + row.UpTag_Sequence + DB_Up2 + "\n")
            dn_seq_name = ">"+row.Group+";"+row.Locus+";"+str(row.Index)+";"+"dn"
            db.write(dn_seq_name+"\n")
            db.write(DB_Dn1 + row.DnTag_Sequence + DB_Dn2 + "\n")


# Modified version to make fasta files for Miha's ORFs. 
def create_fasta_miha(AD_summary, DB_summary, output_path):
    AD_summary = pd.read_table(AD_summary, sep="\t")
    DB_summary = pd.read_table(DB_summary, sep="\t")
    mihas_AD = AD_summary[AD_summary.Plate.str.contains("Miha")]
    mihas_DB = DB_summary[DB_summary.Plate.str.contains("Miha")]
    
    f_ad = "y_AD_M.fasta"
    f_db = "y_DB_M.fasta"
    
    with open(os.path.join(output_path,f_ad), "w") as ad:
        for index, row in mihas_AD.iterrows():
            up_seq_name = ">"+row.Group+";"+row.Locus+";"+str(row.Index)+";"+"up"
            ad.write(up_seq_name+"\n")
            ad.write(AD_Up1 + row.UpTag_Sequence + AD_Up2 + "\n") # add padding sequences
            dn_seq_name = ">"+row.Group+";"+row.Locus+";"+str(row.Index)+";"+"dn"
            ad.write(dn_seq_name+"\n")
            ad.write(AD_Dn1 + row.DnTag_Sequence + AD_Dn2 + "\n")

    with open(os.path.join(output_path, f_db), "w") as db:
        for index, row in mihas_DB.iterrows():
            up_seq_name = ">"+row.Group+";"+row.Locus+";"+str(row.Index)+";"+"up"
            db.write(up_seq_name+"\n")
            db.write(DB_Up1 + row.UpTag_Sequence + DB_Up2 + "\n")
            dn_seq_name = ">"+row.Group+";"+row.Locus+";"+str(row.Index)+";"+"dn"
            db.write(dn_seq_name+"\n")
            db.write(DB_Dn1 + row.DnTag_Sequence + DB_Dn2 + "\n")

# make fasta files for hedgy collection
def create_fasta_hedgy(DB_summary, output_path):
    """
    For the hEdgy project, the BC for the AD side is
    """
    db_hedgy_df = pd.read_csv(DB_summary)
    f_db = os.path.join(output_path, "h_hedgy.fasta")

    with open(f_db, "w") as db:
        for index, row in db_hedgy_df.iterrows():
            up_seq_name = ">"+row.Plate+";"+row["Locus"]+";"+"up"
            db.write(up_seq_name+"\n")
            db.write(DB_Up1 + row.UpTag_Sequence + DB_Up2 + "\n") # add padding sequences

            dn_seq_name = ">"+row.Plate+";"+row["Locus"]+";"+"dn"
            db.write(dn_seq_name+"\n")
            db.write(DB_Dn1 + row.DnTag_Sequence + DB_Dn2 + "\n")


def build_index(fasta_file, output_dir):
    """
    Bowtie build for fasta_file
    """
    basename = os.path.basename(fasta_file).split(".")[0]
    #print basename
    cmd = "bowtie2-build "+fasta_file+" "+os.path.join(output_dir,basename)
    #print cmd
    os.system(cmd)


def main(mode="n/a", null=False):
    if mode == "human": 
        AD_summary = "/home/rothlab/rli/02_dev/08_bfg_y2h/summary/20180927_bhORFeome_AD_RL.csv"
        DB_summary = "/home/rothlab/rli/02_dev/08_bfg_y2h/summary/20180927_bhORFeome_DB_RL.csv"
        ref_path = "/home/rothlab/rli/02_dev/08_bfg_y2h/reference/h_ref/"
    if mode == "yeast":
        AD_summary = "/home/rothlab/rli/02_dev/08_bfg_y2h/summary/20180627_byORFeome_AD.csv"
        DB_summary = "/home/rothlab/rli/02_dev/08_bfg_y2h/summary/20180627_byORFeome_DB_AA.csv"
        ref_path = "/home/rothlab/rli/02_dev/08_bfg_y2h/reference/y_ref/"

    # set for our experiment 
    # AD G1-4
    # DB G1-4
    n = 5
    if mode == "human":
        n = 11

    for i in range(1,n):
        if i < 10:
            create_fasta(AD_summary, DB_summary, ref_path, group_spec=True, AD="G"+str(i), DB="G"+str(i), mode=mode, null=null)

        else:
            create_fasta(AD_summary, DB_summary, ref_path, group_spec=True, AD="G"+str(i), DB="G"+str(i), mode=mode)

    # bowtie build
    list_fasta = os.listdir(ref_path)
    for fasta in list_fasta:
        build_index(os.path.join(ref_path, fasta), ref_path)


def create_fasta_yeast_LAgag(LAnull_file, output_path):
    """
    Build AD null + AD LA gag
    Build DB null + DB LA gag
    """
    
    la_df = pd.read_csv(LAnull_file)

    fdb = os.path.join(output_path, "DBgag.fasta")
    fad = os.path.join(output_path, "ADgag.fasta")
    with open(fdb, "w") as db:
        with open(fad, "w") as ad:
            for index, row in la_df.iterrows():
                up_seq_name = row.Sample+";"+row["96_Well"]+";"+"up"
                dn_seq_name = row.Sample+";"+row["96_Well"]+";"+"dn"

                if "AD" in up_seq_name:
                    ad.write(f">AD;{up_seq_name}"+"\n")
                    ad.write(AD_Up1 + row.UpTag + AD_Up2 + "\n") # add padding sequences

                    ad.write(f">AD;{dn_seq_name}"+"\n")
                    ad.write(AD_Dn1 + row.DownTag + AD_Dn2 + "\n")

                if "DB" in up_seq_name:
                    db.write(f">DB;{up_seq_name}"+"\n")
                    db.write(DB_Up1 + row.UpTag + DB_Up2 + "\n") # add padding sequences

                    db.write(f">DB;{dn_seq_name}"+"\n")
                    db.write(DB_Dn1 + row.DownTag + DB_Dn2 + "\n")


def v_main():

    vADNC = "/home/rothlab/rli/02_dev/08_bfg_y2h/summary/vADNC_withNull.csv"
    vAD2u = "/home/rothlab/rli/02_dev/08_bfg_y2h/summary/vAD2u_withNull.csv"
    vADall = "/home/rothlab/rli/02_dev/08_bfg_y2h/summary/vADall_withNull.csv"
    vDBNC = "/home/rothlab/rli/02_dev/08_bfg_y2h/summary/vDBNC_withNull.csv"
    output_path = "/home/rothlab/rli/02_dev/08_bfg_y2h/reference/v_ref/"
    create_fasta_virus(vADNC, vAD2u, vDBNC, vADall, output_path)


if __name__ == "__main__":
    #hdegy_db = "/home/rothlab/rli/02_dev/08_bfg_y2h/summary/20201014_hEDGY_Screen1_ORF_BC_list.csv"
    #output_path = "/home/rothlab/rli/02_dev/08_bfg_y2h/reference/h_hedgy/"
    #create_fasta_hedgy(hdegy_db, output_path)
    #main(mode="yeast",null=True)
    #v_main()
    # ADsum = "/home/rothlab/rli/02_dev/08_bfg_y2h/summary/20180927_bhORFeome_AD_RL_withNull.csv"
    # DBsum = "/home/rothlab/rli/02_dev/08_bfg_y2h/summary/20180927_bhORFeome_DB_RL_withNull.csv"
    # output_path = "/home/rothlab/rli/02_dev/08_bfg_y2h/reference/hv_ref/"
    #
    # #create_fasta(ADsum, DBsum, output_path, group_spec=False, AD="G0", DB="G0", mode="human", wnull=True)
    
    ADyeast_sum = "/home/rothlab/rli/02_dev/08_bfg_y2h/summary/20180927_byORFeome_AD_withNCnull.csv"
    DByeast_sum = "/home/rothlab/rli/02_dev/08_bfg_y2h/summary/20180927_byORFeome_DB_AA_withNCnull.csv"

    output_path = "/home/rothlab/rli/02_dev/08_bfg_y2h/bfg_data/reference/y_ref/"
    # LAgag and null file 
    LAnull_file = "/home/rothlab/rli/02_dev/08_bfg_y2h/bfg_data/summary/LAgag_and_Null_barcodes_2021_01_21.csv"
    #output_LA = "/home/rothlab/rli/02_dev/08_bfg_y2h/reference/yeast_LAnull/"
    #create_fasta_all_yeast(ADyeast_sum, DByeast_sum, output_path)
    create_fasta_yeast_LAgag(LAnull_file, output_path)

