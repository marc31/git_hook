#!/usr/bin/env python

import os
import subprocess

from pathlib import Path
from shutil import which

# Helper to run program
def run(program, command, cwd = './'):
    args = [program] + command.split()
    p = subprocess.Popen(args, cwd=cwd, stdout=subprocess.PIPE)
    return p.stdout.read().strip()
        
def main():
    # Create client path if not exist
    clientPath = os.path.abspath('./client')
    Path(clientPath).mkdir(parents=True, exist_ok=True)

    # Create server path if not exist
    serverPath = os.path.abspath('./server')
    Path(serverPath).mkdir(parents=True, exist_ok=True)
    
    # Init server bare
    run('git', 'init --bare', cwd=serverPath)
    
    # Make symbolik link into server for post-receive
    run(
        'ln',
        '-s %s post-receive' % os.path.join(os.path.abspath('.'), 'hook-py', 'post-receive'),
        cwd=os.path.join(serverPath, 'hooks')
    )
        
    # Init client
    run('git', 'init', cwd=clientPath)
    run('git', 'remote add deploy %s' % serverPath, cwd=clientPath)
    run('git', 'checkout -b prod', cwd=clientPath)
    run(
        'ln',
        '-s %s pre-commit' % os.path.join(os.path.abspath('.'), 'hook-py', 'pre-commit'),
        cwd=os.path.join(clientPath, '.git', 'hooks')
    )
    
    # First commit
    f = open(os.path.join(clientPath,'test'), "w+")
    f.write("Test")
    f.close()
    run('git', 'add .', cwd=clientPath)
    run('git', "commit -am 'test' -m '!migrate'", cwd=clientPath)
    run('git', 'push --set-upstream deploy prod', cwd=clientPath)
    run('git', 'push deploy', cwd=clientPath)
        
if __name__ == '__main__':
    try:
        main()
    except:
        print('Encountered an exception in the main loop.')

