import os
import sys

# Robust iterative commit creation
sys.setrecursionlimit(10**6)
import subprocess
import datetime
import argparse

def make_commit(days: int):
    if days < 1:
        # Push
        return os.system('git push')
    else:
        dates = f'{days} days ago'

        with open('date.txt', 'a') as file:
            file.write(f'{dates}\n')

        # Staging
        os.system("git add date.txt")

        # Commit
        os.system('git commit --date="'+dates+'" -m "First Commit"')
              
        return days * make_commit(days-1)
        
        
    

# Deprecated recursive call removed

# New implementation

def run(cmd, env=None, check=True):
    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    if check and result.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd) if isinstance(cmd, (list,tuple)) else cmd}\nstdout: {result.stdout}\nstderr: {result.stderr}")
    return result


def make_commits(days: int, yes: bool = False):
    if days < 1:
        print("No commits to create.")
        return
    if days > 100 and not yes:
        resp = input(f"About to create {days} commits. Proceed? [y/N]: ")
        if resp.lower() != 'y':
            print("Aborted.")
            return

    open('date.txt', 'a', encoding='utf-8').close()

    for i in range(days, 0, -1):
        date = datetime.datetime.utcnow() - datetime.timedelta(days=i)
        iso = date.isoformat() + 'Z'

        with open('date.txt', 'a', encoding='utf-8') as f:
            f.write(f"{i} days ago ({iso})\n")

        run(['git', 'add', 'date.txt'])

        env = os.environ.copy()
        env['GIT_COMMITTER_DATE'] = date.strftime('%a %b %d %H:%M:%S %Y +0000')

        msg = f'Commit for {date.date()}'
        run(['git', '-c', 'user.name=auto', '-c', 'user.email=auto@example.com', 'commit', '--date', iso, '-m', msg], env=env)
        print(f'Created commit dated {iso}')

    print("Done creating commits.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--days', type=int, default=365)
    parser.add_argument('--yes', action='store_true', help='Skip confirmation')
    args = parser.parse_args()

    make_commits(args.days, yes=args.yes)


if __name__ == '__main__':
    main()

