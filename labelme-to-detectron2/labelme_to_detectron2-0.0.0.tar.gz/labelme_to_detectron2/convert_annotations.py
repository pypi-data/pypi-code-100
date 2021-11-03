import sys
import json
from pathlib import Path
from tqdm import tqdm

from labeleme_to_detectron2.convert_annotation import convert 

annotation_dir = Path(sys.argv[1])
labelme_annotations = annotation_dir.glob("*.json")
labelme_annotations = sorted([*labelme_annotations])

suffix = "d2"

for path in labelme_annotations:
    with open(path, "r") as f:
        ann = json.load(f)
        ann_d2 = convert(ann)
        
        out_path = path.with_suffix(f".{suffix}.json")
        with open(out_path, "w") as f:
            json.dump(ann_d2, f)