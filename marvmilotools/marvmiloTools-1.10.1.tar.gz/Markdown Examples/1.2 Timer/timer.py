import marvmiloTools as mmt
from time import sleep

#start the timer
mmt.timer.start()

sleep(3)

#pause timer
runtime = mmt.timer.pause()
print("Type of runtime: " + str(type(runtime)))
print("Runtime at pause: " + str(runtime))

#reset timer and get runtime function
mmt.timer.reset()
runtime = mmt.timer.get_runtime()
print("Runtime at reset: " + str(runtime))

#set some laps
mmt.timer.start()
for i in range(3):
    sleep(1)
    runtime = mmt.timer.set_lap()
    print("Runtime at lap " + str(i) + ": " + str(runtime))

#get all laps
laps = mmt.timer.get_laps()
print("Laps: " + str(laps))

sleep(2)

#get time of current lap without setting a lap
lap_runtime = mmt.timer.get_lap_runtime()
print("Current Lap Runtime: " + str(lap_runtime))