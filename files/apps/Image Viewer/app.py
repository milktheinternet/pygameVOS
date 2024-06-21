from vos import *

class MyApp(WindowApp):
    def __init__(self, vos):
        super().__init__(vos, "Image Viewer", (100, 100))
        self.desktop = False
        for ext in 'png jpg jpeg'.split():
            self.vos.open_with[ext] = self

    def open_path(self, path):
        app = self.run()
        img = self.vos.load_image(path)
        app.resize(img.get_size())
        app.srf = img
