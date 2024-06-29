from vos import *

# SETTINGS APP
class MyApp(WindowApp):
    def __init__(self, vos):
        super().__init__(vos, "Settings", (600,400))
        self.settings_path = vos.path+self.path+"settings.json"
        vos.log("SETTINGS PATH:",self.settings_path)
        
    @property
    def json(self):
        return eval(open(self.settings_path).read())
    
    def get(self, key):
        return self.json.get(key)

    def set(self, key, value):
        json = self.json
        json[key] = value
        self.set_json(json)

    def remove(self, key):
        json = self.json
        if key in json.keys():
            del json[key]
            self.set_json(json)

    def set_json(self, json):
        s = "{\n"
        for key, value in json.items():
            s += f"'{key}':'{value}',\n"
        s += "}\n"
        with open(self.settings_path,'w') as f: f.write(s)

    def on_run(self):
        super().on_run()
        self.idx = 0
        self.cache_json = self.json
        self.font = self.vos.load_font(size=15)
        self.line_height = 20
        self.redraw()
        
    def get_key(self, idx):
        return list(self.cache_json.keys())[idx]

    @property
    def current_key(self):
        return self.get_key(self.idx)

    def update(self):
        super().update()
        inp = self.vos.input

        changed = False
        if pg.K_UP in inp.keys_inst:
            self.idx -= 1
            changed = True
        if pg.K_DOWN in inp.keys_inst:
            self.idx += 1
            changed = True

        if changed:
            self.idx %= len(self.cache_json)
            self.redraw()
        
        if pg.K_RETURN in inp.keys_inst:
            if pg.K_LSHIFT in inp.keys or \
               pg.K_RSHIFT in inp.keys: # hold shift to create a new setting
                def callback(key):
                    def callback2(value):
                        self.set(key, value)
                        self.cache_json = self.json
                        self.redraw()
                        self.focus()
                    prompt = f'Set a value for "{key}":'
                    self.vos.get_app("Prompt").run(callback2, prompt)
                prompt = 'Create a new setting:'
            else:
                def callback(text):
                    self.set(self.current_key, text)
                    self.cache_json = self.json
                    self.redraw()
                    self.focus()
                prompt = f'Set a value for "{self.current_key}":'
            self.vos.get_app("Prompt").run(callback, prompt)

    def redraw(self):
        self.srf.fill((0,0,0))
        y2=0
        if self.idx > self.res[1]//self.line_height:
            y2 = - self.idx * self.line_height
            
        for y in range(len(self.cache_json)):
            key = self.get_key(y)
            text = f'{key}: {self.cache_json.get(key)}'
            text = self.font.render(text, True, (255,255,0) if y==self.idx else (255,255,255), (0,0,0))
            self.srf.blit(text, (0, y2))
            y2 += self.line_height
