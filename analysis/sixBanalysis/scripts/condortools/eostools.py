import os
import subprocess

def exists_on_eos(lfn):
    """ check if lfn (starting with /store/group) exists """
    retcode = os.system('eos root://cmseos.fnal.gov ls -s %s > /dev/null 2>&1' % lfn)
    # print "THE FOLDER", lfn, "RETURNED CODE", retcode
    return True if retcode == 0 else False

def makedir_on_eos(lfn, recursive=True):
    """ make a directory on eos, whose name must start as in /store/group/... """
    flags = '-p' if recursive else ''
    retcode = os.system('eos root://cmseos.fnal.gov mkdir %s %s' % (flags, lfn))
    # print lfn, "create with code", retcode
    return True if retcode == 0 else False

def proxy_valid(min_lifetime_hrs = 5):
    """ check if the voms proxy is valid """

    proxyname = os. environ['X509_USER_PROXY']
    
    # proxy exists
    if not os.path.isfile(proxyname):
        return False

    # if exists, check that lifetime is good
    # lifetime = subprocess.check_output(['voms-proxy-info', '--file', myproxyname, '--timeleft']) ## in seconds
    lifetime = subprocess.check_output(['voms-proxy-info', '--timeleft']) ## in seconds
    lifetime = float(lifetime)
    lifetime = lifetime / (60*60)
    print '... proxy lifetime is', lifetime, 'hours'
    if lifetime < min_lifetime_hrs:
        return False    

    return True

def create_proxy(max_tries = 5):
    done  = False
    tries = 0

    while not done:
        status = os.system('voms-proxy-init -voms cms')
        tries += 1
        if os.WEXITSTATUS(status) == 0:
            done = True
        elif tries < max_tries:
            print "... something when wrong with proxy regeneration, please try again (%i tries left)" % (max_tries - tries)
        else:
            raise RuntimeError('create_proxy : cannot create a valid voms proxy')