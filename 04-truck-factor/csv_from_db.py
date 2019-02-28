from MySQLdb import connect
from sys import argv

SQL = "select p.id, c.hash, c.committer, m.file, m.added, m.deleted " \
      "from project p join commit c join file_modification m " \
      "on p.id = c.projectID " \
      "and c.hash = m.hash"

if __name__ == '__main__':
    output_fp = argv[1]
    db = connect(host='127.0.0.1',  passwd="",db="github2")
    c = db.cursor()
    results = c.execute(SQL)
    with open(output_fp, 'w') as output_file:
        print("projectID,hash,committer,file,added,deleted", file=output_file)
        for row in c.fetchall():
            projectID = row[0].replace(',', '')
            hash = row[1].replace(',', '')
            committer = row[2].replace(',', '')
            file = row[3].replace(',', '')
            added = row[4]
            deleted = row[5]
            print(','.join([projectID, hash, committer, file, str(added), str(deleted)]), file=output_file)

