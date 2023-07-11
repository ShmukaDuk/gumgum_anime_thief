import os

folder_path = './episodes/'  # Replace with the actual folder path
output_file = 'missing_episodes.txt'  # Name of the output text file

# Get a list of existing episode numbers
existing_episodes = set()
for filename in os.listdir(folder_path):
    if filename.endswith('.mp4'):
        parts = filename.split('.')
        episode_number = parts[0]
        print(episode_number)
        parts2 = episode_number.split(' ')
        
        actual_episode_number = parts2[3]
        print(actual_episode_number)
        if actual_episode_number.isdigit():
            print("Found episode: ", actual_episode_number)
            existing_episodes.add(int(actual_episode_number))

# Determine the lowest and highest episode numbers
if existing_episodes:
    lowest_episode = min(existing_episodes)
    highest_episode = max(existing_episodes)
else:
    lowest_episode = highest_episode = None

# Find missing episode numbers
missing_episodes = []
if lowest_episode is not None and highest_episode is not None:
    for episode in range(lowest_episode, highest_episode + 1):
        if episode not in existing_episodes:
            missing_episodes.append(episode)

# Save missing episodes to a text file
with open(output_file, 'w') as file:
    file.write('\n'.join(str(episode) for episode in missing_episodes))

print('Missing episodes saved to', output_file)
