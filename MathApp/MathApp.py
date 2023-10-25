from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.spinner import Spinner
import requests

from test_1 import *


API = '3491b25d80fce621ba2ef27a2a67f4d7'

Window.size = (375, 650)

class MainMenu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        line = BoxLayout(orientation = 'vertical', spacing = 10)
        line.padding = (50, 150, 50, 150)

        calculator_btn = Button(text = 'Калькулятор', font_size = 20)
        converter_btn = Button(text = 'Конвертер', font_size = 20)
        timer_btn = Button(text = 'Таймер', font_size = 20)
        stopwatch_btn = Button(text = 'Секундомер', font_size = 20)

        calculator_btn.bind(on_press = self.switch_to_secondary)
        converter_btn.bind(on_press = self.switch_to_secondary)
        timer_btn.bind(on_press = self.switch_to_secondary)
        stopwatch_btn.bind(on_press = self.switch_to_secondary)

        line.add_widget(calculator_btn)
        line.add_widget(converter_btn)
        line.add_widget(timer_btn)
        line.add_widget(stopwatch_btn)

        self.add_widget(line)

    def switch_to_secondary(self, instance):
        screens = {
            'Калькулятор': 'calculator',
            'Конвертер': 'converter',
            'Таймер': 'timer',
            'Секундомер': 'stopwatch'
        }
        self.manager.transition.direction = 'left'
        self.manager.current = screens[instance.text]

class SecondaryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bg_layout = BoxLayout() 

        back_btn = Button(text = 'Назад', size_hint = (None, None), size = (100, 50), font_size = 20)
        back_btn.pos_hint = {'top': 1.0, 'x': 0.0}
        back_btn.bind(on_press = self.switch_to_main)

        self.bg_layout.add_widget(back_btn)
        self.add_widget(self.bg_layout)

    def switch_to_main(self, instances):
        self.manager.transition.direction = 'right'
        self.manager.current = 'main_menu'


class CalculatorScreen(SecondaryScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        axis = BoxLayout(orientation = 'vertical')
        axis.padding = (50, 150, 50, 150)

        self.result = Label(text = '0', size_hint_y = None, height = 100, font_size = 32)
        axis.add_widget(self.result)

        keyboard = GridLayout(cols = 4)

        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-', 
            'C', '0', '=', '+' 
        ]

        for b in buttons:
            temp = Button(text = b, font_size = 26)
            temp.bind(on_press = self.keyboard_press)
            keyboard.add_widget(temp)
        
        axis.add_widget(keyboard)

        self.add_widget(axis)

    def keyboard_press(self, instance):
        current = self.result.text
        btn = instance.text
        if current == '0' or current == 'Ошибка':
            self.result.text = ''
            current = ''

        if btn == '=':
            try:
                self.result.text = str(eval(current))
            except:
                self.result.text = 'Ошибка'
        elif btn == 'C':
            self.result.text = '0'
        else:
            self.result.text = current + btn

class ConverterScreen(SecondaryScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        axis = BoxLayout(orientation = 'vertical', spacing = 10)
        axis.padding = (50, 150, 50, 150)

        
        self.currency = 'USD'

        currency_from_Layout = BoxLayout(
            size_hint = (1, None),
            height = 44
        )

        self.currency_from_spinner = Spinner(
            values = ('USD', 'EUR', 'T', 'RUB'),
            text = 'USD',
            size_hint = (0.6, None),
            height = 44,
            pos_hint = {'center_x': 0.5, 'center_y': 0.5})

        self.currency_from_label = Label(
            text = '0',
            size_hint = (0.4, 1),
            height = 44,
            font_size = 18)


        currency_to_Layout = BoxLayout(
            size_hint = (1, None),
            height = 44
        )
        
        self.currency_to_spinner = Spinner(
            values = ('USD', 'EUR', 'T', 'RUB'),
            text = 'USD',
            size_hint = (0.6, None),
            height = 44,
            pos_hint = {'center_x': 0.5, 'center_y': 0.5})
        
        self.currency_to_label = Label(
            text = '0',
            size_hint = (0.4, 1),
            height = 44,
            font_size = 18)

        convert_btn = Button(
            text = 'Convert',
            size_hint = (1, None),
            size = (200, 44),
            pos_hint = {'center_x': 0.5, 'center_y': 0})
        
        convert_btn.bind(on_press = self.convert)

        keyboard = GridLayout(cols = 3)

        buttons = [
            '7', '8', '9',
            '4', '5', '6',
            '1', '2', '3', 
            '.', '0', 'c', 
        ]

        for b in buttons:
            temp = Button(text = b, font_size = 26)
            temp.bind(on_press = self.keyboard_press)
            keyboard.add_widget(temp)
        
        currency_to_Layout.add_widget(self.currency_to_spinner)
        currency_to_Layout.add_widget(self.currency_to_label)

        currency_from_Layout.add_widget(self.currency_from_spinner)
        currency_from_Layout.add_widget(self.currency_from_label)


        axis.add_widget(currency_from_Layout)
        axis.add_widget(currency_to_Layout)
        axis.add_widget(convert_btn)
        axis.add_widget(keyboard)

        self.add_widget(axis)

    def change_currency(self, instance):
        self.currency = instance.text
        print(self.currency)

    def keyboard_press(self, instance):
        btn = instance.text
        cur_text = self.currency_from_label.text
        if cur_text == '0':
            cur_text = ''
            self.currency_from_label.text = ''
        elif btn == '.' and '.' in cur_text:
            return None
        if btn == 'C':
            self.currency_from_label.text = '0'
        else:
            self.currency_from_label.text = self.currency_from_label.text + btn
    
    def convert(self, instance):
        curr_from = self.currency_from_spinner.text
        curr_to = self.currency_to_spinner.text
        try:
            response = requests.get(f'https://currate.ru/api/?get=rates&pairs={curr_from}{curr_to}&key={API}')
            data = response.json()
            print(data)
            koef = data['data'][curr_from + curr_to]
            print(2)
            result = float(self.currency_from_label.text) * float(koef)
            print(3)
            self.currency_to_label.text = str(round(result, 2))
        except:
            self.currency_to_label.text = 'Ошибка'


class TimerScreen(SecondaryScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        axis = BoxLayout(orientation = 'vertical', spacing = 10)
        axis.padding = (50, 220, 50, 220)

        self.time_left = 0
        self.timer = None
        self.run = False

        self.label = Label(text = '00:00', font_size = 46, size_hint = (1, 0.5))

        plus_sec_btn = Button(text = '+', size_hint = (None, None), size = (50, 30))
        plus_min_btn = Button(text = '+', size_hint = (None, None), size = (50, 30))
        minus_sec_btn = Button(text = '-', size_hint = (None, None), size = (50, 30))
        minus_min_btn = Button(text = '-', size_hint = (None, None), size = (50, 30))

        plus_layout = BoxLayout(
            spacing = 10,
            size_hint = (None, None),
            size = (110, 30),
            pos_hint = {'center_x': 0.5, 'center_y': 0.5})
        plus_layout.add_widget(plus_min_btn)
        plus_layout.add_widget(plus_sec_btn)

        minus_layout = BoxLayout(
            spacing = 10,
            size_hint = (None, None),
            size = (110, 30),
            pos_hint = {'center_x': 0.5, 'center_y': 0.5})
        minus_layout.add_widget(minus_min_btn)
        minus_layout.add_widget(minus_sec_btn)

        self.start_stop_btn = Button(
            text = 'Запуск',
            size_hint = (None, None),
            size = (110, 60),
            pos_hint = {'center_x': 0.5, 'center_y': 0.5})

        plus_sec_btn.bind(on_press = self.plus_sec)
        plus_min_btn.bind(on_press = self.plus_min)
        minus_sec_btn.bind(on_press = self.minus_sec)
        minus_min_btn.bind(on_press = self.minus_min)
        self.start_stop_btn.bind(on_press = self.start_stop)

        axis.add_widget(plus_layout)
        axis.add_widget(self.label)
        axis.add_widget(minus_layout)
        axis.add_widget(self.start_stop_btn)

        self.add_widget(axis)

    def format_time(self, s):
        if s < 0:
            self.time_left = 0
            s = 0
        m, s = divmod(s, 60)
        return f'{m:02}:{s:02}'
        

    def plus_sec(self, instance):
        self.time_left += 1
        self.label.text = self.format_time(self.time_left)

    def plus_min(self, instance):
        self.time_left += 60
        self.label.text = self.format_time(self.time_left)

    def minus_sec(self, instance):
        self.time_left -= 1
        self.label.text = self.format_time(self.time_left)

    def minus_min(self, instance):
        self.time_left -= 60
        self.label.text = self.format_time(self.time_left)

    def start_stop(self, instance):
        if self.run:
            self.start_stop_btn.text = 'Старт'
            self.run = False
            self.timer.cancel()
        else:
            self.start_stop_btn.text = 'Стоп'
            self.run = True
            if self.time_left > 0:
                self.timer = Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, dt):
        self.time_left -= 1
        self.label.text = self.format_time(self.time_left)
        if self.time_left == 0:
            # Clock.unschedule(self.update_timer)
            self.timer.cancel()
            self.start_stop_btn.text = 'Старт'
            self.run = False


class StopwatchScreen(SecondaryScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        axis = BoxLayout(orientation = 'vertical', spacing = 10)
        axis.padding = (50, 150, 50, 150)

        self.time = 0
        self.run = False

        self.label = Label(text = '00:00:00:00', font_size = 32)
        self.reset_btn = Button(text = 'Сброс', font_size = 22, size_hint = (None, None), size = (200, 40), pos_hint = {'center_x': 0.5, 'center_y': 0.5})
        self.start_btn = Button(text = 'Старт', font_size = 22, size_hint = (None, None), size = (200, 40), pos_hint = {'center_x': 0.5, 'center_y': 0.5})
        self.start_btn.bind(on_press = self.start_stop)
        self.reset_btn.bind(on_press = self.reset)

        axis.add_widget(self.label)
        axis.add_widget(self.start_btn)
        axis.add_widget(self.reset_btn)

        self.add_widget(axis)

        Clock.schedule_interval(self.update_time, 0.1)

    def start_stop(self, instance):
        self.run = not self.run
        if self.run:
            self.start_btn.text = 'Стоп'
        else:
            self.start_btn.text = 'Старт'

    def update_time(self, dt):
        if self.run:
            self.time += 1
        self.label.text = str(milliseconds_to_time(self.time*10))

    def reset(self, instance):
        self.run = False
        self.time = 0
        self.label.text = '00:00:00:00'
        self.start_btn.text = 'Старт'


class MathApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenu(name='main_menu'))
        sm.add_widget(CalculatorScreen(name = 'calculator'))
        sm.add_widget(ConverterScreen(name = 'converter'))
        sm.add_widget(TimerScreen(name = 'timer'))
        sm.add_widget(StopwatchScreen(name = 'stopwatch'))

        return sm

app = MathApp()
app.run()