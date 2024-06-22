
import shutil
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "TRUE"
import pygame as pg
pg.init()

from pg_input import Input
from app_loader import get_app

# import app classes
from vos_apps import *
from node_apps import *

# VOS stands for Virtual Operating System
class VOS:
    def __init__(self, res = (1020, 765)):

        self.init_display(res)
 
        self.path = 'files/'
        self.path_tmp = 'tmp/'
        self.path_apps = 'apps/'
        self.path_fonts = 'fonts/'
        
        self.clock = pg.time.Clock()
        self.time = 0 # how many ms since the VOS has started
        
        self.open_with = {}
        # vos.open_with["py"] = <App class instance>
        
        self.running = [] # a list of all apps that are currently running
        self.on_run_funcs = [] # when an app is run, all functions in this list are called with the app as a parameter

        self.input = Input()

        # every call to vos.log is stored here
        self.LOG = ""

        # creates an instance of each app class. This does not "run" the app.
        self.get_apps()

    # FILE OPERATIONS
    # all file operations are done from self.path a.k.a "files/"

    # copies source path (from_) to destination path (to_)
    # works recursively and for files
    def copy(self, from_, to_):
        from_ = self.path + from_
        to_ = self.path + to_
        self.log('copying',from_,'to',to_)
        if not os.path.isdir(to_):
            self.log('destination is not a directory: ',to_)
            return False
        if os.path.exists(from_):
            if os.path.isdir(from_):
                to_ += '/'+from_.split('/')[-1]
                shutil.copytree(from_, to_, dirs_exist_ok = True)
                self.log('successfully copied directory')
            else:
                shutil.copy(from_, to_)
                self.log('successfully copied file')
            return True
        else:
            self.log('source does not exist: ',from_)
            return False

    # lists all of the files in a directory
    def listdir(self, path):
        path = self.path + path
        if os.path.isdir(path):
            return os.listdir(path)
        else:
            return False

    # deletes a file or folder
    def delete(self, path):
        path = self.path + path
        self.log('deleting',path)
        if os.path.exists(path):
            if os.path.isdir(path):
                shutil.rmtree(path)
                self.log('deleted path')
            else:
                os.remove(path)
                self.log('deleted file')
            return True
        else:
            self.log('not found')
            return False

    # saves a file
    def save(self, path, content):
        path = self.path + path
        dest_folder = '/'.join(path.split('/')[:-1])
        if not os.path.exists(dest_folder):
            self.log("destination not found:",dest_folder)
            return False
        with open(path,'w') as f:
            f.write(content)
            self.log("file saved")
            return True

    # creates a folder
    def mkdir(self, path):
        path = self.path + path
        if path[-1] == '/': path = path[:-1]
        dest_folder = '/'.join(path.split('/')[:-1])
        if not os.path.exists(dest_folder):
            self.log("destination not found:",dest_folder)
            return False
        if not os.path.exists(path):
            os.mkdir(path)
            print("made new folder")
        else:
            print("folder already exists")
        return True

    # loads a file and returns string
    def load(self, path):
        path = self.path + path
        if os.path.exists(path):
            with open(path,'r') as f:
                return f.read()
        return False

    # loads a file and returns pg.Surface
    # reccomended to use .convert() or .convert_alpha()
    def load_image(self, path, transparent = False):
        path = self.path + path
        if os.path.exists(path):
            img = pg.image.load(path)
            return img.convert_alpha() if transparent else img.convert()
        return False

    # Opens a file with an App
    # generally will require you to call `app = this.run()` within the app class's open_path function
    def open_with_app(self, path):
        ext = path.split('.')[-1]
        app = self.open_with.get(ext)
        if app:
            app.open_path(path)
        return bool(app)

    # called by apps when they run
    def on_run(self, app):
        for func in self.on_run_funcs:
            func(app)

    # handle creating the pygame window
    def init_display(self, res):
        if res:
            self.res = res
            self.srf = pg.display.set_mode(self.res)
        else:
            self.srf = pg.display.set_mode()
            self.res = self.srf.get_size()

    # adds text to vos.LOG
    # should be used instead of print
    def log(self, *text):
        text = ' '.join(text)
        self.LOG += text + '\n'
        print(text)

    # loads a font from files/fonts/{font_name}.otf
    def load_font(self, name="monospace", size=17):
        return pg.font.Font(self.path + self.path_fonts + name + '.otf', size)

    
    def get_apps(self):
        apps = []
        for app in os.listdir(self.path + self.path_apps):
            p = self.path + self.path_apps + app
            if os.path.isdir(p) and os.path.exists(p+'/app.py'):
                apps.append(get_app(p+'/app.py')(self))
        self.apps = apps

    def get_app(self, name):
        for app in self.apps:
            if app.name == name:
                return app

    def get_running(self, name):
        for app in self.running:
            if app.name == name:
                return app

    def get_all_running(self, name):
        apps = []
        for app in self.running:
            if app.name == name:
                apps.append(app)
        return apps

    def start(self):
        while not self.input.quit:
            self.update()
            self.render()
        for app in self.running:
            app.close()
        pg.display.quit()

    def update(self):
        self.input.update()
        self.delta = self.clock.get_time()
        self.time += self.delta
        for app in self.running:
            if app.active:
                app.update()
        self.clock.tick(60)
        
    def render(self):
        for app in self.running:
            if app.visible:
                if app.active:
                    app.render()
                else:
                    app.idle_render()
        pg.display.update()

if __name__ == "__main__":
    vos = VOS(res=None)
    vos.get_app("Desktop").run()
    vos.start()
