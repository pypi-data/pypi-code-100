import glob
import shutil
import os


# RSM : Recursive Search & Move
def rsm(target_dir, outdir):
    """
    Does a recursive search in the @target_dir and then make a copy of all
    the files found directly into the @outdir.
    """
    pathname = target_dir + "/**/*.dcm"
    files = glob.glob(pathname, recursive=True)

    count = 0
    for file in files:
        shutil.copy2(file, os.path.join(outdir, f"dicom_{str(count)}.dcm"))
        count += 1

    print("Aucun fichier DICOM n'a été trouvé.") if not count else None
