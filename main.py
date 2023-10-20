import subprocess

# List of scripts to run
scripts = [
    "DefenseStats.py",
    "KickingStats.py",
    "PassingStats.py",
    "ReceivingStats.py",
    "RushingStats.py"
]

successful_runs = 0

for script in scripts:
    print(f"Executing {script}...")
    result = subprocess.run(["python", script])

    # Check the return code of the script. If it's 0, it means the script executed successfully.
    if result.returncode == 0:
        successful_runs += 1
        print(f"{script} executed successfully!\n")
    else:
        print(f"Error executing {script}.\n")

print(f"{successful_runs} out of {len(scripts)} scripts executed successfully!")
