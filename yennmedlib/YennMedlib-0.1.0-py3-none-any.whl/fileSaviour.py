import os
import numpy as np
import shutil


class FileSaviour:

    def __init__(self, input_folder=None, output_folder=None):
        self.inpu_folder = input_folder
        self.output_folder = output_folder

    def rename_suffix(self, suffix, suffixpos=None):
        filesname = os.listdir(self.inpu_folder)
        for i in filesname:
            if suffixpos is not None:
                j = i[:-7] + "." + suffix
            j = i.split('.')[0] + "." + suffix
            os.renames(os.path.join(self.inpu_folder, i), os.path.join(self.inpu_folder, j))

    def random_rename(self, suffix, txt_path='./'):
        """
        :param suffix: for example ".nii/.jpg"
        :param txt_path: path to save link txt file
        :return: shuffle files in the folder to [0.suffix, 1.suffix, ..., (num_files-1).suffix] and generate a txt file
        which correspond the renamed file to the original file name
        """
        """
        :param suffix: for example ".nii/.jpg"
        :return:  shuffle files in the folder to [0.suffix, 1.suffix, ..., (num_files-1).suffix] and generate a txt file
        which correspond the renamed file to the original file name
        """
        file_list = os.listdir(self.inpu_folder)
        file_num = len(file_list)
        random_num = np.random.choice(file_num, file_num, replace=False)
        link_txt = open(os.path.join(txt_path, 'renamed-original.txt'), mode='w')
        link_txt.writelines(["renamed", ",", "original", '\n'])
        for idx, i in enumerate(file_list):
            j = str(random_num[idx]) + "." + suffix
            link_txt.writelines([j, ',', i, '\n'])
            os.renames(os.path.join(self.inpu_folder, i), os.path.join(self.output_folder, j))
        link_txt.close()

    def copy_or_move_specific_file(self, identify_str, corm="copy"):
        """
        :param identify_str: the specific string to recognize
        :param corm: copy or move
        """
        assert corm == "copy" or corm == "move", "the argument is not \"copy\" or \"move\""
        files_name_list = os.listdir(self.inpu_folder)
        for f in files_name_list:
            f_path = os.path.join(self.inpu_folder, f)
            if identify_str in f:
                if corm == "move":
                    shutil.move(f_path, self.output_folder)
                elif corm == "copy":
                    shutil.copy(f_path, self.output_folder)

    def remove_specific_suffix_file(self, suffix):
        filenames = os.listdir(self.inpu_folder)
        for i in filenames:
            f_path = os.path.join(self.output_folder, i)
            if suffix in i:
                print(f_path)
                os.remove(f_path)