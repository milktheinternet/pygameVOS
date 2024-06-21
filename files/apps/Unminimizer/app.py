from vos import *

class MyApp(WindowApp):
    def __init__(self, vos):
        self.active = False
        super().__init__(vos, "Unminimizer")

    def on_run(self):
        super().on_run()

        dupes = self.vos.get_all_running(self.name)
        for dupe in dupes:
            if not (dupe is self):
                dupe.close()
        
        self.desk = self.vos.get_running('Desktop')

        dw, dh = self.desk.res
        self.resize((dw-50, dh-50))
        self.srf.set_alpha(200)
        self.desk.active = False
        if not self.desk or not self.desk.minimized:
            print(self.desk)
            print(self.desk.minimized)
            self.close()
        else:
            self.margin = self.desk.margin
            self.size = self.desk.size
            self.draw_minimized()

    def minimize(self):
        self.close()

    def close(self):
        self.desk.active = True
        self.vos.input.click_inst = False
        self.vos.input.on_click.remove(self.on_click)
        super().close()
    
    def draw_minimized(self):
        self.appbtns = []
        x,y = self.margin, self.margin
        
        for app in self.desk.minimized:
            srf = None
            for btn in self.desk.appbtns:
                if btn['name']==app.name:
                    srf = btn['srf']
            if not srf:
                srf = self.desk.makeIcon(self, app.name)
                
            self.srf.blit(srf, (x,y))
            self.appbtns.append({"app":app, "rect":(x,y, self.size, self.size)})
            
            x += self.size + self.margin
            if x + self.size > self.res[0]:
                x = self.margin
                y += self.size + self.margin

        self.base_srf = self.srf.copy()

    def on_click(self):
        clicked_window = super().on_click()
        if clicked_window:
            for btn in self.appbtns:
                if point_within_rect(self.mouse, btn['rect']):
                    btn['app'].focus()
                    self.desk.minimized.remove(btn['app'])
                    self.close()
        return clicked_window
