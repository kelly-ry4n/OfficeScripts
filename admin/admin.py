import github, os, shutil

dirty_path = '../dirty/dirty.txt'

def update_dirty_scripts():
    ''' Reads dirty.txt and updates the files found. If succesful, clears dirty.txt'''
    dirty_scripts = get_dirty_scripts()

    for script in dirty_scripts:        ## Consider making this concurrent since network
        pull_from_project_url(script)   ## requests are very slow

    empty_dirty_file()

def empty_dirty_file():
    with open('../dirty/dirty.txt','w'):
        pass


def get_dirty_scripts():
    ''' Returns a list of dictionaries of dirty scripts'''

    with open(dirty_path) as f:
        raw_dirty_scripts = f.readlines()

    dirty_scripts = []
    for i in raw_dirty_scripts:
        scriptname, url, status = i.split()
        script = {'name':scriptname,'url':url, 'status':status}

        dirty_scripts.append(script)

    return dirty_scripts


def pull_from_project_url(script):
    ''' given a script dictionary, pulls from git to the appropriate folder. Raises ValueError
    if the project does not exist (name and status must be correct)'''

    script_path = '../' + script['status'] + '/' + script['name']
    print script_path
    if os.path.isdir(script_path):
        git_to_folder(script['url'], script_path)
    else:
        raise ValueError, "Invalid project name: %s, status: %s, url: %s" % (script['name'],
                                                                             script['status'],
                                                                             script['url'])

def git_to_folder(url, path):
    ''' Given a github url and path to a folder, merges the officescript branch of the repo at the url
    into the folder'''

    ## BUG
    ## if this function is called with stdin redirected and does not recieve input,
    ## git will remain running, and screw up all subsequent calls.
    ## This can lead to having a huge process tree open.
    ## This persists even after the python process is closed,
    ## so try to only call this from terminal, or make sure that public key
    ## authentication is used or username/password config is set up for
    ## the system's default git <whatever> command.

    branch = 'officescript'
    old_path = os.getcwd()
    os.chdir(path)

    if os.listdir('./')==[]:
        commands = [
            'git init',
            'git remote add -t %s -f origin %s' % (branch, url), ## This sometimes needs
                                                                 ## username and password
                                                                 ## authentication from
                                                                 ## stdin. See BUG at the top of
                                                                 ## this function.
            'git checkout %s' % branch
           ]
    else:
        commands = ['git pull origin officescript']

    for command in commands:
        os.system(command)

    os.chdir(old_path)


def new_project(name, state, url):
    ''' Creates a new project. name is the project name, url is its github url and state is
    alpha | beta | release. (these are strings)'''

    ## Just makes a new folder in the appropriate place.
    projstring = '%s %s %s' % (name, url, state)
    path   = '../%s/' % (state)

    old_path = os.getcwd()

    os.chdir(path)
    os.mkdir(path + name)

    os.chdir(old_path)

    add_project_to_list(name,state,url)

    mark_project_dirty(name)
    update_dirty_scripts()

def mark_project_dirty(name):
    '''Marks a project as dirty for later syncing from its officescript branch'''
    path = '../dirty/dirty.txt'
    project = get_project_from_name(name)
    name, url, state = project['name'],project['url'],project['status']

    if os.path.getsize(path) == 0:
        with open(path, 'a') as f:
            f.write('%s %s %s' % (name, url, state) )
    else:
        with open(path, 'a') as f:
            f.write('\n%s %s %s' % (name, url, state) )

def add_project_to_list(name, state, url):

    projstring = '%s %s %s' % (name, url, state)
    path   = '../projects/projects.txt'

    if os.path.getsize(path) == 0:
        with open(path, 'a') as f:
            f.write('%s %s %s' % (name, url, state) )
    else:
        with open(path, 'a') as f:
            f.write('\n%s %s %s' % (name, url, state) )

def get_projects_list():
    project_path = '../projects/projects.txt'
    with open(project_path) as f:
        raw_project_scripts = f.readlines()

    project_scripts = []
    for i in raw_project_scripts:
        scriptname, url, status = i.split()
        script = {'name':scriptname,'url':url, 'status':status}

        project_scripts.append(script)

    return project_scripts

def get_project_from_name(name):
    projects = get_projects_list()

    for p in projects:
        if p['name'] == name:
            return p

def get_project_from_url(url):
    projects = get_projects_list()

    for p in projects:
        if p['url'] == url:
            return p


if __name__ == '__main__':
    # mark_project_dirty('test_proj')
    # update_dirty_scripts()
    print get_project_from_name('test_proj')