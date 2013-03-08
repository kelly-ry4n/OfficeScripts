import admin

name = raw_input("Project/Folder Name: ")
state= raw_input("State (alpha | beta | release): ")
url  = raw_input("Github url: ")

admin.new_project(name,state,url)