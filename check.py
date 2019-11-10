import json
import os
from datetime import datetime
from collections import Counter

config = json.load(open("config.json"))

def get_file_list(path_list,ext_list):
    # r=root, d=directories, f = files
    files = []
    not_used_files = []
    not_used_extensions = set()
    for path in path_list:
        for r, d, f in os.walk(path):
            for file in f:
                if('.' in file):
                    ext = file.split('.')[-1]
                    if(ext in ext_list):
                        files.append(os.path.join(r, file))
                    else:
                        not_used_files.append(os.path.join(r, file))
                        not_used_extensions.add(ext)
                else:
                    not_used_files.append(os.path.join(r, file))
    return files,not_used_files,not_used_extensions

def get_modifications_times(file_list):
    mod_times = []
    for file in files:
        timestamp = os.path.getmtime(file)
        dt = datetime.fromtimestamp(timestamp)
        mod_times.append(dt)
    return mod_times


def get_duplicate_timestamp_files(mod_times,files):
    res = []
    mod_count = Counter(mod_times)
    timestamp_more_than_one = [k for k, v in mod_count.items() if v > 1]
    #print(f" duplicate times files:")
    for timestamp in timestamp_more_than_one:
        ts_res = {}
        ts_res["ts"] = timestamp
        ts_res["indexes"] = []
        #print(f"duplicate : {timestamp}")
        for index,mod_time in enumerate(mod_times):
            if(mod_time == timestamp):
                ts_res["indexes"].append(index)
                #print(f"  duplicate modif time : {files[index]}", end='')
                #print(f"size = {os.path.getsize(files[index])}")
        res.append(ts_res)
    return res

def print_duplicate_timestamp_files(dup_ts_indexes):
    print(f" duplicate times files:")
    for duplicate in dup_ts_indexes:
        print(f"duplicate : {duplicate['ts']}")
        for index in duplicate['indexes']:
            print(f"  duplicate modif index : {files[index]}", end='')
            print(f" size = {os.path.getsize(files[index])}")
    return

def print_duplicate_ts_samesize(dup_ts_indexes):
    print(f" duplicate time stamps with same size:")
    for duplicate in dup_ts_indexes:
        sizes = []
        for index in duplicate['indexes']:
            sizes.append(os.path.getsize(files[index]))
        duplicate_count = Counter(sizes)
        size_more_than_one = [k for k, v in duplicate_count.items() if v > 1]
        for sz in size_more_than_one:
            print(f"duplicates:")
            for index in duplicate['indexes']:
                size = os.path.getsize(files[index])
                if(sz == size):
                    print(f"  {files[index]}")


#------------------------------------------------------------------------------------------------------

files, not_used_files, not_used_extensions = get_file_list(config["paths"],config["extensions"])

print(f"Matching {len(files)} files")
print(f"non matching extensions {len(not_used_files)} files : {not_used_extensions}")

mod_times = get_modifications_times(files)

dup_ts_indexes = get_duplicate_timestamp_files(mod_times,files)

print_duplicate_ts_samesize(dup_ts_indexes)
