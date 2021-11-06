# -*- coding: utf-8 -*-

import sys, os, math
from loguru import logger
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from datetime import datetime, timezone, timedelta
import numpy as np
from rich.console import Console
import argparse
from scipy.signal import hilbert
import inspect
from scipy.signal import savgol_filter
import matplotlib.patches as patches
import ffmpeg
import matplotlib.transforms as transforms

plotting = False
INTERACTIVE = True
silence_zone_signal_ratio = 0.2 # for detecting silent portion of the second
MORE_THAN_A_SECOND = 1.1
F1 = 612.04 # Hertz 
F2 = 1156.07 # Hz , both from SAMD21 code
SYMBOL_LENGTH = 14.705 # ms, from FSKfreqCalculator.py
N_SYMBOLS_SAMD21 = 34 # including sync pulse, from arduino code


logger.remove()
logger.add("out.txt", backtrace=True, diagnose=True)  # Caution, may leak sensitive data in prod
# logger.add(sys.stdout, level="INFO")
# logger.add(sys.stdout, level="DEBUG")


console = Console()

__version__ = "1.0a1"

def horizontal_marker(ax, y_data, *args, **kwargs):
    trans_ydat_xnorm = transforms.blended_transform_factory(ax.transAxes, ax.transData)
    ax.hlines(y=y_data, xmin=0, xmax=1, transform=trans_ydat_xnorm,  *args, **kwargs)

def vert_marker(ax, x_data, *args, **kwargs):
    trans_ynorm_xdata = transforms.blended_transform_factory(ax.transAxes, ax.transData)
    ax.vlines(x=x_data, ymin=0, ymax=1, transform=trans_ynorm_xdata,  *args, **kwargs)

def to_precision(x,p):
    """
    returns a string representation of x formatted with a precision of p

    Based on the webkit javascript implementation taken from here:
    https://code.google.com/p/webkit-mirror/source/browse/JavaScriptCore/kjs/number_object.cpp
    """
    x = float(x)
    if x == 0.:
        return "0." + "0"*(p-1)
    out = []
    if x < 0:
        out.append("-")
        x = -x
    e = int(math.log10(x))
    tens = math.pow(10, e - p + 1)
    n = math.floor(x/tens)
    if n < math.pow(10, p - 1):
        e = e -1
        tens = math.pow(10, e - p+1)
        n = math.floor(x / tens)
    if abs((n + 1.) * tens - x) <= abs(n * tens -x):
        n = n + 1
    if n >= math.pow(10,p):
        n = n / 10.
        e = e + 1
    m = "%.*g" % (p, n)
    if e < -2 or e >= p:
        out.append(m[0])
        if p > 1:
            out.append(".")
            out.extend(m[1:p])
        out.append('e')
        if e > 0:
            out.append("+")
        out.append(str(e))
    elif e == (p -1):
        out.append(m)
    elif e >= 0:
        out.append(m[:e+1])
        if e+1 < len(m):
            out.append(".")
            out.extend(m[e+1:])
    else:
        out.append("0.")
        out.extend(["0"]*-(e+1))
        out.append(m)

    return "".join(out)

def get_envelope(a):
    return savgol_filter(np.abs(hilbert(a)), 15, 3)

def sliding_mean(data):
    window_width = int(0.5*48000)
    means = np.convolve(data, np.ones(window_width,dtype=int),'valid')/window_width
    start = int(window_width/2)
    x = range(start, len(means) + start)
    return x, means

def frame_info():
    callerframerecord = inspect.stack()[1]
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)
    attributes_names = 'filename function lineno'.split()
    attr_vals = [getattr(info, att) for att in attributes_names]
    filename, fct, fileNo = attr_vals
    filename = os.path.basename(filename)
    return '%s line %i %s()'%(filename, fileNo, fct)

def analyse_silence(sound_data, samplerate):
    silence_width_for_determining_threshold = 0.9 # relative to whole 0.5 sec silent segment
    def sample(time):
        return time*samplerate
    envelope = get_envelope(sound_data)
    whole_signal_mean = envelope.mean() # including silent 0.5 sec zone
    # whole_signal_mean = whole_signal_mean * 0.65 # tweak
    x_sliding_window, sliding_mean_values = sliding_mean(envelope)
    min_convolution = x_sliding_window[np.argmin(sliding_mean_values)]
    start_silent_zone = int(min_convolution - sample(0.25*silence_width_for_determining_threshold))
    end_silent_zone = int(min_convolution + sample(0.25*silence_width_for_determining_threshold))
    silent_values = sound_data[start_silent_zone:end_silent_zone]
    max_value = 1.001*np.abs(silent_values).max() # a little headroom
    five_sigmas = 5 * silent_values.std()
    max_noise = max(max_value, five_sigmas) # if guassian, five sigmas will do it
    if plotting:
        fig, ax = plt.subplots()
        horizontal_marker(ax, whole_signal_mean, linewidth=1, color='blue')
        horizontal_marker(ax, 0, linewidth=0.5, color='black',)
        plt.title('%s '%(frame_info()))
        custom_lines = [Line2D([0], [0], color='blue', lw=2),
            Line2D([0], [0], color='black', lw=2),
            Line2D([0], [0], color='green', lw=2),
            ]
        ax.legend(custom_lines, 'whole_signal_mean,0.5 s rect pulse \nconvolution,silence zone'.split(','), loc='lower right')
        plt.plot(sound_data, marker='.', markersize='0.1', linewidth=0.3, color='purple', alpha=0.3)
        plt.plot(x_sliding_window, sliding_mean_values , marker='.', markersize='0.1', linewidth=0.3, color='black', alpha=0.3)
        width = end_silent_zone - start_silent_zone
        rect = patches.Rectangle((start_silent_zone, -max_noise), width, 2*max_noise, linewidth=1, edgecolor='green', facecolor='none')
        ax.add_patch(rect)
    def is_too_near_hedge(position):
        # segment is 2 sec wide, check if position + 0.25s fits in
        # because end of silence = sync pulse
        return position + 0.25*samplerate > 2*samplerate
    if is_too_near_hedge(min_convolution): # seems to never happen
        logger.error('%s is too close to right hedge, %s'%(min_convolution, 2*samplerate))
        raise ValueError('see log') 
        # TODO: min_convolution = switch_to_other(min_convolution)
    return max_noise, whole_signal_mean, end_silent_zone # end_silent_zone = where to start search

def find_1st_point_over_noise(sound_data, pulse_searching_start_indice, thresh):
    sound_data_extract = sound_data[pulse_searching_start_indice:]
    ofs = pulse_searching_start_indice
    pos_hedge = np.argmax(sound_data_extract > thresh) # find the first (np.argmax of bools)
    neg_hedge = np.argmax(sound_data_extract < -thresh) # True is a max compared to False
    rising_hedge_first_point = min(pos_hedge, neg_hedge)
    if False:
        fig, ax = plt.subplots()
        horizontal_marker(ax, 0, linewidth=0.5, color='black',)
        horizontal_marker(ax, thresh ,linewidth=0.5, color='black', linestyle='dashed')
        horizontal_marker(ax, -thresh ,linewidth=0.5, color='black', linestyle='dashed')
        plt.title('sample #%i (in extract)\n%s'%(rising_hedge_first_point + ofs,frame_info()))
        plt.plot(sound_data, marker='.', markersize='0.5', linewidth=0.1, color='purple')
        plt.plot([pos_hedge + ofs, neg_hedge + ofs],
            [sound_data_extract[pos_hedge], sound_data_extract[neg_hedge]],  marker='o', markersize='2', color='green', linestyle='None')
        plt.plot([rising_hedge_first_point + ofs], [0], marker='o', markersize='2', color='blue', linestyle='None')
        # plt.show()
    logger.debug('pulse at %i in sound_data'%(rising_hedge_first_point + ofs))
    return rising_hedge_first_point + pulse_searching_start_indice - 1

def find_exact_symbol_length(sound_data, pulse_position, samplerate,
        word_width_threshold):
    # return length in ms
    global plotting
    presumed_symbol_length = SYMBOL_LENGTH
    n_bits=N_SYMBOLS_SAMD21 - 1
    def sample_from_ms(ms):
        return 1e-3*ms*samplerate
    def time(sample):
        return sample/samplerate
    # presumed_symbol_length in ms
    # presumed_symbol_length and n_bits values from SAMD21 code
    search_start_position = int(0.67 * sample_from_ms(presumed_symbol_length) + pulse_position) # 2/3 inside the sync pulse
    presumed_width = sample_from_ms(presumed_symbol_length * n_bits)
    search_end_position = int(search_start_position + presumed_width) + 1000 # some headroom to start search outside
    if search_end_position > len(sound_data):
        logger.error('We are at the end of the file, trying to read past its end.')
        raise Exception('stopping here')
        # sound_data = sound_data[:int(len(sound_data)/MORE_THAN_A_SECOND)]
        # sound_data = np.concatenate([sound_data, sound_data[:search_end_position - len(sound_data)]]) 
    extract = sound_data[search_start_position : search_end_position]
    flipped_extract = np.flip(np.abs(extract))
    right_boundary = len(extract) - np.argmax(flipped_extract > word_width_threshold)  + search_start_position
    left_boundary = np.argmax(np.abs(extract) > word_width_threshold)  + search_start_position
    logger.debug('len(data) %i left_boundary, right_boundary: %i %i'%(len(sound_data),
        left_boundary, right_boundary))
    symbol_length = 1e3*(right_boundary - left_boundary)/(n_bits * samplerate)
    relative_error = (symbol_length - presumed_symbol_length)/presumed_symbol_length
    if relative_error > 0.03:
        logger.warning('actual symbol length differs too much: %.2f vs %.2f ms'%(symbol_length, presumed_symbol_length))
        # plotting = True
    if relative_error > 0.05:
        logger.error('actual symbol length differs too much: %.2f vs %.2f ms'%(symbol_length, presumed_symbol_length))
    logger.debug('effective symbol length %.4f ms, relative discrepancy %.4f%%'%(symbol_length, abs(100*relative_error)))
    if plotting:
        fig, ax = plt.subplots()
        horizontal_marker(ax, 0 ,linewidth=0.5, color='black')
        horizontal_marker(ax, word_width_threshold ,linewidth=0.5, color='blue')
        horizontal_marker(ax, -word_width_threshold ,linewidth=0.5, color='blue')
        plt.title(frame_info())
        plt.plot(sound_data, marker='.', markersize='0.5', linewidth=0.1, color='purple')
        plt.plot([pulse_position], [0], marker='o', markersize='2', linewidth=0, color='green')
        plt.plot([left_boundary, right_boundary], [0, 0], marker='o', markersize='2', linewidth=0, color='red')
        plt.plot([search_start_position, search_end_position], [0, 0], marker='o', markersize='2', linewidth=0, color='blue')
        custom_lines = [Line2D([0], [0], color='red', lw=2),
                        Line2D([0], [0], color='blue', lw=2),
            ]            
        ax.legend(custom_lines, ['word boundaries','word_width_threshold'], loc='lower right')
        plt.show()

    return symbol_length

def read_two_seconds(filename, where):
    # where is in secondes (fractional OK)
    logger.debug('will read around %.2f sec\n\n'%where)
    logger.debug('ffprobing %s '%(os.path.basename(filename) ))
    logger.debug('ffprobing %s '%(filename) )
    fprobe = ffmpeg.probe(filename)
    sr = int(fprobe['streams'][0]['sample_rate'])
    logger.debug('ffbprobed samplerate %i Hz'%(sr ))
    dryrun = (ffmpeg
        .input(filename, ss=where - 1, t=2)
        .output('pipe:', format='s16le', acodec='pcm_s16le')
        # .global_args("-loglevel", "quiet")
        # .global_args("-nostats")
        # .global_args("-hide_banner")      
        .get_args())
    dryrun = ' '.join(dryrun)
    logger.debug('using ffmpeg to pipe wav file into numpy array, ffmpeg get_args():\n%s'%dryrun)
    out, _ = (ffmpeg
        .input(filename, ss=where - 1, t=2)
        .output('pipe:', format='s16le', acodec='pcm_s16le')
        .global_args("-loglevel", "quiet")
        .global_args("-nostats")
        .global_args("-hide_banner")      
        .run(capture_stdout=True))
    data = np.frombuffer(out, np.int16)
    max_data = data.max()
    data = data/max_data
    return data, sr

def reading_half_a_second(filename, position):
    # 0.55 to be precise
    # poistion in sec
    out, _ = (ffmpeg
        .input(filename, ss=position , t=0.55)
        .output('pipe:', format='s16le', acodec='pcm_s16le')
        .global_args("-loglevel", "quiet")
        .global_args("-nostats")
        .global_args("-hide_banner")      
        .run(capture_stdout=True))
    data = np.frombuffer(out, np.int16)
    max_data = data.max()
    data = data/max_data
    return data

def make_second_fct_helper(samplerate):
  def f(sample):
    return sample/samplerate
  return f

def make_sample_fct_helper(samplerate):
  def f(time):
    return int(time * samplerate)
  return f

def main_frequency(symbol_data, samplerate):
    w = np.fft.fft(symbol_data)
    # w = np.fft.rfft(symbol_data)
    freqs = np.fft.fftfreq(len(w))
    # print(freqs.min(), freqs.max())
    idx = np.argmax(np.abs(w))
    freq = freqs[idx]
    freq_in_hertz = abs(freq * samplerate)
    return freq_in_hertz

def bit(freq):
  if np.isclose(freq, F1, 0.1):
    return '0'
  if np.isclose(freq, F2, 0.1):
    return '1'
  logger.error("FSK demodulation: can't match frequency %i after FFT (close to 10%%, neither %f nor %f Hz)"%(freq, F1, F2) )
  return None

def decode_int(binary_string, where, width):
  subset = binary_string[where:where+width]
  subset = subset[::-1]
  return int(subset,2)

def get_start_time(soundfile_name):
    # will try to demodulate two different beeps: at the beginning
    # and at the file end and validate them: number of seconds in the file
    # between them == nbr of seconds between demodulated UTC beeps
    duration, samplerate = file_info(soundfile_name)
    logger.debug('reading %s, duration %.1f seconds, sampled at %f Hz'
                 %(soundfile_name, duration, samplerate))
    if duration > 9:
        hop = 3 # seconds
    else:
        hop = int(duration/3)
    n_trials = 0
    for  i in [1, 2, 3]: # loop A
      n_trials += 1
      time_seconds_start = hop * i
      logger.debug('decoding trial #%i: %i sec from start'%(n_trials, time_seconds_start))
      beg = readUTC(soundfile_name, time_seconds_start)
      if beg[0]: # datetime found
        logger.info('trial #%i, succeeded decoding at %i sec'%(n_trials, time_seconds_start))
        break # from loop A
      else:
        logger.info('trial #%i, no decoding at %i sec'%(n_trials, time_seconds_start))
      continue # loop A
    if beg[0] is None: # no datetime found after all 3 trials
        logger.error('oups, couldnt decode none of the three bleeps at file start')
        # raise Exception('couldnt decode none of the three bleeps at file start stopping here')
        return None, None
    logger.info('will try to validate UTC at end with UTC at start')
    n_trials = 0
    n_validation = 0
    for i in [-3, -2, -1]: # loop B
      n_trials += 1
      offset_end = hop * i                                                                                                                                   
      time_seconds_end = duration + offset_end
      logger.debug('decoding trial #%i: %i sec from end, %i sec'%(n_trials, offset_end, time_seconds_end))
      end = readUTC(soundfile_name, time_seconds_end)
      if end[0]: #  datetime found
        logger.info('trial #%i, succeeded decoding at %i sec'%(n_trials, offset_end))
        n_validation += 1
        logger.info('does it validates with start? Check #%i'%n_validation)
        does_validate = delay_is_OK(beg, end, samplerate)
        if does_validate:
          logger.info('Yes, UTC at %i validates UTC at %i'%(offset_end, time_seconds_start))
        break # from loop B
      else:
        logger.info('trial #%i, no decoding at %i sec'%(n_trials, offset_end))
      continue # loop B
    if end[0] is None: # no datetime found after all 3 trials
        logger.error('oups, couldnt decode none of the three bleeps at file end')
      # raise Exception('stopping here')
        return None, None
    pulse_datetime_beginning, pulse_position_beginning = beg
    pulse_datetime_end, pulse_position_end = end
    delta_seconds_whole_file = (pulse_datetime_end - pulse_datetime_beginning).total_seconds()
    delta_samples_whole_file = pulse_position_end - pulse_position_beginning
    effective_samplerate = delta_samples_whole_file / delta_seconds_whole_file
    samplerate_discrepancy = 1e6*abs(effective_samplerate - samplerate)/samplerate
    base = os.path.basename(soundfile_name)
    incertitude_microsec = int(1e6/samplerate)
    start_UTC = pulse_datetime_beginning - timedelta(seconds=pulse_position_beginning/effective_samplerate)
    logger.info('%i UTC secs between start and end pulses and %i samples'%(delta_seconds_whole_file, delta_samples_whole_file))
    logger.info('effective sample rate: %s Hz'%(to_precision(effective_samplerate,8)))
    logger.info('stated sample rate %i Hz'%(samplerate))
    logger.info('sample rate discrepancy: %.0f ppm'%(samplerate_discrepancy))
    if __name__ == '__main__':
        console.print('\n  recording of [gold1]%s [/gold1]started at [gold1]%s (UTC) ± %i μs[/gold1]'%(base, start_UTC, incertitude_microsec))
        console.print('  localtime: [gold1]%s[/gold1]'%(start_UTC.astimezone().strftime('%Y-%m-%d %H:%M:%S')))
        console.print('  [gold1]%i UTC secs[/gold1] between start and end pulses for [gold1]%i[/gold1] samples'%(delta_seconds_whole_file, delta_samples_whole_file))
        console.print('  effective sample rate: [gold1]%s Hz[/gold1]'%(to_precision(effective_samplerate,8)))
        console.print('  stated sample rate [gold1]%i Hz[/gold1]'%(samplerate))
        console.print('  sample rate discrepancy: [gold1]%.0f ppm[/gold1]\n'%(samplerate_discrepancy))
    logger.info('recording of %s started at %s (UTC) ± %i us'%(base, start_UTC, incertitude_microsec))
    logger.info('localtime: %s'%(start_UTC.astimezone().strftime('%Y-%m-%d %H:%M:%S')))
    return start_UTC, effective_samplerate

def file_info(filename):
  probe = ffmpeg.probe(filename)
  audio_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'audio'), None)
  sample_rate = int(audio_stream['sample_rate'])
  # pprint(audio_stream)
  if 'nb_frames' in audio_stream:
    nb_frames = int(audio_stream['nb_frames'])
    duration = nb_frames / sample_rate
  else:
    if 'duration' in audio_stream:
      duration = float(audio_stream['duration'])
    else:
      logger.error('oups, cant find duration from ffprobe')
      raise Exception('stopping here')
  return duration, sample_rate # duration in sc. sample_rate in Hz

def demodulate2FSK(data_for_2FSK, pulse_position_in_extract, word_width_threshold, samplerate, pulse_position_in_file):
  # data_for_2FSK, pulse_position_in_2FSK_extract, samplerate = \
  #   reread_exactly_a_second(soundfile_name, extract_start_time_in_file, pulse_position_in_extract)
  sample = make_sample_fct_helper(samplerate)
  effective_symbol_length = find_exact_symbol_length(data_for_2FSK, pulse_position_in_extract, samplerate, word_width_threshold)
  # because SAMD21 core clock is  48 MHZ ± 2%
  symbol_length_samples = sample(effective_symbol_length*1e-3)
  if plotting:
    millis_symbols = effective_symbol_length * 1e-3 * np.arange(0, N_SYMBOLS_SAMD21 + 1)
    # millis_symbols_mid = effective_symbol_length * 1e-3 * (np.arange(0, N_SYMBOLS_SAMD21 + 1) + 0.5)
    sample_symbols = np.array([sample(t) for t in millis_symbols]) + pulse_position_in_extract
    # sample_symbols_mid = np.array([sample(t) for t in millis_symbols_mid]) + pulse_position_in_2FSK_extract
    fig, ax = plt.subplots()
    plt.title('sync at sample #%i in file, %.2f sec\n%s '%(pulse_position_in_file, pulse_position_in_file/samplerate, frame_info()))
    custom_lines = [Line2D([0], [0], color='blue', lw=3),
                # Line2D([0], [0], color='orange', lw=3),
                ]
    ax.legend(custom_lines, ['word_width_threshold'])
    horizontal_marker(ax, 0 ,linewidth=0.5, color='black')
    horizontal_marker(ax, word_width_threshold ,linewidth=1, color='blue')
    horizontal_marker(ax, -word_width_threshold ,linewidth=1, color='blue')
    # horizontal_marker(ax, pulse_detecting_threshold ,linewidth=1, color='orange')
    # horizontal_marker(ax, -pulse_detecting_threshold ,linewidth=1, color='orange')
    for x in sample_symbols:
      plt.plot([x, x], [-0.25, 0.25],  markersize='0.5', linewidth=0.8, color='green')
    plt.plot(data_for_2FSK, marker='.', markersize='0.5', linewidth=0.1, color='purple')
    plt.plot([pulse_position_in_extract], [0], marker='o', markersize='2', color='green')
    plt.show()
  logger.debug('symbol length %i samples'%symbol_length_samples)
  a1 = data_for_2FSK[pulse_position_in_extract:]
  def slice_analyse_decode(a):
    symbols_data = [a[x:x+symbol_length_samples] for x in range(0, len(a), symbol_length_samples)]
    symbols_data = symbols_data[1:N_SYMBOLS_SAMD21] # skip sync pulse
    frequencies = [main_frequency(data, samplerate) for data in symbols_data]
    time_correction_factor = effective_symbol_length/SYMBOL_LENGTH # because SAMD21 internal clock ± 2%
    frequencies = [int(time_correction_factor * f) for f in frequencies]
    logger.debug('word frequencies %s'%frequencies)
    # bits = [bit(f) for f in frequencies]
    bits = []
    for i,f in enumerate(frequencies):
        a_bit = bit(f)
        if a_bit == None:
            logger.error('FFT did not work for bit #%i'%i)
            return None # return from slice_analyse_decode()
        bits.append(a_bit)
    # if None in bits:
    #   logger.error('FFT did not work for bit #%i'%(bits.index(None)))
    #   return None # return from slice_analyse_decode()
    word = ''.join(bits)
    logger.debug('bits %s'%word)
    # indices_and_length = [(0,2),(2,6),(8,6),(14,5),(19,5)] # from SAMD21 code ppssync.ino
    indices_and_length = [(0,2),(2,6),(8,6),(14,5),(19,5),(24,4),(28,5)] # from SAMD21 code ppssync.ino
    vals = [decode_int(word,*d) for d in indices_and_length]
    logger.debug('decoded: %s'%vals)
    return vals
  vals1 = slice_analyse_decode(a1)
  if vals1 == None:
    logger.error('should try elsewhere')
    return None, None
  version, SS, MM, HH, DD, MT, YO = vals1
  if SS not in range(60) or MM not in range(60) or HH not in range(24) or MT not in range(1,12):
    logger.warning('decoded BFSK out of range')
    return None, None
  python_date1 = datetime(YO + 2021, MT, DD, HH, MM, SS, tzinfo=timezone.utc)
  logger.debug('decoded date ISO 8601 = "%s"'%python_date1)
  logger.debug('local time: %s'%(python_date1.astimezone().strftime('%Y-%m-%d %H:%M:%S')))
  return version, python_date1

def delay_is_OK(UTC_1, UTC_2, samplerate):
  # arguments are outputs of readUTC()
  if None in UTC_1 or None in UTC_2:
      return False
  # samplerate = UTC_1[2]
  datetime_1, sample_position_1 = UTC_1
  datetime_2, sample_position_2 = UTC_2
  diff_seconds_with_samples = (sample_position_2 - sample_position_1)/samplerate
  diff_seconds_with_UTC = (datetime_2 - datetime_1).total_seconds()
  logger.debug('check for delay between \n%s and\n%s'%(UTC_1, UTC_2))
  logger.info('delay using samples number: %f sec'%(diff_seconds_with_samples))
  logger.info('delay using timedeltas: %.2f sec'%(diff_seconds_with_UTC))
  return round(diff_seconds_with_samples) == diff_seconds_with_UTC
    
def readUTC(soundfile_name, extract_start_time_in_file):
  if extract_start_time_in_file < 0:
    logger.error('extract_start_time_in_file is negative!%f'%extract_start_time_in_file)
  # extract_start_time_in_file in seconds
  # UTC returned is within 2s around extract_start_time_in_file
  sound_data, samplerate = read_two_seconds(soundfile_name, where=extract_start_time_in_file)
  second = make_second_fct_helper(samplerate)
  sample = make_sample_fct_helper(samplerate)
  pulse_detecting_threshold, word_width_threshold, pulse_searching_start_indice = analyse_silence(sound_data, samplerate)
  pulse_position_in_sound_data = find_1st_point_over_noise(sound_data, pulse_searching_start_indice, thresh=pulse_detecting_threshold)
  pulse_position_in_file = pulse_position_in_sound_data + sample(extract_start_time_in_file - 1) # extract_start_time_in_file is in the middle of a 2 sec window
  logger.debug('PPS at %.3fs, sample #%i in file, #%i in read segment'%(second(pulse_position_in_file), pulse_position_in_file, pulse_position_in_sound_data))
  # the sync pulse-word end interval is exactly 500 ms
  # check if there's enough data after sync pulse for 2FSK demodulation
  nbr_of_samples_left = len(sound_data) - pulse_position_in_sound_data
  if nbr_of_samples_left < sample(510e-3):
    logger.debug('sync pulse near the segment end: 2FSK word is incomplete: %.02f sec'%second(nbr_of_samples_left))
    sound_data = reading_half_a_second(soundfile_name, pulse_position_in_file/samplerate)
    pulse_position_in_sound_data = 0
  version, UTC_datetime = demodulate2FSK(sound_data, pulse_position_in_sound_data, word_width_threshold, samplerate, pulse_position_in_file)
  return UTC_datetime, pulse_position_in_file

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str)
    args = parser.parse_args()
    soundfile_name = args.filename
    time, effective_SR = get_start_time(soundfile_name)
    plt.show()

if __name__ == '__main__':
    main()

