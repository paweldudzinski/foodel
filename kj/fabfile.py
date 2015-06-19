from fabric.api import local

def push_changes(message = 'pushed via fabric'):
    local("git add .")
    local("git commit -m '%s'" % (message))
    local("git push origin master")
