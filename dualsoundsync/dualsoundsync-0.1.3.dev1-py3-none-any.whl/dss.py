#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse, sys
# from datetime import datetime, timedelta
from itertools import count
# import dualsoundsync.file_io as file_io
from . import file_io
import glob
from pprint import pprint
# from readPPStrack import validated_UTC_at_both_ends as start_time
from os.path import basename, splitext, split, join
# from pathlib import Path
from os import remove
# import scipy.io.wavfile as wavf
import numpy as np
import ffmpeg
from yaml import load
import os
from loguru import logger


def check_overlaps(yaml_files):
	def start_t(yaml):
		return yaml['start']
	yaml_video_files = [yaml for yaml in yaml_files if yaml['origin'] == 'video']
	yaml_video_files = sorted(yaml_video_files, key=start_t)
	yaml_audio_files = [yaml for yaml in yaml_files if yaml['origin'] == 'audio']
	yaml_audio_files = sorted(yaml_audio_files, key=start_t)
	for i in range(len(yaml_video_files) - 1):
		yaml = yaml_video_files[i]
		start = yaml['start']
		end = yaml['end']
		yaml_next = yaml_video_files[i + 1]
		start_next = yaml_next['start']
		video_overlaps = start_next < end
		if video_overlaps:
			n1, n2 = (yaml['filename'], yaml_next['filename'])
			logger.error('video %s and %s overlap, is this a multicam setup? Quitting.'%(n1, n2))
			raise Exception
	for i in range(len(yaml_audio_files) - 1):
		yaml = yaml_audio_files[i]
		start = yaml['start']
		end = yaml['end']
		yaml_next = yaml_audio_files[i + 1]
		start_next = yaml_next['start']
		video_overlaps = start_next < end
		if video_overlaps:
			n1, n2 = (yaml['filename'], yaml_next['filename'])
			logger.error('audio %s and %s overlap, is this a multicam setup? Quitting.'%(n1, n2))
			raise Exception

def find_matching_vids_and_sounds(yaml_files):
	times = []
	for yaml in yaml_files:
		t1 = {'start_or_end': 'start', 'time':yaml['start'], 'filename':yaml['filename'], 'rec_type':yaml['origin']}
		t2 = {'start_or_end': 'end', 'time':yaml['end'], 'filename':yaml['filename'], 'rec_type':yaml['origin']}
		times.append(t1)
		times.append(t2)
	def with_time(t):
		return t['time']
	times = sorted(times, key=with_time) # cardinality should be odd
	if len(times)%2 != 0:
		logger.error('odd number of recoding starts=stops?')
		raise Exception
	matched = []
	singles = []
	trio_pairs = []
	recording_indice = 0
	group_cardinality = 0
	for recording_indice in range(0, len(times), 2):
		group_cardinality += 2
		first_time = times[recording_indice] # a time is either an end or a begining
		second_time = times[recording_indice + 1]
		fst_type = first_time['start_or_end']
		scnd_type = second_time['start_or_end']
		name1 = first_time['filename']
		name2 =  second_time['filename']
		if fst_type == 'start' and scnd_type == 'end':
			# singleton
			if name1 != name2:
				logger.error('start and end time give a singleton but with two files? dekosse?')
				raise Exception
			if group_cardinality !=2:
				logger.error('start and end time give a singleton but with group_cardinality=%i'%group_cardinality)
				raise Exception
			singles.append(name1)
			group_cardinality = 0
			continue
		# from now on, it's a pair or a trio:
		if group_cardinality == 4: # closing a pair ?
			if fst_type == 'end' and scnd_type == 'end':
				if name1 == name2:
					logger.error('closing a pair with same file? dekosse?')
					raise Exception
				matched.append((name1, name2))
				group_cardinality = 0
				continue
			if fst_type == 'end' and scnd_type == 'start': # should be bridging a trio
				# print('bridging')
				if name1 == name2:
					logger.error('bridging a trio with same file? dekosse?')
					raise Exception
				trio_pairs.append((name1, name2))
				continue
			else:
				logger.error('group_cardinality is 4 and were not bridging!')
				raise Exception
		if group_cardinality == 6: # should be closing a trio
			if fst_type != 'end' or scnd_type != 'end':
				logger.error('group_cardinality is 6 and were not closing a trio!')
				raise Exception
			if name1 == name2:
				logger.error('closing a trio with same file? dekosse?')
				raise Exception
			trio_pairs.append((name1, name2))
			logger.debug('closing a trio')
			group_cardinality = 0
	if len(trio_pairs)%2 != 0:
		logger.error('trio_pairs length should be even, not odd: %i'%len(trio_pairs))
		raise Exception
	trios = []
	for pair_indice in range(0, len(trio_pairs) - 1, 2):
		p1 = set(trio_pairs[pair_indice])
		p2 = set(trio_pairs[pair_indice + 1])
		trios.append(set.union(p1,p2))
	return singles, matched, trios



def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("rushes_path", help="path of media directory")
	args = parser.parse_args()
	# try:
	#     if sys.argv[1]:
	#         rushes_path = str(sys.argv[1])
	# except:
	#     print( "no argument given - using Ramp/rushes")
	#     rushes_path = '/home/lutzray/SyncQUO/Dev/AtomicSync/Sources/PostProduction/Ramp/rushes'
	# print(args.rushes_path)
	rushes_path = args.rushes_path
	print('scanning %s'%rushes_path)
	os.chdir(rushes_path)
	file_io.mkdirs()
	print('splitting audio from video...')
	file_io.detach()
	print('splitting audio R and L channels')
	file_io.make_mono_files()
	print('trying to decode YaLTC in audio files')
	file_io.build_yaml_files()
	yaml_files = file_io.collect_yaml_files()
	print('looking for time overlaps forming pairs...')
	check_overlaps(yaml_files)
	singles, matched, trios = find_matching_vids_and_sounds(yaml_files) # names only
	for pair_names in matched: # retreiving data
		pair_yaml = [[yaml for yaml in yaml_files if yaml['filename'] == fn ][0] for fn in pair_names]
		video = [yaml for yaml in pair_yaml if yaml['origin'] == 'video'][0]
		audio = [yaml for yaml in pair_yaml if yaml['origin'] == 'audio'][0]
		video_start_time = video['start']
		audio_start_time = audio['start']
		time_difference = abs((audio_start_time - video_start_time).total_seconds())
		n_samples = int(time_difference * audio['effective-audio-samplerate'])
		wav_filename = file_io.find_wav_from_yml_filename(audio['filename'])
		video_filename = file_io.find_video_from_yml_filename(video['filename'])
		video_dir, video_name = split(video_filename)
		basename, extension = splitext(video_name)
		if basename[-2:] != '_v':
			raise Exception('%s not ending in _v'%video['filename'])
		merged_video_basename = basename[:-2] + extension
		logger.info('for %s delta: %f sec, %i samples'%(merged_video_basename, time_difference, n_samples))
		if video_start_time < audio_start_time:
			# audio is late, should pad it
			logger.info('%s audio is late, will pad it'%wav_filename)
			crop_or_pad_wav_file(wav_filename, n_samples)
		else: # audio is ahead, should shop it
			logger.info('%s audio is ahead, will shop it'%wav_filename)
			file_io.crop_or_pad_wav_file(wav_filename, - n_samples)
		print('joining back synced audio to video: ', end='')
		file_io.join_audio_and_video(wav_filename, video_filename, merged_video_basename)
		logger.info('wrote %s'%merged_video_basename)






