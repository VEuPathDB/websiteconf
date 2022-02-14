#!/bin/env python3

# This script takes the space delimited file master_configuration_set and the
# tsrc manifest, and joins them based on the scm_group column.  You could think
# of it as an sql join where scm_group = tsrc group.
# 
# it outputs a yaml structure for every site/line in master_configuration set.
#
# custom scm config can be specified by giving the value 'custom' for scm_group
# and specifying a filename containing scm yaml in the scm_branch column of
# master_configuration_set

import argparse
import sys
import requests
import ruamel.yaml
import csv

from pathlib import Path
from tsrc.manifest import load_manifest
from copy import deepcopy


def decomment(csvfile):
    """ simple helper function to remove comments from a file """
    for row in csvfile:
        raw = row.split('#')[0].strip()
        if raw: yield row

def get_custom_yaml(f):
    """ get custom yaml from file """
    with open("./{}".format(f),'r') as f:
        data = ruamel.yaml.safe_load(f)

    return data


def main(args):


    # if manifest argument starts with http, fetch file to local .manifest.yml
    # otherwise, read in file at path.
    if args.manifest.startswith('http'):
        resp = requests.get(args.manifest)

        with open('.manifest.yml','w') as f:
            f.write(resp.text)

        manifest_file = '.manifest.yml'

    else:
        manifest_file = args.manifest


    manifest_path = Path(manifest_file)
    manifest = load_manifest(manifest_path)

    # create group_list dict containing a list of repos in each group 
    group_list = {}
    for group in manifest.group_list.groups:
        repo_list = []

        for repo in manifest.get_repos(groups = [group]):
            repo_list.append(
                {'dest': repo.dest,
                 'url': repo.remotes[0].url,
                 'branch': repo.branch,
                 })
        group_list[group] = repo_list


    # create site_config to hold structure for each line/site
    site_config={}
    with open('master_configuration_set') as csvfile:
        reader = csv.DictReader(decomment(csvfile), delimiter = ' ', skipinitialspace=True)
        for row in reader:
            # create key of the site, with dict values of row
            site_config[row['site']] = dict(row)

            # allow overriding of group with custom yaml, with filename
            # specified in scm_branch column
            if row['scm_group'] == 'custom':
                scm_conf = get_custom_yaml(row['scm_branch'])
            else:
                # get scm_conf from tsrc group, update the branch with the one
                # specified in the row
                scm_conf = group_list[row['scm_group']]
                for repo in scm_conf:
                    repo['branch'] = row['scm_branch']

            # we use deepcopy to avoid a reference to scm_conf that would get
            # overwritten on the next loop
            site_config[row['site']]['scm_conf'] = deepcopy(scm_conf)


    output = ruamel.yaml.dump({'site_config': site_config}, default_flow_style=False)
    if args.outfile:
        with open(args.outfile, 'w') as f:
            f.write(output)
    else:
        print(output)

    #print(ruamel.yaml.dump({'site_config': site_config}, default_flow_style=False))
    #print(ruamel.yaml.dump(site_config, default_flow_style=False))


if __name__ == "__main__":
    """ This is executed when run from the command line """

    description = "join master_configuration_set and a tsrc manifest to create a yaml structure"

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("-m", "--manifest",
        action="store",
        dest="manifest",
        default="https://raw.githubusercontent.com/VEuPathDB/tsrc/master/manifest.yml",
        help="specify the path to a tsrc manifest.  If given a url, it will be fetched to '.manifest.yml' and used. (default: %(default)s)")

    parser.add_argument("-o", "--outfile",
        action="store",
        dest="outfile",
        help="specify a file where output will be written.  If unspecified, stdout will be used. (default: %(default)s)")

    args = parser.parse_args()
    main(args)
