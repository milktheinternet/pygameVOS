from vos import *

class MyApp(NodeApp):
    def __init__(self, vos):
        super().__init__(vos, "start", vos.res)
        
        self.users = os.listdir('users')
        vos.log("USERS:", *self.users)

        self.bg = (100, 100, 100)

    def on_run(self):
        super().on_run()
        self.setup_nodes()

    def confirm_btn(self):
        username = self.username.text
        password = self.password.text
        if username not in self.users:
            self.message.text = "Invalid username. Log in:"
            self.username.text = "USERNAME"
            self.password.text = "PASSWORD-coming soon"
        else:
            self.vos.input.quit = True

            VOS(res=self.vos.res if not self.vos.fullscreen else None, user=username).start()

    def setup_nodes(self):
        W, H = self.vos.res

        self.font = self.vos.load_font(size=32)

        SZ = (W, H//5)
        
        # message
        self.message = TextNode(self, size=SZ,
            pos=(0,0), text="Log in to your account:",
            font=self.font, center=True)
        self.add(self.message)
        # username
        self.username = InputNode(self, size=SZ,
            pos=(0,SZ[1]), font=self.font, center=True,
                                  text="USERNAME")
        self.add(self.username)
        # password
        self.password = InputNode(self, size=SZ,
            pos=(0,SZ[1]*2), font=self.font, center=True,
                                  text="PASSWORD-coming soon")
        self.add(self.password)
        # confirm
        self.confirm = ButtonNode(self, size=SZ,
            pos=(0,SZ[1]*3), text="LOG IN", font=self.font,
            center=True, on_press=self.confirm_btn)
        self.add(self.confirm)
        # new
        self.newuser = ButtonNode(self, size=SZ,
            pos=(0,SZ[1]*4), text="NEW USER-coming soon", font=self.font,
            center=True, on_press=None)
        self.add(self.newuser)

    def render(self):
        self.srf.fill(self.bg)
        self.render_nodes()
        super().render()
