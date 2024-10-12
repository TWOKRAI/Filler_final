class WindowManager:
    def __init__(self):
        self.initialize_windows()
        

    def initialize_windows(self):
        from Filler_interface.Window_start.start_conrtol import window_start
        self.window_start = window_start

        from Filler_interface.Window_datetime.datetime_control import window_datetime
        self.window_datetime = window_datetime

        from Filler_interface.Window_pop_up.pop_up_control import window_pop_up
        self.window_pop_up = window_pop_up

        from Filler_interface.Window_low.low_control import window_low
        self.window_low = window_low

        from Filler_interface.Window_main.main_filler_conrtol import main_filler_window
        self.window_main_filler = main_filler_window

        from Filler_interface.Window_list1.list1_control import window_list1
        self.window_list1 = window_list1

        from Filler_interface.Window_statistic.statistic_control import window_statistic
        self.window_statistic = window_statistic

        from Filler_interface.Window_settings1.settings_control2 import window_setting1
        self.window_settings1 = window_setting1

        from Filler_interface.Window_settings2.settings2_control import window_setting2
        self.window_settings2 = window_setting2

        from Filler_interface.Window_prepare.prepare_control import window_prepare
        self.window_prepare = window_prepare

        from Filler_interface.Window_view.view_conrtol import window_view
        self.window_view = window_view

        from Filler_interface.Window_error.error_conrtol import window_error
        self.window_error = window_error

        from Filler_interface.Window_cip.cip_control2 import window_cip
        self.window_cip = window_cip

        from Filler_interface.Window_robot.robot_control import window_robot
        self.window_robot = window_robot

        from Filler_interface.Window_filler.filler_conrtol import filler_window
        self.window_filler = filler_window

    def show_initial_windows(self):
        self.window_low.show()
        self.window_start.show_animation()

    def set_fullscreen(self, fullscreen):
        if fullscreen:
            self.window_start.fullscreen()
            self.window_datetime.fullscreen()
            self.window_low.fullscreen()
            self.window_main_filler.fullscreen()
            self.window_list1.fullscreen()
            self.window_statistic.fullscreen()
            self.window_settings1.fullscreen()
            self.window_settings2.fullscreen()
            self.window_prepare.fullscreen()
            self.window_view.fullscreen()
            self.window_filler.fullscreen()
            self.window_error.fullscreen()
            self.window_cip.fullscreen()
            self.window_robot.fullscreen()

    def hide_datetime_window(self):
        self.window_datetime.hide()

    def show_datetime_window(self):
        self.window_datetime.show_window()

    def set_language(self, lang_num):
        self.window_main_filler.language(lang_num)
        self.window_list1.language(lang_num)
        self.window_statistic.language(lang_num)
        self.window_settings1.language(lang_num)
        self.window_settings2.language(lang_num)
        self.window_prepare.language(lang_num)
        self.window_filler.language(lang_num)
        self.window_cip.language(lang_num)
        self.window_robot.language(lang_num)
        self.window_pop_up.language(lang_num)
        self.window_error.language(lang_num)

    def recolor_icons(self):
        self.window_main_filler.set_icons()
        self.window_list1.set_icons()
        self.window_settings1.set_icons()
        self.window_settings2.set_icons()
        self.window_statistic.set_icons()
        self.window_cip.set_icons()
        self.window_robot.set_icons()

    def close_windows(self, window_focus):
        if window_focus != self.window_start.window_name:
            self.window_start.hide()
            #print(f'close: {self.window_start.window_name}')

        if window_focus != self.window_datetime.window_name:
            self.window_datetime.hide()
            #print(f'close: {self.window_datetime.window_name}')

        if window_focus != self.window_main_filler.window_name:
            self.window_main_filler.hide()
            #print(f'close: {self.window_main_filler.window_name}')

        if window_focus != self.window_list1.window_name:
            self.window_list1.hide()
            #print(f'close: {self.window_list1.window_name}')

        if window_focus != self.window_statistic.window_name:
            self.window_statistic.hide()
            #print(f'close: {self.window_statistic.window_name}')

        if window_focus != self.window_settings1.window_name:
            self.window_settings1.hide()
            #print(f'close: {self.window_settings1.window_name}')

        if window_focus != self.window_settings2.window_name:
            self.window_settings2.hide()
            #print(f'close: {self.window_settings2.window_name}')

        if window_focus != self.window_prepare.window_name:
            self.window_prepare.hide()
            #print(f'close: {self.window_prepare.window_name}')

        if window_focus != self.window_view.window_name:
            self.window_view.close()
            #print(f'close: {self.window_view.window_name}')

        if window_focus != self.window_filler.window_name:
            self.window_filler.hide()
            #print(f'close: {self.window_filler.window_name}')

        if window_focus != self.window_error.window_name:
            self.window_error.hide()
            #print(f'close: {self.window_error.window_name}')

        if window_focus != self.window_cip.window_name:
            self.window_cip.hide()
            #print(f'close: {self.window_cip.window_name}')

        if window_focus != self.window_robot.window_name:
            self.window_robot.hide()
            #print(f'close: {self.window_robot.window_name}')

    def show_window(self, window_focus):
        match window_focus:
            case self.window_start.window_name:
                self.window_start.hide()
                self.window_start.show()

            case self.window_main_filler.window_name:
                self.window_main_filler.hide()
                self.window_main_filler.show()

            case self.window_list1.window_name:
                self.window_list1.show()

            case self.window_statistic.window_name:
                self.window_statistic.hide()
                self.window_statistic.show()

            case self.window_settings1.window_name:
                self.window_settings1.hide()
                self.window_settings1.show()

            case self.window_settings2.window_name:
                self.window_settings2.hide()
                self.window_settings2.show()

            case self.window_prepare.window_name:
                self.window_prepare.hide()
                self.window_prepare.show()

            case self.window_view.window_name:
                self.window_view.close(1)
                self.window_view.show()

            case self.window_filler.window_name:
                self.window_filler.hide()
                self.window_filler.show()

            case self.window_error.window_name:
                self.window_error.hide()
                self.window_error.show()

            case self.window_cip.window_name:
                self.window_cip.hide()
                self.window_cip.show()

            case self.window_robot.window_name:
                self.window_robot.hide()
                self.window_robot.show()
