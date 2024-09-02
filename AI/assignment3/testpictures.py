from pictures import *

class Test:
    def __init__(self):
        self.picture = Picture()  

    def show_initial_picture(self):
        self.picture.show()
    def show_zip_part(self):
        self.picture.showzip()
    def show_perms(self):
        self.picture.genPerms()
        self.picture.show_perms()
    def deduct_row(self):
        self.picture.deductRow(checkType(0),2)


def run():
    test = Test()
    test.show_initial_picture()
    test.show_zip_part()
    test.show_perms()
    test.deduct_row()

run()