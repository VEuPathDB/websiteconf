# websiteconf

Configuring jenkins built websites at VEuPathDB.

## How to use

### How to update database used by a website
* update master_configuration_set with the new values for the site(s) you need to change
* commit changes


### How to change scm configuration for a website.
* update master_configuration_set with the scm_group (taken from tsrc) and the scm_branch
* if you require a set of branches that are not the same for every repo, specify 'custom' in the scm_group, and a filename in 'scm_branch'.  That file must contain yaml describing the repositories and branches required.
* commit changes


## Details

master_configuration_set is used by conifer when configuring websites during a jenkins build.  As well, even before a site is built, a pipeline job requires a list of repositories to check out.  This repository automates creating a file for this purpose by using groups defined in tsrc (https://github.com/VEuPathDB/tsrc) and the branch specified in master_configuration set. 

### important files
* **make_yaml.py** - This script does the work of joining master_configuration_set, tsrc manifest, and custom scm config to create yaml output for each site.
* **Jenkinsfile** - This configures a jenkins job to run make_yaml.py whenever either this repo, or tsrc is updated.  It makes the produced yaml available to be fetched by website jobs
* **master_configuration_set** - This is a whitespace delemited file containing configuration used for building websites.  It is structured with one site per line, and a column for each configuration parameter.  This makes it very easy to make quick changes to blocks of sites (updating dbs for qa sites, for example)
* **_custom_scm.yml_** - Custom scm configuration can be put in separate files, and referenced in master_configuration_set.  These files will be read by make_yaml.py and combined in the output yaml.
* **requirements.txt** - used to specify requirements when creating a python virtual environment required to run make_yaml.py

