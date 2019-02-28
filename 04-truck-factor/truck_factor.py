import pandas as pd
from statistics import median
from sys import argv

if __name__ == '__main__':
    input_file = argv[1]
    file_tf_output = argv[2]
    project_tf_output = argv[3]
    raw_data = pd.read_csv(input_file)

    raw_dict = {}
    tf_dict = {}
    for row in raw_data.values:
        projectID = row[0]
        file = row[3]
        changes = row[4] + row[5]

        try:
            raw_dict[projectID][file].append(changes)
        except KeyError:
            try:
                raw_dict[projectID][file] = [changes]
                tf_dict[projectID][file] = 0
            except KeyError:
                raw_dict[projectID] = {file: [changes]}
                tf_dict[projectID] = {file: 0}

    for project in raw_dict.keys():
        for filename in raw_dict[project].keys():
            changelist = raw_dict[project][filename]
            raw_dict[project][filename] = (sum(changelist), sorted(changelist))

    truck_factor = 1
    while truck_factor < 100:
        for project in raw_dict.keys():
            for filename in raw_dict[project].keys():
                total_changes, changelist = raw_dict[project][filename]
                if len(changelist) > 0:
                    biggest_change = changelist.pop()
                    if total_changes == 0:
                        changes_left = 0
                    else:
                        changes_left = sum(changelist) / total_changes
                    if changes_left < .5:
                        tf_dict[project][filename] = truck_factor
                        raw_dict[project][filename] = (total_changes, [])
        truck_factor += 1

    proj_tf_dict = {}
    with open(file_tf_output, 'w') as output_file:
        print("project,file,factor", file=output_file)
        for proj, p_dict in tf_dict.items():
            tf_list = []
            for file, tf in p_dict.items():
                tf_list.append(tf)
                print(proj + "," + file + "," + str(tf), file=output_file)
            proj_tf_dict[proj] = median(tf_list)

    with open(project_tf_output, 'w') as output_file:
        print("project,factor", file=output_file)
        for project, tf in proj_tf_dict.items():
            print(project + "," + str(tf), file=output_file)


