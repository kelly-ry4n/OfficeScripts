

## Define some tests for testscript
import testscript
def test1():
    assert 1 == 1

def test2():
    assert testscript.testfunc() is None

script_1_tests = [test1,test2]

## a list of dictionaries, each defining a script in this directory
officeinfo = [{ ## This is the first script in the folder
                "name"        : "testscript.py",
                "version"     : "0.1",
                "contact"     : "Kelly Ryan - kelly.ry4n@gmail.com",
                "description" : "A test script for admin tools",
                "manual"      : "This script prints testscript.py Script executed!",
                "tests"       : script_1_tests,
                "url"         : "https://github.com/kelly-ry4n/test_script"
            }, { ## This is the second
                "name"        : "testscript2.py",
                "version"     : "0.1",
                "contact"     : "Kelly Ryan - kelly.ry4n@gmail.com",
                "description" : "A short descrition of the second test",
                "manual"      : "Detailed project usage information",
                "tests"       : [], ## No tests for this script. Naughty naughty.
                "url"         : "https://github.com/kelly-ry4n/test_script"
            }]