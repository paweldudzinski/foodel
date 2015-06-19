from fabric.api import local, cd, env

env.hosts = ['papaduda@web1.mydevil.net']

class DeployPreparator(object):

    def __init__(self, commit_message):
        self.commit_message = commit_message
    
    def push_changes(self):
        local("git add .")
        local("git commit -m '%s'" % (self.commit_message))
        local("git push origin master")
        
        
def deploy(commit_message='pushed via fabric'):
    preparator = DeployPreparator(commit_message)
    preparator.push_changes()
    cd('~/foodel/foodel')
