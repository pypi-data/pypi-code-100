import json
import logging
import subprocess

from pathlib import Path
from typing import List, Literal, Union


log = logging.getLogger("enderturing")

_ffmpeg_defaults = ["ffmpeg", "-nostdin", "-loglevel", "quiet"]


def _exec_cmd(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if p.returncode != 0:
        raise RuntimeError(cmd[0], out, err)
    return out.decode("utf-8")


def get_num_channels(path: Path):
    """Gets number of audio channels in the file using ffprobe.

    Args:
        path: Path to audio file to get number of channels for.

    Returns:
        Number of audio channels in the file.
    """
    cmd = ["ffprobe", "-show_format", "-show_streams", "-of", "json", path]
    res = json.loads(_exec_cmd(cmd))
    num_channels = int(res["streams"][0]["channels"])
    log.debug("Identified %d channels in '%s'", num_channels, str(Path))
    return num_channels


def _get_ffmpeg_mono_file_cmd(path: Path, *, asr_sample_rate: int):
    cmd = [*_ffmpeg_defaults, "-i", str(path), "-ar", str(asr_sample_rate), "-ac", "1", "-f", "s16le", "-"]
    return cmd


def _get_ffmpeg_file_cmd_channels_list(path: Path, *, asr_sample_rate: int, channels: Union[List[int], int] = None):
    cmd = [*_ffmpeg_defaults, "-i", str(path)]
    if channels:
        dst = channels if isinstance(channels, list) else range(channels)
        for channel in dst:
            cmd.append("-map_channel")
            cmd.append(f"0.0.{channel}")
    cmd.extend(["-ar", str(asr_sample_rate), "-f", "s16le", "-"])
    return cmd


def _get_ffmpeg_join_files_cmd(files: List[Path], *, asr_sample_rate: int):
    cmd = _ffmpeg_defaults.copy()
    merge_filter = ""
    for idx, path in enumerate(files):
        cmd.append("-i")
        cmd.append(str(path))
        merge_filter += f"[{idx}:a]"
    merge_filter += f"amerge=inputs={len(files)}[a]"
    cmd.extend(["-filter_complex", merge_filter, "-map", "[a]", "-ar", str(asr_sample_rate), "-f", "s16le", "-"])
    return cmd, len(files)


def _get_ffmpeg_file_cmd(path: Path, sample_rate: int, channels: Union[List[int], int, Literal["all", "mono"]] = "all"):
    # FFMPEG Chan manipulation
    # https://trac.ffmpeg.org/wiki/AudioChannelManipulation

    if channels == "mono":
        asr_channels = 1
        cmd = _get_ffmpeg_mono_file_cmd(path, asr_sample_rate=sample_rate)
        return cmd, asr_channels

    detected_channels = get_num_channels(path)
    if channels == "all":
        asr_channels = detected_channels
        cmd = _get_ffmpeg_file_cmd_channels_list(path, asr_sample_rate=sample_rate)
        return cmd, asr_channels

    if isinstance(channels, list):
        valid_channels = [channel for channel in channels if channel < detected_channels]
        if len(valid_channels) < len(channels):
            log.warning(
                "Some values in `channels` are out of range, ignored %d provided values",
                len(channels) - len(valid_channels),
            )
        asr_channels = len(valid_channels)
        cmd = _get_ffmpeg_file_cmd_channels_list(path, asr_sample_rate=sample_rate, channels=valid_channels)
        return cmd, asr_channels

    if isinstance(channels, int):
        if channels > detected_channels:
            log.warning(
                "Requested %d channels for recognition, but file '%s' has %d channels, using lower value",
                channels,
            )
            asr_channels = detected_channels
        else:
            asr_channels = channels
        if asr_channels == detected_channels:
            cmd = _get_ffmpeg_file_cmd_channels_list(path, asr_sample_rate=sample_rate)
        else:
            cmd = _get_ffmpeg_file_cmd_channels_list(path, asr_sample_rate=sample_rate, channels=asr_channels)
        return cmd, asr_channels

    raise ValueError("Unsupported `channels` value")
