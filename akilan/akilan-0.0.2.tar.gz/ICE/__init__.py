from .src.prep import *
print(f"""
Welcome to the Image Classification Engine.
Note :
 - Working Directory : {os.getcwd()}
 - Dataset are stored in the 'DATASETS' folder.
 - Models are stored in the 'MODELS' folder.
 - Results are stored in the 'RESULTS' folder.
     
""")
if os.path.exists(os.path.join(os.getcwd(), 'DATASETS')):
    print(f"Dataset folder found at {os.path.join(os.getcwd(), 'DATASETS')}")
else:
    print(
        f"Dataset folder not found. Creating one at {os.path.join(os.getcwd(), 'DATASETS')}")
    os.mkdir(os.path.join(os.getcwd(), 'DATASETS'))

if os.path.exists(os.path.join(os.getcwd(), 'MODELS')):
    print(f"Model folder found at {os.path.join(os.getcwd(), 'MODELS')}")
else:
    print(
        f"Model folder not found. Creating one at {os.path.join(os.getcwd(), 'MODELS')}")
    os.mkdir(os.path.join(os.getcwd(), 'MODELS'))

if os.path.exists(os.path.join(os.getcwd(), 'RESULTS')):
    print(f"Results folder found at {os.path.join(os.getcwd(), 'RESULTS')}")
else:
    print(
        f"Results folder not found. Creating one at {os.path.join(os.getcwd(), 'RESULTS')}")
    os.mkdir(os.path.join(os.getcwd(), 'RESULTS'))
