from fabric.api import local, cd, env, run

env.hosts = ['web1.mydevil.net']
env.user = 'papaduda'
env.password = 'xWmnCtoV'

class DeployPreparator(object):

    def __init__(self, commit_message):
        self.commit_message = commit_message
    
    def push_changes(self):
        local("git add .")
        local("git commit -m '%s'" % (self.commit_message))
        local("git push origin master")
        
    def update_remote(self):
        print env.user
        with cd("~/foodel/foodel"):
            run("git pull")
            
    def restart(self):
        with cd("~/foodel/foodel"):
            run("kill -9 `ps aux | grep -v grep | grep '/home/papaduda/python-env/bin/python' | awk '{print $2}'`")
            run("/home/papaduda/python-env/bin/python /home/papaduda/python-env/bin/pserve --reload --daemon --pid-file=pserve_5000.pid production.ini http_port=5000")
        
def deploy(commit_message='pushed via fabric'):
    preparator = DeployPreparator(commit_message)
    preparator.push_changes()
    preparator.update_remote()
    preparator.restart()
    
        

