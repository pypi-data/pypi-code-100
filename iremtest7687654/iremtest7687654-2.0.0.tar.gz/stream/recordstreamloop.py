## This method nor required for recording stream. Please check run.sh or create new one.

from stream.recordstream import record_stream


def record_stream_loop(loop: int):
    counter = 0
    while True:
        counter += 1  # Count the while loop.
        # We call record_stream function and add args.
        # In future, we will call this args from current function for flexible use.
        record_stream(
            source='',  # What is source link?
            limit=10,  # How many frames will be captured for this video.
            time_sleep=1,  # How many times have a frame in seconds?
            frame_rate=1.0,  # How many frames per second in the video?
            output_path='storage/'
        )
        # Break the loop when counter reached the loop limit.
        if counter == loop:
            break


# We created run function to execute record_stream_loop function
def run_loop():
    record_stream_loop(
        loop=15
    )


if __name__ == "__main__":
    run_loop()
