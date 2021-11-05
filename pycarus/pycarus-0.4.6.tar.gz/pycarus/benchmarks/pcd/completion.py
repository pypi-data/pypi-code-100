from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import cast

import torch
from torch import Tensor

from pycarus.geometry.pcd import read_pcd
from pycarus.metrics.chamfer_distance import chamfer
from pycarus.metrics.emd_distance import emd
from pycarus.metrics.f_score import fscore
from pycarus.utils import progress_bar


def pcd_completion_evaluation(
    gt_dir: Path,
    pred_dir: Path,
    results_dir: Path,
    batch_size: int = 512,
    gpu: bool = True,
) -> None:
    """Evaluate point cloud completion results.

    The function requires the ground-truth clouds and the predicted ones to be
    organized in two separate directories with the same structure. Each directory
    must contain one sub-directory for each category and each subdirectory must
    contain one .ply file for each cloud. The function expects the name of the files
    in the "gt_dir" and "pred_dir" directories to be matching in order to perform
    the comparison.

    Four metrics are computed: the two Chamfer Distances proposed in the paper
    "Variational Relational Point Completion Network.", Earth Mover's Distance and F1 score.
    Results are saved into two files ("global_results.csv" and "single_results.csv")
    inside the given "result_dir" directory.

    Args:
        gt_dir: Directory with ground-truth clouds.
        pred_dir: Directory with predicted clouds.
        results_dir: Directory where the .csv files with the results will be saved.
        batch_size: The batch size to use for computing metrics.
        gpu: Whether to use gpu or not to compute metrics.

    Raises:
        ValueError: If one prediction is missing.
    """
    results_dir.mkdir(parents=True, exist_ok=True)

    single_results_file = results_dir / "single_results.csv"
    if single_results_file.exists():
        single_results_file.unlink()

    with open(single_results_file, "wt") as f:
        f.write("CATEGORY/NAME,CD_P,CD_T,EMD,F1-SCORE\n")

    cd_ps = defaultdict(list)
    cd_ts = defaultdict(list)
    emds = defaultdict(list)
    f1_scores = defaultdict(list)

    gt_files = []
    pred_files = []
    categories_dirs = [subdir for subdir in gt_dir.iterdir() if subdir.is_dir()]
    for category_dir in categories_dirs:
        for gt_file in category_dir.glob("*.ply"):
            gt_files.append(gt_file)
            pred_files.append(pred_dir / category_dir.name / gt_file.name)

    num_batches = len(gt_files) // batch_size
    num_batches = num_batches + 1 if len(gt_files) % batch_size != 0 else num_batches

    for batch in progress_bar(range(num_batches)):
        start = batch * batch_size
        end = start + batch_size
        gt_files_batch = gt_files[start:end]
        pred_files_batch = pred_files[start:end]

        gts = torch.stack([read_pcd(gt_file) for gt_file in gt_files_batch], dim=0)
        preds = torch.stack([read_pcd(pred_file) for pred_file in pred_files_batch], dim=0)

        if gpu:
            gts = gts.cuda()
            preds = preds.cuda()

        cds_pred_gt, cds_gt_pred = chamfer(preds, gts, squared=False)
        cds_pred_gt_sq, cds_gt_pred_sq = chamfer(preds, gts, squared=True)
        emds_, _ = emd(preds, gts, eps=0.004, iterations=3000, squared=False)
        f1s, _, _ = fscore(preds.cpu(), gts.cpu(), 0.01)

        for i, gt_file in enumerate(gt_files_batch):
            category = gt_file.parent.name
            shape_name = gt_file.stem

            cd_p = float(((cds_gt_pred[i] + cds_pred_gt[i]) / 2).item())
            cd_ps["all"].append(cd_p)
            cd_ps[category].append(cd_p)

            cd_t = float((cds_gt_pred_sq[i] + cds_pred_gt_sq[i]).item())
            cd_ts["all"].append(cd_t)
            cd_ts[category].append(cd_t)

            emd_ = float(emds_[i].item())
            emds["all"].append(emd_)
            emds[category].append(emd_)

            f1_score = float(cast(Tensor, f1s)[i].item())
            f1_scores["all"].append(f1_score)
            f1_scores[category].append(f1_score)

            with open(single_results_file, "at") as f:
                line = f"{category}/{shape_name},{cd_p:.8f},{cd_t:.8f},{emd_:.8f},{f1_score:.8f}\n"
                f.write(line)

    global_results_file = results_dir / "global_results.csv"
    if global_results_file.exists():
        global_results_file.unlink()

    with open(global_results_file, "wt") as f:
        f.write("CATEGORY,CD_P,CD_T,EMD,F1-SCORE\n")

    for category in sorted(cd_ps.keys()):
        if category != "all":
            m_cd_p = mean(cd_ps[category])
            m_cd_t = mean(cd_ts[category])
            m_emd_ = mean(emds[category])
            m_f1_score = mean(f1_scores[category])

            with open(global_results_file, "at") as f:
                f.write(f"{category},{m_cd_p:.8f},{m_cd_t:.8f},{m_emd_:.8f},{m_f1_score:.8f}\n")

    with open(global_results_file, "at") as f:
        f.write("\n\n")
        f.write(f"MEAN CD_P,{mean(cd_ps['all']):.8f}\n")
        f.write(f"MEAN CD_T,{mean(cd_ts['all']):.8f}\n")
        f.write(f"MEAN EMD,{mean(emds['all']):.8f}\n")
        f.write(f"MEAN F1 SCORE,{mean(f1_scores['all']):.8f}\n")
