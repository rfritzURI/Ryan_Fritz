# 1. Simple directory tree
# Replicate this tree of directories and subdirectories:

# ├── draft_code
# |   ├── pending
# |   └── complete
# ├── includes
# ├── layouts
# |   ├── default
# |   └── post
# |       └── posted
# └── site

# 1. Using os.system or os.mkdirs replicate this simple directory tree.
# 2. Delete the directory tree without deleting your entire hard drive

import os
path = "C:\RyanGIS\Class_3\Coding_Challenge_3\my_directory3"
os.mkdir(path)
# Tree folders
branch_one = ["draft_code", "includes", "layouts", "site"]
branch_two_draft_code = ["pending", "complete"]
branch_two_layouts = ["default", "post"]
branch_three_post = ["posted"]

# Joining tree folders
for branch in branch_one:
    os.mkdir(os.path.join(path, branch))

for branch in branch_two_draft_code:
    os.mkdir(os.path.join(path, "draft_code", branch))

for branch in branch_two_layouts:
    os.mkdir(os.path.join(path, "layouts", branch))

for branch in branch_three_post:
    os.mkdir(os.path.join(path, "posted", branch))

import shutil
shutil.rmtree(path)


