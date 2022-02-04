from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.vkeyboard import VKeyboard
from kivy.core.window import Window
from kivy.properties import ObjectProperty

KV= '''

<NumericKeyboardScreen>:
    name:'regitration_window1'
    text_field: text_field
    RelativeLayout:

        MDToolbar:
            title: 'Numeric Keyboard Implementation'
            elevation: 10
            y: self.parent.height - self.height

        MDLabel:
            text: 'Number TextField'
            font_size: 15
            y: self.parent.height - self.height - dp(90)
            pos_hint :{'center_x':0.5}
            halign: 'center'
            size_hint_y: None
            height: dp(20)

        MDTextField:
            id: text_field
            hint_text: 'For Eg:- 987654321'
            y: self.parent.height - self.height - dp(135)
            pos_hint :{'center_x':0.5}
            size_hint_x : 0.35
            mode: 'rectangle'
            input_filter: 'int'
            on_focus: root.set_layout(keyboard_anchor, self)


        RelativeLayout:
            id: keyboard_anchor
            size_hint_y: 0.5

WindowManager:
    NumericKeyboardScreen:
        id: key_num
'''

class WindowManager(ScreenManager):
    pass

class NumericKeyboardScreen(MDScreen):
    focus_count = 0
    def set_layout(self, keyboard_anchor, target_textfield):
        self.focus_count += 1
        v_keyboard = NumericKeyboard(
            text_field = target_textfield
        )
        keyboard_anchor.clear_widgets()
        keyboard_anchor.add_widget(v_keyboard)

        if self.focus_count == 2:
            keyboard_anchor.clear_widgets()
            self.focus_count = 0


class NumericKeyboard(VKeyboard):
    text_field = ObjectProperty()
    custom_vk_layout = ObjectProperty('numeric.json')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.available_layouts['numpad'] = self.custom_vk_layout
        self.layout = self.custom_vk_layout
        self.pos_hint = {'center_x': 0.5}

    def on_key_down(self, keyboard, keycode, text, *args):
        """ The callback function that catches keyboard events. """

        if isinstance(keycode, tuple):
            keycode = keycode[1]

        if keycode == "bs":
            if len(textfield_data) > 0:
                self.text_field.text = textfield_data[:-1]
        else:
            self.text_field.text += u"{0}".format(keycode)


    def on_key_up(self, keyboard, keycode, *args):
        """ The callback function that catches keyboard events. """
        textfield_data = self.text_field.text

        if isinstance(keycode, tuple):
            keycode = keycode[1]

        if keycode == "bs":
            if len(textfield_data) > 0:
                self.text_field.text = textfield_data[:-1]
        else:
            self.text_field.text += u"{0}".format(keycode)


    def _keyboard_close(self, *args):
        """ The active keyboard is being closed. """
        if self._keyboard:
            self._keyboard.unbind(on_key_down=self.key_down)
            self._keyboard.unbind(on_key_up=self.key_up)
            self._keyboard = None

class MainApp(MDApp):
    def build(self):
        return Builder.load_string(KV)


if __name__ == '__main__':
    MainApp().run()
