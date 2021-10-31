import os 
from pydub import AudioSegment
import shutil

class AudioFileConverter:
    def __init__(self):
        return
    
    def convert_or_copy_files(self, directory_with_files):
        initial_working_directory = os.getcwd()
        
        output_directory = self._create_output_directory(directory_with_files)
        
        files_to_convert = self._read_in_files_to_convert(directory_with_files, output_directory)
        
        os.chdir(output_directory)
        for file in files_to_convert:
            if(self._is_a_wav_file(file.name)):
                self._copy_file(file, output_directory)
            else:
                self._convert_file_to_wav(file)
                
        os.chdir(initial_working_directory)
        return output_directory
    
    def _create_output_directory(self, directory_with_files):
        output_directory = directory_with_files + "\\" + 'wav_files'
        os.makedirs(output_directory)
        return output_directory
    
    def _read_in_files_to_convert(self, directory_with_files, output_directory_real_path):
        files = []
        output_directory = self._get_last_token(output_directory_real_path, '\\')
        for entry in os.scandir(directory_with_files):
            if entry.name != output_directory:
                files.append(entry)
        return files
    
    def _is_a_wav_file(self, file_name):
        return (".wav" in file_name)
    
    def _copy_file(self, file, output_directory):
        shutil.copy2(os.path.realpath(file), output_directory)
        return
    
    def _convert_file_to_wav(self, file):
        export_to_wav = AudioSegment.from_mp3(os.path.realpath(file))
        export_to_wav.export(self._get_new_file_name(file.name), format="wav")
        return
    
    def _get_new_file_name(self, file_name):
        return file_name.rstrip(self._get_last_token(file_name, '.')) + 'wav'
    
    def _get_last_token(self, string, substring_to_split_on):
        return string.rsplit(substring_to_split_on, 1)[1]