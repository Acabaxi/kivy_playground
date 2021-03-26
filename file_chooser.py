from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.filechooser import FileChooserIconView

Builder.load_string("""
<MyWidget>:
    id: my_widget
    FileChooserIconView:
        id: filechooser
        path: my_widget.set_path()
        on_selection: my_widget.selected(filechooser.selection)
        size_hint_x: 1
    Image:
        id: image
        source: ""

""")


class MyWidget(BoxLayout):

    def selected(self,filename):
        try:
            self.ids.image.source = filename[0]
        except:
            pass

    def set_path(self):
        return "/home/pedro"


class MyApp(App):
    def build(self):
        return MyWidget()

if __name__ == '__main__':
    MyApp().run()