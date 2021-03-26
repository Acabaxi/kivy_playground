import kivy
kivy.require('1.0.6')

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton

from kivy.uix.anchorlayout import AnchorLayout

from kivy.uix.screenmanager import ScreenManager, Screen

patient_id = -1
patient_uf = -1


class LoginScreen(GridLayout):

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 2

        username_ti = TextInput(multiline=False, hint_text='Patient ID', halign='center', size_hint=(None,None), width=200, height=80)
        username_ti.bind(text=self.on_text)
        username_anchor_layout = AnchorLayout(anchor_x='center')
        self.username = username_ti
        username_anchor_layout.add_widget(self.username)
        self.add_widget(username_anchor_layout)

        # self.add_widget(self.username)
        #########
        sd_btn = ToggleButton(text='From SD card', group='input_media', size_hint=(None, None), width=self.width,
                              height=self.height)
        anchor_layout = AnchorLayout(anchor_x='center')
        anchor_layout.add_widget(sd_btn)
        self.add_widget(anchor_layout)

        ###########
        uf_count_ti = TextInput(multiline=False, hint_text='Patient ID', halign='center', size_hint=(None,None), width=200, height=80)
        uf_count_ti.bind(text=self.on_text)
        uf_count_anchor_layout = AnchorLayout(anchor_x='center')
        self.uf_count_ti = uf_count_ti
        uf_count_anchor_layout.add_widget(self.uf_count_ti)
        self.add_widget(uf_count_anchor_layout)

        # self.password = TextInput(password=True, multiline=False)
        # self.add_widget(self.password)

        ###########
        camera_btn = ToggleButton(text='From camerea', group='input_media',size_hint=(None, None), width=self.width,
                              height=self.height)
        anchor_camera_layout = AnchorLayout(anchor_x='center')
        anchor_camera_layout.add_widget(camera_btn)
        self.add_widget(anchor_camera_layout)

        ##########
        self.add_widget(Label())

        #######333
        proceed_button = Button(size_hint=(None,None), width=50, height=50)
        anchor_proceed_layout = AnchorLayout(anchor_x='right', anchor_y='bottom')
        anchor_proceed_layout.add_widget(proceed_button)
        self.add_widget(anchor_proceed_layout)

    def on_text(self, instance, value):
        print("TExt is", value)


class GridLayoutScreen(Screen):
    def __init__(self, **kwargs):
        super(GridLayoutScreen, self).__init__(**kwargs)
        self.add_widget(LoginScreen())


class LabelScreen(Screen):
    def __init__(self, **kwargs):
        super(LabelScreen, self).__init__(**kwargs)
        self.add_widget(Label())

class MyApp(App):
    #
    # def build(self):
    #     return LoginScreen()
    def build(self):
        sm = ScreenManager()
        # sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(GridLayoutScreen(name='settings'))
        sm.add_widget(LabelScreen(name='settings'))

        return sm

if __name__ == '__main__':
    MyApp().run()


