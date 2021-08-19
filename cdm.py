#! /usr/bin/python3

import math
import threading
import pygame
from tkinter import *
from glob import glob
from os import path
from inputs import get_gamepad, UnpluggedError

# Where the .wav files are kept:
SAMPLES_DIR = './samples'


A = 'BTN_SOUTH'
B = 'BTN_EAST'
X = 'BTN_WEST'
Y = 'BTN_NORTH'
LB = 'BTN_TL'
RB = 'BTN_TR'
LT = 'ABS_Z'
RT = 'ABS_RZ'
LS_X = 'ABS_X'
LS_Y = 'ABS_Y'
LS_BTN = 'BTN_THUMBL'
RS_X = 'ABS_RX'
RS_Y = 'ABS_RY'
RS_BTN = 'BTN_THUMBR'
SELECT = 'BTN_SELECT'
START = 'BTN_START'
DPAD_UP = 'ABS_HAT0Y'
DPAD_DOWN = 'ABS_HAT0Y'
DPAD_LEFT = 'ABS_HAT0X'
DPAD_RIGHT = 'ABS_HAT0X'

ALL_BUTTONS = [A, B, X, Y, LB, RB, LS_BTN, RS_BTN, SELECT, START, DPAD_UP, DPAD_DOWN, DPAD_LEFT, DPAD_RIGHT, LT, RT]
ALL_INPUTS = ALL_BUTTONS + [LT, RT, LS_X, LS_Y, RS_X, RS_Y]

sound_map = {}

sound_files = glob(f"{SAMPLES_DIR}/*.wav")
options_map = {}
for sound_file in sound_files:
    options_map[path.basename(sound_file)] = sound_file

SOUND_OPTIONS = options_map


class XboxController(object):
    MAX_TRIG_VAL = math.pow(2, 8)
    MAX_JOY_VAL = math.pow(2, 15)

    def __init__(self):
        self.LeftJoystickY = 0
        self.LeftJoystickX = 0
        self.RightJoystickY = 0
        self.RightJoystickX = 0
        self.LeftTrigger = 0
        self.RightTrigger = 0
        self.LeftBumper = 0
        self.RightBumper = 0
        self.A = 0
        self.X = 0
        self.Y = 0
        self.B = 0
        self.LeftThumb = 0
        self.RightThumb = 0
        self.Back = 0
        self.Start = 0
        self.LeftDPad = 0
        self.RightDPad = 0
        self.UpDPad = 0
        self.DownDPad = 0

        self._monitor_thread = threading.Thread(target=self._monitor_controller, args=())
        self._monitor_thread.daemon = True
        self._monitor_thread.start()

        #self._monitor_thread_debug = threading.Thread(target=self._monitor_controller_debug, args=())
        #self._monitor_thread_debug.daemon = True
        #self._monitor_thread_debug.start()


    def read(self):
        return [
            self.LeftJoystickY,
            self.LeftJoystickX,
            self.RightJoystickY,
            self.RightJoystickX,
            self.LeftTrigger,
            self.RightTrigger,
            self.LeftBumper,
            self.RightBumper,
            self.A,
            self.X,
            self.Y,
            self.B,
            self.LeftThumb,
            self.RightThumb,
            self.Back,
            self.Start,
            self.LeftDPad,
            self.RightDPad,
            self.UpDPad,
            self.DownDPad,
        ]

    def _monitor_controller(self):
        try:
            get_gamepad()
        except UnpluggedError:
            print("[!] Error: No controller found.  Exiting.")
            exit(1)
        while True:
            # get_gamepad() returns list of 1 input event
            event = get_gamepad()[0]
            if event.state:
                play_sound_for_button(event.code)

    def _monitor_controller_debug(self):
        while True:
            events = get_gamepad()
            for event in events:
                if event.code == 'ABS_Y':
                    self.LeftJoystickY = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_X':
                    self.LeftJoystickX = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_RY':
                    self.RightJoystickY = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_RX':
                    self.RightJoystickX = event.state / XboxController.MAX_JOY_VAL # normalize between -1 and 1
                elif event.code == 'ABS_Z':
                    self.LeftTrigger = event.state / XboxController.MAX_TRIG_VAL # normalize between 0 and 1
                elif event.code == 'ABS_RZ':
                    self.RightTrigger = event.state / XboxController.MAX_TRIG_VAL # normalize between 0 and 1
                elif event.code == 'BTN_TL':
                    self.LeftBumper = event.state
                elif event.code == 'BTN_TR':
                    self.RightBumper = event.state
                elif event.code == 'BTN_SOUTH':
                    self.A = event.state
                elif event.code == 'BTN_NORTH':
                    self.X = event.state
                elif event.code == 'BTN_WEST':
                    self.Y = event.state
                elif event.code == 'BTN_EAST':
                    self.B = event.state
                elif event.code == 'BTN_THUMBL':
                    self.LeftThumb = event.state
                elif event.code == 'BTN_THUMBR':
                    self.RightThumb = event.state
                elif event.code == 'BTN_SELECT':
                    self.Back = event.state
                elif event.code == 'BTN_START':
                    self.Start = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY1':
                    self.LeftDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY2':
                    self.RightDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY3':
                    self.UpDPad = event.state
                elif event.code == 'BTN_TRIGGER_HAPPY4':
                    self.DownDPad = event.state


def set_sound_map(button, sound):
    print("DEBUG:", button, sound)
    sound_map[button] = sound


def play_sound_for_button(code):
    #print("DEBUG:", code)
    sound = SOUND_OPTIONS.get(sound_map.get(code))
    if sound:
        pygame.mixer.Sound(sound).play()


def main():
    pygame.mixer.init()
    #joy = XboxController()
    XboxController()
    master = Tk()

    menu_button_map = {}
    for button in ALL_BUTTONS:
        variable = StringVar(master, name=button)
        variable.set("--- Select one ---")
        menu_button_map[button] = variable

    l0 = Label(master, text='\nA')
    l0.pack()
    w0 = OptionMenu(master, menu_button_map[A], *SOUND_OPTIONS, command=lambda x: set_sound_map(A,x))
    w0.pack()
    l1 = Label(master, text='\nB')
    l1.pack()
    w1 = OptionMenu(master, menu_button_map[B], *SOUND_OPTIONS, command=lambda x: set_sound_map(B,x))
    w1.pack()
    l2 = Label(master, text='\nX')
    l2.pack()
    w2 = OptionMenu(master, menu_button_map[X], *SOUND_OPTIONS, command=lambda x: set_sound_map(X,x))
    w2.pack()
    l3 = Label(master, text='\nY')
    l3.pack()
    w3 = OptionMenu(master, menu_button_map[Y], *SOUND_OPTIONS, command=lambda x: set_sound_map(Y,x))
    w3.pack()
    l4 = Label(master, text='\nLB')
    l4.pack()
    w4 = OptionMenu(master, menu_button_map[LB], *SOUND_OPTIONS, command=lambda x: set_sound_map(LB,x))
    w4.pack()
    l5 = Label(master, text='\nRB')
    l5.pack()
    w5 = OptionMenu(master, menu_button_map[RB], *SOUND_OPTIONS, command=lambda x: set_sound_map(RB,x))
    w5.pack()
    l6 = Label(master, text='\nLS_BTN')
    l6.pack()
    w6 = OptionMenu(master, menu_button_map[LS_BTN], *SOUND_OPTIONS, command=lambda x: set_sound_map(LS_BTN,x))
    w6.pack()
    l7 = Label(master, text='\nRS_BTN')
    l7.pack()
    w7 = OptionMenu(master, menu_button_map[RS_BTN], *SOUND_OPTIONS, command=lambda x: set_sound_map(RS_BTN,x))
    w7.pack()
    l8 = Label(master, text='\nSELECT')
    l8.pack()
    w8 = OptionMenu(master, menu_button_map[SELECT], *SOUND_OPTIONS, command=lambda x: set_sound_map(SELECT,x))
    w8.pack()
    l9 = Label(master, text='\nSTART')
    l9.pack()
    w9 = OptionMenu(master, menu_button_map[START], *SOUND_OPTIONS, command=lambda x: set_sound_map(START,x))
    w9.pack()
    l10 = Label(master, text='\nDPAD_UP')
    l10.pack()
    w10 = OptionMenu(master, menu_button_map[DPAD_UP], *SOUND_OPTIONS, command=lambda x: set_sound_map(DPAD_UP,x))
    w10.pack()
    l11 = Label(master, text='\nDPAD_DOWN')
    l11.pack()
    w11 = OptionMenu(master, menu_button_map[DPAD_DOWN], *SOUND_OPTIONS, command=lambda x: set_sound_map(DPAD_DOWN,x))
    w11.pack()
    l12 = Label(master, text='\nDPAD_LEFT')
    l12.pack()
    w12 = OptionMenu(master, menu_button_map[DPAD_LEFT], *SOUND_OPTIONS, command=lambda x: set_sound_map(DPAD_LEFT,x))
    w12.pack()
    l13 = Label(master, text='\nDPAD_RIGHT')
    l13.pack()
    w13 = OptionMenu(master, menu_button_map[DPAD_RIGHT], *SOUND_OPTIONS, command=lambda x: set_sound_map(DPAD_RIGHT,x))
    w13.pack()


    try:
        mainloop()
        #while True:
        #    print(joy.read())
    except KeyboardInterrupt:
        pygame.mixer.quit()
        exit(0)

if __name__ == '__main__':
    main()
