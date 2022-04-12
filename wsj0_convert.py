import argparse
import os
import subprocess


def main():
    # check if input directory exists
    if not os.path.exists(args.input):
        raise ValueError('input directory does not exist')

    # check if output directory exists
    if not os.path.exists(args.output):
        raise ValueError('output directory does not exist')

    # create audio directory in output directory
    audio_dir = os.path.join(args.output, 'audio')
    if not os.path.exists(audio_dir):
        os.mkdir(audio_dir)

    # find all wv1 files
    wv1_files = []
    for root, folders, files in os.walk(args.input):
        for file in filter(lambda x: x.endswith('wv1'), files):
            wv1_files.append(os.path.join(root, file))
    n_files = len(wv1_files)

    # main loop
    for i, filepath in enumerate(wv1_files):

        # show progress
        if not args.quiet:
            print(f'{i}/{n_files} ({i/n_files*100:.1f}%)')

        # grab utterance id and speaker id and from filename
        utterance_id = os.path.basename(filepath).replace('.wv1', '.wav')
        speaker_id = utterance_id[:3]
        speaker_dir = os.path.join(audio_dir, speaker_id)
        if not os.path.exists(speaker_dir):
            os.mkdir(speaker_dir)

        # check if output file already exists
        wavfile = os.path.join(speaker_dir, utterance_id)
        flacfile = wavfile.replace('.wav', '.flac')
        if args.no_flac:
            outfile = wavfile
        else:
            outfile = flacfile
        if os.path.exists(outfile):
            if not args.quiet:
                print(f'{outfile} already exists')
            continue

        # call sph2pipe to convert to wav
        if not args.quiet:
            print(f'writing {wavfile}')
        subprocess.call([
            'sph2pipe',
            '-f',
            'wav',
            filepath,
            wavfile,
        ])

        # call ffmpeg to convert to flac and delete wav file
        if not args.no_flac:
            if not args.quiet:
                print(f'converting to {flacfile}')
            subprocess.call([
                'ffmpeg',
                '-y',
                '-i',
                wavfile,
                flacfile,
            ], stderr=subprocess.DEVNULL)
            os.remove(wavfile)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='convert WSJ0 corpus')
    parser.add_argument('input', help='path to WSJ0 corpus')
    parser.add_argument('output', help='output directory')
    parser.add_argument('--no-flac', action='store_true',
                        help='skip conversion to flac')
    parser.add_argument('--quiet', action='store_true',
                        help='disable verbose')
    args = parser.parse_args()
    main()
