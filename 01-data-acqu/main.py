from subprocess import run
from os import getcwd, path, chdir
from contextlib import contextmanager

GIT_ROOT = 'https://github.com/'
CLONE_ROOT = 'clones/'

@contextmanager
def cd(newdir):
    # Credit cdunn2001 stackoverflow.com
    prevdir = getcwd()
    chdir(path.expanduser(newdir))
    try:
        yield
    finally:
        chdir(prevdir)


def cloneProject(repoOwner, project):
    gitURL = GIT_ROOT + repoOwner + '/' + project + '.git'
    cloneDir = CLONE_ROOT + project
    run(['git', 'clone', gitURL, cloneDir])


def cleanupProject(project):
    cloneDir = CLONE_ROOT + project
    run(['rm', '-rf', cloneDir])


def getCommitMetadata(repoOwner, project):
    cloneDir = CLONE_ROOT + project
    with open('commit_data/' + repoOwner + '#####' + project + '.csv', 'w') as ouputFile:
        with cd(cloneDir):
            run(['git', 'log', '--pretty=format:%H,,%an,,%ae,,%ad,,%cn,,%ce,,%ct'], stdout=ouputFile)


def getModifiedFiles(project):
    cloneDir = CLONE_ROOT + project
    with open('modified_files_data/' + project + '.csv', 'w') as outputFile:
        with cd(cloneDir):
            with open('temporary.nick', 'w') as tmpFile:
                run(['git', 'log', '--pretty=format:🐱%n%H', '--numstat'], stdout=tmpFile)
            for line in open('temporary.nick'):
                line = line[:-1]
                if line == '🐱':
                    commithash = ''
                elif line.strip() == '':
                    continue
                elif commithash == '':
                    commithash = line
                else:
                    added, deleted, modpath = line.split(maxsplit=2)
                    print(commithash + ',,' + str(added) + ',,' + str(deleted) + ',,' + modpath, file=outputFile)


def processProject(repo_owner, project):
    print('Repo Owner: ' + repo_owner + '; Project: ' + project)
    cloneProject(repo_owner, project)
    try:
        getCommitMetadata(repoOwner, project)
        getModifiedFiles(project)
        cleanupProject(project)
    except:
        cleanupProject(project)


if __name__ == '__main__':
    projects = []
    for line in open('resource/repos.list.subset'):
        repoOwner, project = line[:-1].split('/')
        projects.append((repoOwner, project))

        processProject(repoOwner, project)

