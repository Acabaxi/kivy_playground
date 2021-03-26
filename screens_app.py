import kivy
kivy.require('1.0.6')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

Builder.load_string("""
<MenuScreen>:
    BoxLayout:
        Button:
            text: 'Goto settings'
            on_press: 
                root.manager.current = 'settings'
                root.manager.transition.direction = 'right'
        Button:
            text: 'Quit'

<SettingsScreen>:
    BoxLayout:
        Button:
            text: 'My settings button'
        Button:
            text: 'Back to menu'
            on_press: 
                root.manager.current = 'menu'
                root.manager.transition.direction = 'left'
""")

class MenuScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

class ScreenApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(SettingsScreen(name='settings'))

        return sm


if __name__ == '__main__':

    ScreenApp().run()
