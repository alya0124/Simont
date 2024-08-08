import subprocess

def export_requirements(filename='requirements.txt'):
    with open(filename, 'w') as f:
        result = subprocess.run(['pip', 'freeze'], stdout=subprocess.PIPE, text=True)
        f.write(result.stdout)

if __name__ == "__main__":
    export_requirements()