

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "TRUE"
import pygame as pg
pg.init()

from pg_input import Input
from app_loader import get_app
from vos_apps import *
from node_apps import *

import shutil


class VOS:
    def __init__(self, res = (1020, 765)):

        self.init_display(res)
        
        self.path = 'files/'
        self.path_tmp = self.path+'tmp/'
        self.path_apps = self.path+'apps/'
        self.path_fonts = self.path+'fonts/'
        
        self.clock = pg.time.Clock()
        self.time = 0
        
        self.open_with = {}
        self.running = []
        self.on_run_funcs = []

        self.input = Input()

        self.LOG = ""

        self.get_apps()

        self.settings = {}
        
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

    def listdir(self, path):
        path = self.path + path
        if os.path.isdir(path):
            return os.listdir(path)
        else:
            return False

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

    def load(self, path):
        path = self.path + path
        if os.path.exists(path):
            with open(path,'r') as f:
                return f.read()
        return False

    def open_with_app(self, path):
        ext = path.split('.')[-1]
        app = self.open_with.get(ext)
        if app:
            app.open_path(path)
        return bool(app)

    def on_run(self, app):
        for func in self.on_run_funcs:
            func(app)

    def init_display(self, res):
        if res:
            self.res = res
            self.srf = pg.display.set_mode(self.res)
        else:
            self.srf = pg.display.set_mode()
            self.res = self.srf.get_size()

    def log(self, *text):
        text = ' '.join(text)
        self.LOG += text + '\n'
        print(text)
        
    def load_font(self, name="monospace", size=17):
        return pg.font.Font(self.path_fonts + name + '.otf', size)
    
    def get_apps(self):
        apps = []
        for app in os.listdir(self.path_apps):
            p = self.path_apps + app
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
    vos = VOS()
    vos.get_app("Desktop").run()
    vos.start()
