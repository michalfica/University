from pictures import *

if __name__ == '__main__':
    try:
        p = Picture()
        p.genPerms()
        p.deductAll()
        p.backtrack()
        p.saveOtput()
    except Exception as e:
        print("Problem during try?Impossible constraints")
        print(e)