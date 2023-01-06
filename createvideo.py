# !/usr/bin/python3

import os
import subprocess

# Set the path to the directory with the short videos
path = '/path/to/short/videos'

# Set the path to the directory where the compiled videos should be saved
output_path = '/path/to/compiled/videos'

# Set the path to the directory where the used short videos should be moved
used_path = '/path/to/used/videos'

# Set the maximum length of the compiled video in seconds
max_length = 720  # 12 minutes

# Set the name of the compiled video
output_name = 'compiled_video.mp4'

# Set the path to the ffmpeg executable
ffmpeg_path = '/path/to/ffmpeg'

# Set the input and output file paths
input_files = ''
output_file = os.path.join(output_path, output_name)

# Keep track of the total length of the compiled video
total_length = 0

# Iterate through the short videos in the directory
for file in os.listdir(path):
    # Get the file path
    file_path = os.path.join(path, file)

    # Get the file length using ffmpeg
    result = subprocess.run([ffmpeg_path, '-i', file_path], stderr=subprocess.PIPE)
    output = result.stderr.decode()
    duration_line = [line for line in output.split('\n') if 'Duration' in line][0]
    time_parts = duration_line.split(',')[0].split(': ')[1].split(':')
    file_length = int(time_parts[0]) * 3600 + int(time_parts[1]) * 60 + int(time_parts[2])

    # Add the file to the input list and update the total length if it fits
    if total_length + file_length <= max_length:
        input_files += f'-i {file_path} '
        total_length += file_length
    else:
        # If the file does not fit, break out of the loop
        break

# Concatenate the short videos into a single longer video using ffmpeg
subprocess.run([ffmpeg_path, '-y', input_files, '-filter_complex', f'concat=n={len(input_files.split("-i ")) - 1}:v=1:a=1', output_file], stderr=subprocess.PIPE)

# Move the used short videos to the used directory
for file in input_files.split("-i ")[1:]:
    os.rename(file, os.path.join(used_path, os.path.basename(file)))
