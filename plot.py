import matplotlib.pyplot as plt

# Data
attempts = [1, 2, 3]
final_losses = [0.118, 0.0881, 0.0715]
times = ["16:31", "24:15", "36:11"]

# Convert times to minutes
times_in_minutes = [int(time.split(':')[0]) * 60 + int(time.split(':')[1]) for time in times]

# Create the plot
plt.plot(times_in_minutes, final_losses, marker='o', linestyle='-')
plt.xlabel('Time (minutes)')
plt.ylabel('Final Loss')
plt.title('Final Loss vs Time')

# Annotate the points
for i, txt in enumerate(attempts):
    plt.annotate(f'Attempt {txt}', (times_in_minutes[i], final_losses[i]), textcoords="offset points", xytext=(0, 10), ha='center')

# Show the plot
plt.show()
