from vos import *

class MyApp(DictMenuApp):
    def __init__(self, vos):
        super().__init__(vos, "Help", (500, 400))
        self.resizeable = True

        def help_to_options(s):
            opts = {}
            for line in s.split('\n'):
                while line in opts.keys():
                    line += ' '
                opts[line] = None
            return opts
        
        self.tree = {}

        path = self.path+"help_txts/"

        for file in self.vos.listdir(path):
            self.tree[file.split('.')[0]] = help_to_options(
                self.vos.load(path+file))

        for app in self.vos.listdir(self.vos.path_apps):
            helptxt = self.vos.load(
                self.vos.path_apps+app+'/help.txt')
            if helptxt:
                self.tree[app] = help_to_options(helptxt)
