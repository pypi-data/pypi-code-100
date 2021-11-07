import ffmpeg, yaml, scipy.io.wavfile
from datetime import datetime, timedelta
from os import listdir, chdir, remove
from os.path import isfile, join, splitext, basename
from loguru import logger
from pprint import pprint, pformat
import pathlib, shutil
import os, glob, numpy
# import dualsoundsync.YaLTCdemodulation as YaLTCdemodulation
from . import YaLTCdemodulation
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

OUTPUT_DIR = 'dualsoundsync'
SPLIT_DIR = join(OUTPUT_DIR, 'split')
SYNCED_DIR = join(OUTPUT_DIR, 'synced')

def is_audio_only(probe_output):
    if not probe_output:
        return False
    streams = probe_output['streams']
    codecs = [stream['codec_type'] for stream in streams]
    return 'video' not in codecs and 'audio' in codecs

def split_channels(file):
    # and remove original
    silenced_opts = ["-loglevel", "quiet", "-nostats", "-hide_banner"]  
    # silenced_opts = [ ]  
    in1 = ffmpeg.input(file)
    file_basename, _ = splitext(file)
    L_chan_fn = file_basename + '_Lchan' + '.wav'
    R_chan_fn = file_basename + '_Rchan' + '.wav'
    out1 = in1.output(L_chan_fn, map_channel='0.0.0')
    out2 = in1.output(R_chan_fn, map_channel='0.0.01')
    ffmpeg.run([out1, out2.global_args(*silenced_opts)], overwrite_output=True)

def make_mono_files():
    for name in glob.glob(join(SPLIT_DIR,'**','*.wav'), recursive=True):
    # for name in glob.glob('media/**/*.wav', recursive=True):
        # print(name)
        pr = get_ffprobe(name)
        streams = pr['streams']
        audio_streams = [stream for stream in streams if stream['codec_type']=='audio']
        if len(audio_streams) > 1:
            raise Exception('multiple audio streams?')
        audio_stream = audio_streams[0]
        nb_of_audio_channel = audio_stream['channels']
        # print('chan: %s'%nb_of_audio_channel)
        if nb_of_audio_channel == 1:
            logger.info('%s is already mono'%basename(name))
            continue
        if nb_of_audio_channel == 2:
            logger.info('splitting %s in L and R channels'%basename(name))            
            split_channels(name)
            remove(name)

def get_ffprobe(fn):
    try:
        probe = ffmpeg.probe(fn)
    except:
        print('"%s" is not recognized by ffprobe'%fn)
        probe = None
    return probe

def is_video_with_audio(probe_output):
    if not probe_output:
        return False
    streams = probe_output['streams']
    codecs = [stream['codec_type'] for stream in streams]
    return 'video' in codecs and 'audio' in codecs

def is_audio_only(probe_output):
    if not probe_output:
        return False
    streams = probe_output['streams']
    codecs = [stream['codec_type'] for stream in streams]
    return 'video' not in codecs and 'audio' in codecs

def detach_AUDIO_VIDEO(file):
    silenced_opts = ["-loglevel", "quiet", "-nostats", "-hide_banner"]  
    # silenced_opts = [ ]  
    in1 = ffmpeg.input(file)
    file_basename, video_extension = splitext(file)
    detach_rep = join(SPLIT_DIR, file_basename)
    pathlib.Path(detach_rep).mkdir(parents=True, exist_ok=True)
    audio_fn = join(detach_rep, file_basename) + '_a' + '.wav'
    video_fn = join(detach_rep, file_basename) + '_v' + video_extension
    # out1 = in1.output(audio_fn, map='0:a', acodec='copy')
    out1 = in1.output(audio_fn, map='0:a')
    out2 = in1.output(video_fn, map='0:v', vcodec='copy')
    ffmpeg.run([out1, out2.global_args(*silenced_opts)], overwrite_output=True)
    # os.path.split audio channels if more than one



def crop_or_pad_wav_file(fn, n_samples_pad):
    # if n_samples_pad < 0, chop the begining
    # this rewrites the file
    fs, in_data = scipy.io.wavfile.read(fn)
    if n_samples_pad < 0:
        out_data = in_data[-n_samples_pad:]
    else:
        padding = numpy.zeros(n_samples_pad)
        out_data = numpy.hstack((padding, in_data))
    scipy.io.wavfile.write(fn, fs, out_data.astype(numpy.int16))

def build_yaml_files():
    wave_files = list(glob.glob(join(SPLIT_DIR, '**', '*.wav'), recursive=True))
    for i, name in enumerate(wave_files):
        print("%i of %i"%(i+1, len(wave_files)), end ="")
        logger.info('will fprobe %s'%name)
        pr = get_ffprobe(name)
        duration = pr['format']['duration'] # string, in sec
        streams = pr['streams']
        audio_streams = [stream for stream in streams if stream['codec_type']=='audio']
        if len(audio_streams) > 1:
            raise Exception('multiple audio streams?')
        audio_stream = audio_streams[0]
        nominal_sr = audio_stream['sample_rate']
        nb_of_audio_channel = audio_stream['channels']
        if nb_of_audio_channel == 1:
            time, effective_SR = YaLTCdemodulation.get_start_time(name)
            if time:
                print(': %s started at %s'%(basename(name), time))
                rep, _ = os.path.split(name)
                was_video = list(pathlib.Path(rep).rglob('*_v.*')) != []
                # print(was_video)
                origin = 'video' if was_video else 'audio'
                fn, _ = splitext(name)
                fn += '.yml'
                f = open(fn, "w")
                f.write("origin: '%s'\n"%origin)
                f.write("UTC-start-time: '%s'\n"%time)
                f.write("duration: %s #sec\n"%duration)
                f.write("nominal-audio-samplerate: %s #Hz\n"%nominal_sr)
                f.write("effective-audio-samplerate: %f #Hz\n"%effective_SR)
                f.close()
                remove(name)
                logger.info('wrote %s'%(basename(fn)))
            else:
                logger.info('%s start is unknown'%basename(name))
                print(': nope')
            continue
        if nb_of_audio_channel == 2:
            print('%s stereo, skipping...'%basename(name))
        continue

def join_audio_and_video(audio_filename, video_filename, out_fn):
    output_path = join(SYNCED_DIR, out_fn)
    print('%s'%output_path)
    # pathlib.Path(SYNCED_DIR).mkdir(parents=True, exist_ok=True)
    silenced_opts = ["-loglevel", "quiet", "-nostats", "-hide_banner"]
    (
    ffmpeg
    .input(video_filename)
    .output(output_path, shortest=None, vcodec='copy')
    # .global_args('-i', audio_filename)
    .global_args('-i', audio_filename, *silenced_opts)
    .overwrite_output()
    # .get_args()
    .run()
    )

def find_wav_from_yml_filename(yml_filename):
    (dirname, filename) = os.path.split(yml_filename)
    wav_pattern = join(dirname,'*.wav')
    globbed = glob.glob(wav_pattern)
    if len(globbed) != 1:
        raise Exception('more than one wave file')
    return globbed[0]

def find_video_from_yml_filename(yml_filename):
    (dirname, filename) = os.path.split(yml_filename)
    vid_pattern = join(dirname,'*_v.*')
    globbed = glob.glob(vid_pattern)
    if len(globbed) != 1:
        raise Exception('more than one wave file')
    return globbed[0]

def collect_yaml_files():
  yaml_files = []
  for name in glob.glob(join(SPLIT_DIR, '**', '*.yml'), recursive=True):
      # print(name)
      data = yaml.load(open(name), Loader=Loader)
      data['filename'] = name
      start = datetime.fromisoformat(data['UTC-start-time'])
      del data['UTC-start-time']
      end = start + timedelta(seconds=float(data['duration']))
      data['start'] = start
      data['end'] = end
      yaml_files.append(data)
  return yaml_files

def copy_audio(file):
    file_basename, _ = splitext(file)
    detach_rep = join(SPLIT_DIR, file_basename)
    pathlib.Path(detach_rep).mkdir(parents=True, exist_ok=True)
    shutil.copy2(file, detach_rep)


# if working_rep:
#     all_files_in_rep = [join(working_rep, f) for f in listdir(working_rep) if isfile(join(working_rep, f))]
# else:
#     all_files_in_rep = [f for f in listdir('.') if isfile(f)]


def mkdirs():
    pathlib.Path(SPLIT_DIR).mkdir(parents=True, exist_ok=True)
    pathlib.Path(SYNCED_DIR).mkdir(parents=True, exist_ok=True)


def detach():
    all_files_in_rep = [f for f in listdir('.') if isfile(f)]
    basenames = [splitext(fn)[0] for fn in all_files_in_rep]
    dup = set([elem for elem in basenames if basenames.count(elem) > 1])
    if dup:
        logger.error('two files with same name: %s'%dup)
        raise Exception
    # pathlib.Path(SPLIT_DIR).mkdir(parents=True, exist_ok=True)
    for fn in all_files_in_rep:
        probe = get_ffprobe(fn)
        if is_video_with_audio(probe):
            logger.debug('%s is video '%fn)
            detach_AUDIO_VIDEO(fn)
        if is_audio_only(probe):
            logger.debug('%s is audio '%fn)
            copy_audio(fn)


