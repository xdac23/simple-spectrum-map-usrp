import subprocess
import sys

if len(sys.argv) != 3:
    print("Usage: python3 controller.py <from_iter> <to_iter>")
    sys.exit(1)

from_iter = int(sys.argv[1])
to_iter = int(sys.argv[2])

# Execute n77_exporter.py script for each iteration
for iteration in range(from_iter, to_iter + 1):
    # Construct the command to execute n77_exporter.py with the current iteration number
    command = ['python3', 'n77_exporter.py', f'--iteration={iteration}']

    # Execute the command
    subprocess.run(command)
