import os
import pandas as pd
import json
import sys
import seaborn as sns

name_map = {
    "hannahyouakim": "hannahy",
    "hewy": "hannahy"
}

always_include_users = set(["Steinbach", "GravyBaby", "flipperkid"])

PENALTY_TIME=250

def get_user(l, user):
    for elem in l:
        if elem['name'] == user:
            return elem
    return {
        "solveTime": None
    }


def update_usernames(d):
    for k,v in d.items():
        for elem in v:
            if elem['name'] not in name_map:
                continue
            elem['name'] = name_map[elem['name']]


def read_folder(folder):
    results = []
    fnames = os.listdir(folder)
    for f in fnames:
        if not f.endswith('json'):
            continue
        path = os.path.join(folder, f)
        with open(path) as fin:
            d = json.loads(fin.read())
            update_usernames(d)
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


def get_all_users(master):
    users = set()
    for k, v in master.items():
        day_users = [x['name'] for x in v]
        users.update(day_users)
    return sorted(list(users))


def remove_users_from_df(df, users):
    columns = df.columns.values.tolist()
    good_users = []
    for user in users:
        if user in always_include_users:
            good_users.append(user)
            continue
        count_all = len(df[user])
        count_bad = sum(df[user].isna())
        if count_bad / count_all < 0.4:
            good_users.append(user)
    print(good_users)
    df = df[['Date'] + good_users]
    return df


def to_dataframe(master):
    users = get_all_users(master)
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
    df = remove_users_from_df(df, users)
    df = df.sort_values("Date", ascending=False)
    return df


def to_html(df, out_file):
    #df = df.fillna(PENALTY_TIME)
    df.index = df['Date']
    df = df[df.columns.values.tolist()[1:]]
    with pd.option_context('display.precision', 0):
        s = df.style.background_gradient(cmap='coolwarm', axis=1).highlight_null(null_color='white')
        html_str = s.render()
        out_html_name = out_file[:-4] + ".html"
        with open(out_html_name, 'w') as fout:
            fout.write(html_str)


def de_normalize(folder, out_file):
    results = read_folder(folder)
    master = join_results(results)
    df = to_dataframe(master)
    df.to_csv(out_file, index=None)
    to_html(df, out_file)


if __name__ == "__main__":
    de_normalize(sys.argv[1], sys.argv[2])
