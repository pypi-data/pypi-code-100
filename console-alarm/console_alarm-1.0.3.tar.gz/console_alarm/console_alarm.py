#!/usr/bin/env python3.9
""" A small console script to set an alarm clock.

Summary
-------
	Small alarm function for your console. Usable with one ([minutes] like
	a pomodoro) or two numeric arguments ([hh] [mm] sets alarm time).
	Also usable as module. But for bigger projects another approach should
	be used, because this one uses sleep and freezes the thread.

Routine Listings
----------------
	start_pomodoro
		Starts pomodorolike alarm.

	start_alarm_clock
		Starts an alarm that rings at a specified time.

	ring
		Rings the alarm for a given amount of seconds.

Notes
-----
	This alarm clock checks every minute how long the script has to sleep
	until the alarm rings. When less than a minute is left, the script
	waits for this period of time and then rings.

	This approach is not preferred for projects where you can set more
	than one timer and where you want to stop timer before they ring.

	Therefore I would suggest a list of active timer timestamps that are
	checked periodically in background (every second or less) and start an
	alarm if the current time passes one of the list values. After the
	alarm starts, this timestamp could be set to a snooze (maybe 5
	minutes) or get removed after the user notices the alarm.
"""

import sys
import time
import numpy
import pygame
import pygame.sndarray
from math import floor


def start_pomodoro(minutes: int, /):
	""" Starts pomodorolike alarm.

	Parameters
	----------
	minutes : float
		In how many minutes the alarm should start. Minutes has to be
		between 1 and 1439.

	Raises
	------
	ValueError
		If the [minutes] parameter isn't between 1 and 1439.

	TypeError
		If the [minutes] parameter is not int.

	See Also
	--------
	start_alarm_clock

	Example
	-------
	start_pomodoro(1409)
	"""

	# Check if parameter is in range.
	_is_in_range(minutes, 1, 1439)

	# Add [minutes] to current time.
	alarm = time.localtime(time.time()+minutes*60)

	# We set the alarm clock to the calculated time.
	start_alarm_clock(alarm.tm_hour, alarm.tm_min, alarm.tm_sec)


def start_alarm_clock(alarm_hour: int, alarm_min: int, alarm_sec: int = 0, /):
	""" Starts an alarm that rings at a specified time.

	Parameters
	----------
	alarm_hour : int
		The hour value of the alarm time.
	alarm_min : int
		The minute value of the alarm time.
	alarm_sec : int, default = 0
		The seconds of the alarm time. This parameter is optional and
		defaults to 0.

	Raises
	------
	ValueError
		If the [alarm_hours] parameter isn't between 0 and 23 or
		[alarm_min] or [alarm_sec] parameters aren't between 0 and 59.

	TypeError
		If one of the [alarm_hour], [alarm_min] or [alarm_sec] parameters
		is not int.

	See Also
	--------
	start_pomodoro

	Example
	-------
	startAlarmClock(14,9)
	"""

	# Check if parameters are in range.
	_is_in_range(alarm_hour, 0, 23)
	_is_in_range(alarm_min, 0, 59)
	_is_in_range(alarm_sec, 0, 59)

	# Here we calc how many seconds we have to wait.
	remaining_seconds = _calc_secs_to_time(alarm_hour, alarm_min, alarm_sec)

	# Define boolean variable to break the while loop
	is_waiting_done = False

	# Sleeping time!
	# While there are still seconds to wait
	while not is_waiting_done:
		# Memorize the last count of remaining seconds
		old_remaining_seconds = remaining_seconds

		# Calc how many seconds are still on the clock
		remaining_seconds = _calc_secs_to_time(alarm_hour, alarm_min, alarm_sec)

		# Tell the user about the waiting time
		_print_time_until_alarm(remaining_seconds)

		# Check if os was hibernated during alarm ring
		if old_remaining_seconds < remaining_seconds:
			print('Missed alarm!', old_remaining_seconds, remaining_seconds)
			return

		# Check if there are less than 60 seconds left.
		if 60 >= remaining_seconds > 0:
			# Sleep for the last few seconds.
			time.sleep(remaining_seconds)
			is_waiting_done = True
		elif remaining_seconds >= 60:
			# Sleep for 60 seconds and check again
			time.sleep(60)

	# And time to wake up!!
	print("Wake up!!! <3")
	ring(5)


def ring(seconds: int, /):
	""" Rings the alarm for a given amount of [seconds].

	Parameters
	----------
	seconds : int
		How long the alarm is going to ring.

	Raises
	------
	ValueError
		If the [seconds] parameter isn't between 1 and 60.

	TypeError
		If the [seconds] parameter is not int.

	Example
	-------
	_ring(5)
	"""

	# Check if parameter is in range.
	_is_in_range(seconds, 1, 60)

	# Initializing pygame for playing audio
	pygame.mixer.pre_init(44100, -16, 1)
	pygame.init()

	# Load the notes we want to play
	# C-4 (Do)
	low = _get_note(261.626)

	# G-4 (Sol)
	high = _get_note(391.995)

	# Play the one second alarm sound for the passed number of seconds.
	for i in range(seconds):
		for x in range(10):
			_play_note(high, 25)
			_play_note(low, 25)
		pygame.time.delay(500)


def _get_note(frequency: float, /) -> pygame.mixer.Sound:
	""" Calculates the note and returns a Sound object.

	Parameters
	----------
	frequency : float
		The frequency of the note e.g. 440 for A and 880 for A'.

	Returns
	-------
	pygame.mixer.Sound
		The calculated Sound object, that can be played.

	Raises
	------
	ValueError
		If the [frequency] parameter isn't between 1 and 44100.

	TypeError
		If the [frequency] parameter is not float or int.
	"""

	# Check if parameter is in range.
	_is_in_range(floor(frequency), 1, 44099)

	# Check if parameter has the correct type,
	if not isinstance(frequency, (int, float)):
		raise TypeError

	# How many sound frames are there per wave
	frames = 44100/frequency

	# Put the sawtooth frames into an array.
	arr = numpy.array([16384 * (x % frames) / frames - 8192 for x in range(0, 44100)]).astype(numpy.int16)

	# Return a Sound object created from the wave frame array.
	return pygame.sndarray.make_sound(arr)


def _play_note(sound: pygame.mixer.Sound, duration: int, /):
	""" Plays the passed note for the passed duration.

	Parameters
	----------
	sound : pygame.mixer.Sound
		The Sound object containing the note.
	duration : int
		The duration of the note in milliseconds.

	Raises
	------
	ValueError
		If duration is smaller than or equal 0.

	TypeError
		If the [sound] parameter is not pygame.mixer.Sound or [duration]
		is not int.

	Example
	-------
	_play_note(high_C, 50)
	"""

	# Check if parameter [duration] is in range.
	_is_in_range(duration, 1)

	# Check parameter [sound] for correct type.
	if not isinstance(sound, pygame.mixer.Sound):
		raise TypeError

	sound.play(-1)
	pygame.time.delay(duration)
	sound.stop()


def _print_time_until_alarm(seconds: int, /):
	""" Prints the time until the alarm rings onto the console.

	Parameters
	----------
	seconds : int
		The remaining seconds until the alarm rings.

	Raises
	------
	ValueError
		If the [seconds] parameter is smaller than 0.

	TypeError
		If the [seconds] parameter is not int.

	Example
	-------
	print_time_until_alarm(128)
	> Alarm starts in 0 hour(s), 2 minute(s), and 8 second(s)
	"""

	# Check if parameter is in range.
	_is_in_range(seconds, 0)

	# Calc our user output.
	needed_hour = floor(seconds / 3600)
	needed_min = floor((seconds - (needed_hour * 3600)) / 60)
	needed_sec = floor(seconds - needed_min * 60 - needed_hour * 3600)

	# Here we inform the user on how long he have to wait for his alarm.
	print("Alarm starts in {} hour(s), {} minute(s), and {} second(s)".format(needed_hour, needed_min, needed_sec))


def _calc_secs_to_time(hour: int, minutes: int, seconds: int = 0, /) -> int:
	""" Calculates the amount of seconds until the alarm is supposed to ring.

	Parameters
	----------
	hour : int
		The clocks hour value at the alarm ring time.
	minutes : int
		The clocks minute value at the alarm ring time.
	seconds : int, optional = 0
		The clocks second value at the alarm ring time.

	Returns
	-------
	int
		Seconds remaining until the alarm rings.

	Raises
	------
	ValueError
		If [hour] isn't between 0 and 23 or [minutes] or [seconds] aren't
		between 0 and 59.

	TypeError
		If one of the [hour], [minutes] or [seconds] parameters is not
		of type int.

	Example
	-------
	_calc_secs_to_time(14, 9)
	"""

	# Check if parameters are in range.
	_is_in_range(hour, 0, 23)
	_is_in_range(minutes, 0, 60)
	_is_in_range(seconds, 0, 60)

	# Get the current time.
	now = time.localtime()

	# Put the hours and the minutes of the current time in variables.
	current_hour = now.tm_hour
	current_min = now.tm_min

	# How many minutes do we have to wait?
	needed_min = minutes - current_min

	# If the value of minutes is smaller than the current times minutes.
	# e.g when it is 14:09 and you set the alarm for 15:06
	if needed_min < 0:
		# We need a positive value for the seconds.
		needed_min += 60
		# And we reduce the hours we need to wait by one.
		current_hour += 1

	# Now we check how much hours there are until the alarm rings.
	needed_hour = hour - current_hour

	# If the hour value is smaller than hour current time, we have a day switch in it.
	# e.g when it is 20:06 and you set the alarm for 19:06
	if needed_hour < 0:
		needed_hour += 24

	# If the user wants to set the current time as an alarm.
	if needed_hour == needed_min == 0:
		needed_hour = 24

	# Return the seconds remaining until the alarm rings.
	return needed_min*60 + needed_hour*3600 - now.tm_sec + seconds


def _is_in_range(value: int, minimum: int = -sys.maxsize - 1, maximum: int = sys.maxsize, /):
	""" Checks if value is in range and raises an exception if not.

	Parameters
	----------
	value : int
		The value that should be checked.
	minimum : int, default = -sys.maxsize - 1
		The smallest value the [value] parameter is allowed to have.
	maximum : int, default = sys.maxsize
		The biggest value the [value] parameter is allowed to have.

	Raises
	------
	ValueError
		If [value] is not between [minimum] and [maximum].

	TypeError
		If [value], [minimum] or [maximum] is not int.
	"""

	if not (isinstance(value, int) and isinstance(minimum, int) and isinstance(maximum, int))\
		or isinstance(value, bool) or isinstance(minimum, bool) or isinstance(maximum, bool):
		raise TypeError

	if not minimum <= value <= maximum:
		raise ValueError


def _print_help():
	""" Prints the help text. """

	print("")
	print("Small alarm function for your console.")
	print("Usable with one or two numeric arguments.")
	print("")
	print("One argument:")
	print("If there is only one argument it is interpreted as minutes. The alarm will act")
	print("as a pomodoro that rings after the set minutes. The maximum amount of minutes")
	print("is 1439 and the minimum is 1.")
	print("")
	print("Two arguments:")
	print("With two arguments, you will set a alarm clock for a specified time.")
	print("If you set 14 09 as arguments, the alarm will start at 14:09.")
	print("")
	print("On ubuntu you can put this task into background with 'ctrl+z' and then run 'bg'")
	print("Get it to the foreground again with fg")


def console_entry_point(sys_args):
	# If the user entered one numeric parameter.
	if len(sys_args) == 2 and sys_args[1].isnumeric():

		# Load the parameter as minutes.
		arg_minutes = (int(sys_args[1]))

		# Check if the pomodoro is set to a reasonable time.
		if 1 <= arg_minutes < 1440:

			# Start the pomodoro.
			start_pomodoro(arg_minutes)

		else:
			# Else we tell the user how he can use this tool.
			_print_help()

	# If the user entered two numeric parameter.
	elif len(sys_args) == 3 and sys_args[1].isnumeric() and sys_args[2].isnumeric():

		# The first parameter is the hour value of the set time.
		arg_hour = int(sys_args[1])
		# The second parameter is the minute value of the set time.
		arg_minute = int(sys_args[2])

		# Check if the hour and minute values are reasonable for a alarm clock time.
		if arg_hour >= 0 or arg_hour < 24 or arg_minute >= 0 or arg_minute < 60:
			# We start our alarm clock.
			start_alarm_clock(arg_hour, arg_minute)
		else:
			# Else we let the user know how to use this tool.
			_print_help()

	# Else there where the wrong number of arguments or they had the wrong type.
	else:
		# Show the help text.
		_print_help()


# If the module is run as a script.
if __name__ == "__main__":
	console_entry_point(sys.argv)
