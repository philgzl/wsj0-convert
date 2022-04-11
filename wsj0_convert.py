import argparse
import json
import os
import re
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

    # initialize metadata dictionary
    metadata = {}

    # main loop
    for root, folders, files in os.walk(args.input):
        for file in filter(lambda x: x.endswith(('wv1', 'wv2')), files):
            filepath = os.path.join(root, file)

            # parse metadata from file header
            with open(filepath, 'rb') as f:
                header = f.read(1024).decode("utf-8")
            m = re.findall(r"([\S]+?) -[\S]+? (.+?)\n", header)
            if not m:
                raise ValueError(f'could not parse header in {filepath}')
            file_metadata = dict(m)

            # use the utterance id as key
            utterance_id = file_metadata.pop('utterance_id')
            metadata[utterance_id] = file_metadata

            # grab speaker id and create speaker directory
            speaker_id = file_metadata['speaker_id']
            speaker_dir = os.path.join(audio_dir, speaker_id)
            if not os.path.exists(speaker_dir):
                os.mkdir(speaker_dir)

            # check is output file already exists
            wavfile = os.path.join(speaker_dir, f'{utterance_id}.wav')
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

    # save metadata
    with open(os.path.join(args.input, 'metadata.json'), 'w') as f:
        json.dump(metadata, f)


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
