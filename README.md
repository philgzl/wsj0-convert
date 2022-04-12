# wsj0-convert
A Python script to convert the WSJ0 speech corpus to more friendly file formats.

# Requirements
- `sph2pipe` in PATH. Get it from [here](https://www.ldc.upenn.edu/language-resources/tools/sphere-conversion-tools).
- `ffmpeg` in PATH (not required if using the `--no-flac` option)

# Usage
Simply run:

```
python wsj0_convert.py <path-to-WSJ0> <output-dir>
```

This will create an `audio` directory inside `<output-dir>` containing all the audio files in `.flac` format,
or in `.wav` format if using the `--no-flac` option.
The audio files are organized in sub-directories by speakers.

# Notes
- Only `.wv1` files are converted. `.wv2` files are skipped.
- The original folder structure is not respected. Output files are organized in sub-directories by speaker.
- Total output size if 3.9 GB when using `.flac` format.
- For extra speaker information (e.g. gender), see [here](https://catalog.ldc.upenn.edu/docs/LDC93S6A/).
