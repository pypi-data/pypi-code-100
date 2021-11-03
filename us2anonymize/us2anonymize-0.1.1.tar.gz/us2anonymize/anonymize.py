import argparse
import itertools
import math
import os
import sys
import time
from pathlib import Path

import cv2
import numpy as np
import pydicom
from pydicom import uid
from pydicom.encaps import encapsulate
from pydicom.pixel_data_handlers import apply_color_lut
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


def is_video(img=None, shape=None):
    shape = shape or (isinstance(img, np.ndarray) and img.shape)
    return shape and (len(shape) == 4 or (len(shape) == 3 and shape[-1] > 4))


def ybr_to_rgb(img):
    return cv2.cvtColor(img, cv2.COLOR_YCR_CB2BGR)


def blank_top_bar(media, regions):
    video = is_video(media)
    image = np.mean(media, axis=0) if video else media
    new_image = np.mean(image[..., :3], axis=-1) if 3 <= image.shape[-1] <= 4 else image
    binary_image = (new_image > 2).astype('uint8')
    h = int(binary_image.shape[0] * 0.2)
    sum_pixel = np.sum(binary_image[:h, :], axis=1)
    top_bar = np.where(sum_pixel > (binary_image.shape[0] * 0.88))
    top_bar_bottom = 0
    if len(top_bar[0]) != 0:
        new_image[top_bar, :] = 0
        image[top_bar, :] = 0
        top_bar_bottom = top_bar[0][-1] + 1
    top_bar_bottom = max(top_bar_bottom, 40)
    mask = np.ones_like(media[0] if video else media)
    mask[:top_bar_bottom] = 0
    for region in regions:
        xo, xn = region.RegionLocationMinX0, region.RegionLocationMaxX1
        yo, yn = region.RegionLocationMinY0, region.RegionLocationMaxY1
        mask[yo:yn, xo:xn] = 1
    media *= mask


def parse_dicom_pixel(dicom):
    px = dicom.pixel_array
    pi = dicom.PhotometricInterpretation
    dicom.PhotometricInterpretation = 'RGB'
    if pi in ['YBR_FULL', 'YBR_FULL_422']:
        px = np.asarray([ybr_to_rgb(img) for img in px]) if is_video(px) else ybr_to_rgb(px)
    elif pi in ['PALETTE COLOR']:
        px = (apply_color_lut(px, dicom) // 255).astype('uint8')
    else:
        dicom.PhotometricInterpretation = pi
    blank_top_bar(px, getattr(dicom, "SequenceOfUltrasoundRegions", []))
    return px


def ensure_even(stream):
    # Very important for some viewers
    if len(stream) % 2:
        return stream + b"\x00"
    return stream


def person_data_callback(ds, e):
    if e.VR == "PN" or e.tag == (0x0010, 0x0030):
        del ds[e.tag]


def write_dicom(src, out):
    # Populate required values for file meta information
    ds = pydicom.dcmread(src)
    ds.remove_private_tags()
    ds.walk(person_data_callback)
    media = parse_dicom_pixel(ds)
    video = is_video(media)
    ds.file_meta.TransferSyntaxUID = uid.JPEGExtended

    ds.is_little_endian = True
    ds.is_implicit_VR = False

    ds.BitsStored = 8
    ds.BitsAllocated = 8
    ds.HighBit = 7

    ds.Rows, ds.Columns, ds.SamplesPerPixel = media.shape[video:]
    if video:
        ds.StartTrim = 1
        ds.StopTrim = ds.NumberOfFrames = media.shape[0] if video else 1
        ds.CineRate = ds.RecommendedDisplayFrameRate = 63
        ds.FrameTime = 1000 / ds.CineRate
        ds.ActualFrameDuration = math.ceil(1000 / ds.CineRate)
        ds.PreferredPlaybackSequencing = 0
        ds.FrameDelay = 0
    ds.PhotometricInterpretation = "YBR_FULL"
    ds.PixelData = encapsulate([ensure_even(cv2.imencode('.jpg', img)[1].tobytes())
                                for img in (media if video else [media])])
    ds['PixelData'].is_undefined_length = True
    out.parent.mkdir(exist_ok=True, parents=True)
    ds.save_as(out.with_suffix(".dcm"), write_like_original=True)


def handle_path(src, dst, path, i, n=None, overwrite=False):
    rel = path.relative_to(src)
    out = (dst / rel).with_suffix(".dcm")
    print(f"[ {str(i + 1).zfill(len(str(n or 0)))}{' / ' + str(n) if n else ''} ] {rel} ", end='')
    try:
        if overwrite or not out.is_file():
            write_dicom(path, dst / rel)
        print(f"-> {os.path.abspath(out)} ✓")
    except Exception as exc:
        print(f'✗ - {exc}')


class Handler(FileSystemEventHandler):
    def __init__(self, args, i=0, *vargs, **kwargs):
        self.src = args.src
        self.dst = args.dst
        self.cnt = itertools.count(i)
        super().__init__(*vargs, **kwargs)

    def on_created(self, event):
        handle_path(self.src, self.dst, Path(event.src_path), next(self.cnt))

    def on_moved(self, event):
        return self.on_created(event)

    def on_modified(self, event):
        return self.on_created(event)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "src", type=Path, help="The folder to anonymize")
    parser.add_argument(
        "--dst", help="The output folder for the anonymized DICOM, defaults to src folder suffixed with '_anonymized'")
    parser.add_argument(
        "--watch", action="store_true", help="Watch the src folder for changes")
    parser.add_argument(
        "--overwrite", action="store_true", help="Overwrite files in the output folder")
    args = parser.parse_args(sys.argv[1:])
    src = args.src
    args.dst = Path(args.dst or src.parent / f"{src.stem}_anonymized")
    paths = [src] if src.is_file() else list(src.rglob("*"))
    n = len(paths)
    i = -1
    for i, path in enumerate(paths):
        handle_path(src, args.dst, path, i, n)
    if args.watch:
        src.mkdir(exist_ok=True, parents=True)
        event_handler = Handler(args, i + 1)
        observer = Observer()
        try:
            observer.schedule(event_handler, src, recursive=True)
            observer.start()
            print(f"watching folder {os.path.abspath(src)}")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
            observer.join()
