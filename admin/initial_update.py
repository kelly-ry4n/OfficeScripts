## Once build tools are working, we can do this with just the url

## Each project must have an 'officescript' branch. This is what will be
## fetched.

import admin

initial_projects = [
    ["first_scripts","beta" ,"https://github.com/alouis93/Office-Scripts"],
    ["test_script"  ,"alpha","https://github.com/kelly-ry4n/test_script"],
]

for i in initial_projects:
    name, state, url = *i

    admin.new_project(name, state, url)
    admin.mark_project_dirty(name, state, url)

admin.update_dirty_scripts()
