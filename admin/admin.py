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
    if os.path.isdir(script_path):
        git_to_folder(script['url'], script_path)
    else:
        raise ValueError, "Invalid project name: %s, status: %s, url: %s" % (script['name'],
                                                                             script['status'],
                                                                             script['url'])

def git_to_folder(url, path):
    ''' Given a github url and path to a folder, merges the officescript branch of the repo at the url
    into the folder'''
    branch = 'officescript'
    old_path = os.getcwd()
    os.chdir(path)

    if os.listdir('./')==[]:
        commands = [
            'git init',
            'git remote add -t %s -f origin %s' % (branch, url),
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

    projstring = '%s %s %s' % (name, url, state)
    path   = '../%s/' % (state)

    old_path = os.getcwd()

    os.chdir(path)
    os.mkdir(path + name)

    os.chdir(old_path)

def mark_project_dirty(name,state,url):
    '''Marks a project as dirty for later syncing from its officescript branch'''
    path = '../dirty/dirty.txt'
    if os.path.getsize(path) == 0:
        with open(path, 'a') as f:
            f.write('%s %s %s' % (name, url, state) )
    else:
        with open(path, 'a') as f:
            f.write('\n%s %s %s' % (name, url, state) )



if __name__ == '__main__':
    ## update_dirty_scripts()
    ## new_project('test_script', 'alpha', 'https://github.com/kelly-ry4n/test_script')
    ## mark_project_dirty('test_script', 'alpha', 'https://github.com/kelly-ry4n/test_script')
