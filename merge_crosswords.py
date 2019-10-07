import os
import pandas as pd
import json
import sys

def get_user(l, user):
    for elem in l:
        if elem['name'] == user:
            return elem
    raise ValueError()

def read_folder(folder):
    results = []
    fnames = os.listdir(folder)
    for f in fnames:
        if not f.endswith('json'):
            continue
        path = os.path.join(folder, f)
        with open(path) as fin:
            d = json.loads(fin.read())
            results.append(d)
    return results

def count_solved(l):
    solved = [x['finished'] for x in l]
    return sum(solved)

def join_results(results):
    master = {}
    for result in results:
        my_key = list(result.keys())[0]
        if my_key not in master:
            master[my_key] = result[my_key]
            continue
        old_solved = count_solved(master[my_key])
        new_solved = count_solved(result[my_key])
        if new_solved > old_solved:
            master[my_key] = result[my_key]
    return master


def parse_time(s):
    if s is None:
        return None
    my_vars = [int(x) for x in s.split(":")]
    return 60 * my_vars[0] + my_vars[1]


def to_dataframe(master):
    users = [x['name'] for x in master['2019-09-19']]
    table = []
    for k, v in master.items():
        row = [k]
        for user in users:
            my_data = get_user(v, user)
            my_time = my_data['solveTime']
            my_time = parse_time(my_time)
            row.append(my_time)
        table.append(row)
    df = pd.DataFrame(table)
    df.columns = ['Date'] + users
    df = df.sort_values("Date")
    return df


def de_normalize(folder, out_file):
    results = read_folder(folder)
    master = join_results(results)
    df = to_dataframe(master)
    df.to_csv(out_file, index=None)

    html_str = df.to_html()
    out_html_name = out_file[:-4] + ".html"
    with open(out_html_name, 'w') as fout:
        fout.write(html_str)


if __name__ == "__main__":
    de_normalize(sys.argv[1], sys.argv[2])
