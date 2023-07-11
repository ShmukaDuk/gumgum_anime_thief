import os

folder_path = './episodes1/'  # Replace with the actual folder path

# Iterate over each file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.mp4'):
        # Extract episode number and resolution
        parts = filename.split('.')
        episode_number = parts[1]
        resolution = parts[3]
        file_extension = parts[-1]

        # Create new filename
        new_filename = f"One Piece Episode {episode_number}.{resolution}.{file_extension}"

        # Rename the file
        old_path = os.path.join(folder_path, filename)
        new_path = os.path.join(folder_path, new_filename)
        os.rename(old_path, new_path)