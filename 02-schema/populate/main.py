from os import walk
from subprocess import run

COMMIT_DATA_DIR = '../../01-data-acqu/commit_data'
MOD_FILES_DIR = '../../01-data-acqu/modified_files_data'

if __name__ == '__main__':
    arg1 = input("enter u")
    arg2 = input("enter p")

    with open('db_files/project.dat', 'w') as project_file:
        with open('db_files/github_user.dat', 'w') as user_file:
            with open("db_files/commit.dat", 'w') as commit_file:
                for root, dir, files in walk(COMMIT_DATA_DIR):
                    for file in files:
                        fileparts = file.split('#####')
                        name = fileparts[1].split('.csv')[0]
                        id = file.split('.csv')[0]
                        print(id + '\t' + name, file=project_file)
                        for line in open(root + '/' + file):
                            fields = line[:-1].split(',,')
                            hash = fields[0]
                            authorName = fields[1]
                            authorEmail = fields[2]
                            authorTime = fields[3]
                            committerName = fields[4]
                            committerEmail = fields[5]
                            committerTime = fields[6]
                            print('\t'.join([authorEmail, authorName]), file=user_file)
                            print('\t'.join([committerEmail, committerName]), file=user_file)

                            # TODO: Fix placeholder values and dates
                            print('\t'.join([hash, 'placeholder', 'placeholder', id, authorEmail, authorTime, committerEmail, committerTime]), file=commit_file)
    with open('db_files/file_modification.dat', 'w') as mod_file:
        for root, dir, files in walk(MOD_FILES_DIR):
            for file in files:
                for line in open(root + '/' + file):
                    fields = line[:-1].split(',,')
                    hash = fields[0]
                    added = fields[1]
                    deleted = fields[2]
                    filename = fields[3]
                    print('\t'.join([hash, filename, added, deleted]), file=mod_file)

    run(['mysqlimport', '-u' + arg1, '-p' + arg2, '--local', 'github', 'db_files/project.dat'])
    run(['mysqlimport', '-u' + arg1, '-p' + arg2, '--local', 'github', 'db_files/github_user.dat'])
    run(['mysqlimport', '-u' + arg1, '-p' + arg2, '--local', 'github', 'db_files/commit.dat'])
    run(['mysqlimport', '-u' + arg1, '-p' + arg2, '--local', 'github', 'db_files/file_modification.dat'])
