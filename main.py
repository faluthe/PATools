import os

if __name__ == '__main__':
    if os.geteuid() != 0:
        # Elevate to root using Polkit. Calls virtualenv's python executable to run this script.
        cwd = os.path.dirname(os.path.realpath(__file__))

        os.execvp("pkexec",
                  ["pkexec",
                   "env",
                   f"DISPLAY={os.environ['DISPLAY']}",
                   f"{cwd}/virtualenv/bin/python",
                   os.path.realpath(__file__)])
        
    from gui.layout import init_layout
    
    init_layout()