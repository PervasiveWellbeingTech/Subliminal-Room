import librosa

def track_beats(input_file):
    print('Loading ', input_file)
    y, sr = librosa.load(input_file, sr=22050)
    # Use a default hop size of 512 samples @ 22KHz ~= 23ms
    hop_length = 512
    # This is the window length used by default in stft
    print('Tracking beats...')
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr, hop_length=hop_length)
    print('Estimated tempo: {:0.2f} beats per minute'.format(tempo))
    # 'beats' will contain the frame numbers of beat events.
    beat_times = librosa.frames_to_time(beats, sr=sr, hop_length=hop_length)
    print("Beat table generated.")
    # print(beat_times)
    return (beat_times, tempo)

def test():
    print(beat_track('heartbeat.mp3'))
