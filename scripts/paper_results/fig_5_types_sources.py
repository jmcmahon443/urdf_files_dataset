import json
import pandas as pd
from helper_functions import _get_files_with, _get_subdirectories

def _extract_meta_information(filename, columns):
    meta_infos = pd.DataFrame(columns=columns)
    with open(filename, 'r') as f:
        data = json.load(f)
    robots = data['robots']
    for robot in robots:
        meta_infos = pd.concat([meta_infos, pd.Series({'name':robot['name'], 'type': robot['type']}).to_frame().T], ignore_index=True)
    return meta_infos

def _extract_source_information(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data['source']

####

dataframe_columns = ['type','source']
dataset_information = pd.DataFrame(columns=dataframe_columns)

meta_info_filename = "meta-information.json"
source_info_filename = "source-information.json"

dir = "urdf_files"
subdirs = _get_subdirectories(dir)

for d in subdirs:
    list_of_meta_file_paths = _get_files_with(d, meta_info_filename)
    list_of_source_file_paths = _get_files_with(d, source_info_filename)
    assert len(list_of_source_file_paths) == 1, f"Error, expecting one source information file in subdataset, but found either more or none: {list_of_source_file_paths}"
    for file in list_of_meta_file_paths:
        meta_infos = _extract_meta_information(file, dataframe_columns)
        meta_infos['source'] = _extract_source_information(list_of_source_file_paths[0])
        dataset_information = pd.concat([dataset_information, meta_infos], ignore_index=True)

types_sources = pd.DataFrame(dataset_information.groupby(['type','source']).count())
types_sources = types_sources.reset_index().rename({'name':'count'},axis='columns')

types_sources.to_csv("fig_5_types_sources.csv",index=False)