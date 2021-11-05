


from pyminer.common_functions import find_string_db_dir
from pyminer.cell_signals import subset_action_table


##
## First, find the right directory
stringdb_dir=find_string_db_dir(stringdb_dir)
## then id the right interaction file
if organism in organism_action_files:
    db_file = os.path.join(stringdb_dir,organism_action_files[organism])
## subset the action table for only these pathologic associated genes 
action_table, activation_dict, inhibition_dict, other_dict, all_included_bg = subset_action_table(receptor_or_secreted_list,db_file)
