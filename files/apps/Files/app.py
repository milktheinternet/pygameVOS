from vos import *
isdir = os.path.isdir

class MyApp(DictMenuApp):
    def __init__(self, vos):
        super().__init__(vos, "Files", (500, 400))
        self.reset()

    def reset(self):
        self.copied = ""
        self.tree = self.make_options("")

    def save_file(self, path, callback):
        self.on_paste = callback
        self.reset()
        self.copied = "tmp/"+path
        self.tree = self.make_save_options("")

    def copy(self, path):
        self.copied = path
        self.vos.log('copying '+path)

    def on_paste(self, pasted_to):
        print("PASTED!!",pasted_to)
        
    def paste(self, path):
        if not self.copied:return

        self.vos.log('pasting '+self.copied+' to '+path)
        
        self.vos.copy(self.copied, path)

        self.on_paste(path)
        self.update_tree()

    def delete(self, path):
        self.vos.delete(path)
        self.back()
        self.update_tree()

    def update_tree(self):
        self.tree = self.make_options("")

    def rename(self, from_path):
        to_path = '/'.join(from_path.split('/')[:-1])+'/'
        callback = lambda name:(self.vos.rename(from_path, to_path+name), self.update_tree())
        app = PromptApp("prompt", self.vos, f"Rename {from_path}:", callback)
        app.run()
        
    def open_path(self, path):
        self.location = []
        self.tree = self.make_options(path)

    def open_file(self, path):
        for app in self.vos.apps:
            if app.open_path(path):
                return
        self.close()
    
    def make_options(self, path):
        if not path or path[-1] == '/':
            branch = {opt:self.make_options(path + opt) for opt in self.vos.listdir(path)}
            branch["flags"] = ["double_back"]
            return branch
        elif isdir(self.vos.path + path):
            return {
                "open":self.make_options(path+'/'),
                "copy":lambda:self.copy(path),
                "paste":lambda:self.paste(path),
                "delete":lambda:self.delete(path),
                "rename":lambda:self.rename(path)
                }
        else:
            return {
                "open":lambda:self.open_file(path),
                "copy":lambda:self.copy(path),
                "delete":lambda:self.delete(path),
                "rename":lambda:self.rename(path)
                }
    
    def make_save_options(self, path):
        if not path or path[-1] == '/':
            branch = {opt:self.make_save_options(path + opt) for opt in self.vos.listdir(path)}
            branch["flags"] = ["double_back"]
            return branch
        elif isdir(self.vos.path + path):
            return {
                "open":self.make_save_options(path+'/'),
                "save in folder":lambda:(self.paste(path),self.close())
                }
    
    def update(self):
        super().update()
        self.text = '/'.join([self.location[i] for i in range(len(self.location)) if 1 - i % 2])

    
