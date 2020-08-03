def round_seconds_by_frequency(framerate, seconds):
    seconds = framerate * seconds
    seconds = int(seconds)
    seconds = seconds / framerate
    return seconds