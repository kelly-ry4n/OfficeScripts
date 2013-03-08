import admin

if __name__ == '__main__':
    name = raw_input("project name: ")
    admin.mark_project_dirty(name)
