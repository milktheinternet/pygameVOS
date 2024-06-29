from vos import *

class MyApp(WindowApp):
    def __init__(self, vos):
        super().__init__(vos, "Desktop")
        
        self.icons = {}

        self.margin = 10
        self.size = 64
        self.iconFont = self.vos.load_font(size=50)
        self.appbtns = []

        self.minimized = []

        self.desktop = False

    def focus(self):
        for app in self.vos.running:
            app.active = False
        self.active = True
        if self in self.vos.running:self.vos.running.remove(self)
        self.vos.running.insert(0, self)

    def makeIcon(self, name):
        srf = pg.Surface((self.size, self.size))
        srf.blit(self.iconFont.render(name[:2], True, (255,255,255),(0,0,0)),(0,0))
        return srf

    def on_run(self):
        settings = self.vos.get_app("Settings")
        self.bg = eval(settings.get("desktop-background"))
        super().on_run()
        self.prep_app_btns()
        self.vos.on_run_funcs.append(self.on_vos_run)

    def on_vos_run(self, app):
        if 'WindowApp' in app.flags:
            app.on_minimize = self.on_minimize

    def prep_app_btns(self):
        self.appbtns = []
        x,y = self.margin, self.margin
        
        for app in self.vos.apps:
            if not app.desktop:
                continue

            ico_path = self.vos.path+app.path+'icon.png'
            if os.path.exists(ico_path):
                srf = self.vos.load_image(app.path+'icon.png', True)
                srf = pg.transform.smoothscale(srf, (self.size, self.size))
            else:
                print(app.path+'icon.png', 'not found')
                srf = self.makeIcon(app.name)
                
            self.appbtns.append({
                "srf":srf,
                "rect":(x, y, self.size, self.size),
                "app":app,
                "name":app.name
                })
            
            x += self.size + self.margin
            if x + self.size > self.res[0]:
                x = self.margin
                y += self.size + self.margin

    def draw_btns(self):
        for btn in self.appbtns:
            self.srf.blit(btn['srf'], btn['rect'][:2])

    def update(self):
        super().update()
        if not self.active:return
        if self.vos.input.click_inst:
            for btn in self.appbtns:
                if point_within_rect(self.mouse, btn['rect']):
                    btn['app'].run()

    def on_minimize(self, app):
        self.minimized.append(app)
        print('minimized', app.name, self.minimized)

    def render(self):
        self.srf.fill(self.bg)
        self.draw_btns()
        super().render()
    
        
