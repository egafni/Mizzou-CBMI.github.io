from argh import arg,ArghParser,command,CommandError
import cosmos_session
from Workflow.models import Workflow
import os

@arg('id',type=str, help='id for workflow to terminate')
def terminate(args):
    if args.id is None:
        raise CommandError('please choose a name OR an id')
    wf = Workflow.objects.get(pk=args.id)
    print "Telling workflow {0} to terminate".format(wf)
    wf.terminate()

    #lsf qdel all: bjobs|cut -d " " -f 1 -|sed 1d|xargs -t -L 1 qdel

@arg('-p','--port',help='port to serve on',default='8080')
def runweb(args):
    os.system('manage runserver 0.0.0.0:{0}'.format(args.port))   
     
        
def shell(args):
    os.system('manage shell_plus')

@arg('id',help='workflow id')
@arg('-q',action="store_true",help='Queued Jobs only')  
@arg('-jid',action="store_true",help='Job id only')    
def jobs(args):
    jobs = Workflow.objects.get(pk=args.id).jobManager.jobAttempts.all()
    if args.q:
        jobs = jobs.filter(queue_status='queued')
    for ja in jobs:
        if args.jid:
            print ja.drmaa_jobID
        else:
            print ja
    
            
    
@arg('id',type=int,help='workflow id')    
def list(args):
    for workflow in Workflow.objects.all():
        print workflow
    
parser = ArghParser()
parser.add_commands([runweb,shell],namespace='adm',title='Admin')
parser.add_commands([terminate,list,jobs],namespace='wf',title='Workflow')

if __name__=='__main__':
    parser.dispatch()