import os
from threading import Thread
from time import sleep

import cv2 as cv
import win32api
import win32con
from pynput.mouse import Controller as MouseController

import colorfulText
from vision import Vision
from windowcapture import WindowCapture

# Change the working directory to the folder this script is in.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

mouse = MouseController()


class StateEnum:
    INITIALIZING = 0
    READY = 1
    UPGRADING = 2
    UPGRADED = 3
    STOPPED = 4
    INVENTORY_COMPLETED = 5  # Lets us re-initialize when whole inventory is completed.


class DebugEnum:
    UPGRADE_SCROLL = 0
    UPGRADABLE_ITEMS = 1
    MONEY = 2
    CONFIRM_BUTTON = 3
    NO_ANIMATION = 4


wincap = WindowCapture('Knight OnLine Client')
vision = Vision('upgradeScroll.jpg', 'items', 'confirmButton1.jpg', 'confirmButton2.jpg')

upgrade_scroll_position = []
confirm_button_one_position = []
confirm_button_two_position = []
item_positions = []
upgraded_items = []
stage = 1
max_stage = 7
game_upgrade_limit = 27

for i in list(range(3))[::-1]:
    print('Starting in ', i + 1)
    sleep(1)

print('Get ready! All upgradable slots will be upgraded to +{}.'.format(max_stage))

state = StateEnum.INITIALIZING

# DEBUG = DebugEnum.UPGRADABLE_ITEMS
DEBUG = None


def detect_upgrade_scroll():
    global upgrade_scroll_position, DEBUG

    if len(upgrade_scroll_position):
        return upgrade_scroll_position

    rectangles = vision.findUpgradeScroll(screenshot, 0.7)
    positions = vision.get_click_points(rectangles)

    if not positions:
        print('There is no upgrade scroll in your inventory.')
        stop()

    target = wincap.get_screen_position(positions[0])

    if DEBUG == DebugEnum.UPGRADE_SCROLL:
        image = vision.draw_crosshairs(screenshot, positions)
        cv.imshow('Display', image)

    upgrade_scroll_position = target

    return rectangles


def detect_confirm_button_one():
    global confirm_button_one_position, DEBUG

    if len(confirm_button_one_position):
        return confirm_button_one_position

    rectangles = vision.findConfirmButtonOne(screenshot, 0.6)
    positions = vision.get_click_points(rectangles)

    if not positions:
        print("Did you open the upgrade window? I couldn't detect the confirm button.")
        stop()

    target = wincap.get_screen_position(positions[0])

    if DEBUG == DebugEnum.CONFIRM_BUTTON:
        image = vision.draw_crosshairs(screenshot, positions)
        cv.imshow('Display', image)

    confirm_button_one_position = target

    return rectangles


def detect_confirm_button_two():
    global confirm_button_two_position, DEBUG

    if confirm_button_two_position:
        return confirm_button_two_position

    ss = wincap.get_screenshot()
    rectangles = vision.findConfirmButtonTwo(ss, 0.7)
    positions = vision.get_click_points(rectangles)

    if not positions:
        print("Unable to find the 2nd confirm button.")
        stop()

    confirm_button_two_position = wincap.get_screen_position(positions[0])

    return rectangles


def click_upgrade_scroll():
    global upgrade_scroll_position

    x = upgrade_scroll_position[0]
    y = upgrade_scroll_position[1]

    press_right((x, y + 15))


def upgrade_the_item():
    global confirm_button_one_position, confirm_button_two_position

    x = confirm_button_one_position[0]
    y = confirm_button_one_position[1]

    press_left((x, y + 15))
    sleep(0.1)

    if not confirm_button_two_position:
        detect_confirm_button_two()

    click_confirm_button_two()

    print('Upgrade in progress.')


def click_confirm_button_two():
    global confirm_button_two_position

    x = confirm_button_two_position[0]
    y = confirm_button_two_position[1]

    press_left((x, y + 15))


def initialize_upgradable_items():
    global item_positions, DEBUG

    if len(item_positions):
        return item_positions

    rectangles = vision.find(screenshot, 0.6)
    item_positions = vision.get_click_points(rectangles)

    if not item_positions:
        print("I couldn't find any upgradable item. Shutting down the bot.")
        stop()

    if DEBUG == DebugEnum.UPGRADABLE_ITEMS:
        image = vision.draw_crosshairs(screenshot, item_positions)
        cv.imshow('Display', image)


def detect_and_click_first_upgradable_item():
    global item_positions, upgraded_items

    for item in item_positions:
        if item not in upgraded_items:
            x, y = item
            press_right((x, y + 15))
            upgraded_items.append(item)
            break


def press_right(pos):
    win32api.SetCursorPos(pos)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
    sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)


def press_left(pos):
    win32api.SetCursorPos(pos)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def stop():
    global state
    colorfulText.text("...BOT HAS BEEN TERMINATED...")
    cv.destroyAllWindows()
    state = StateEnum.STOPPED


def run():
    global upgraded_items, item_positions, stage, max_stage, game_upgrade_limit, state

    if state != StateEnum.STOPPED:
        print('Total: {} Current: {} - availability: {}'.format(len(item_positions) + 1, len(upgraded_items) + 1,
                                                                game_upgrade_limit))

        if len(item_positions) == len(upgraded_items):
            if stage == max_stage:
                print('All slots have been upgraded to the desired level: {} '.format(stage + 1))
                stop()
            else:
                stage += 1

                print('All items are upgraded. Preparing the next stage.')

                upgraded_items = []
                item_positions = []
                sleep(1)
                initialize_upgradable_items()
                run()
        else:
            detect_and_click_first_upgradable_item()
            sleep(0.2)
            click_upgrade_scroll()
            sleep(0.2)
            upgrade_the_item()

            game_upgrade_limit -= 1

            if game_upgrade_limit == 0:
                for _ in range(3):
                    colorfulText.text('Upgrade limit exceeded. Restart the game.')

                # ALT + F4.
                sleep(2)
                win32api.keybd_event(0xA4, win32api.MapVirtualKey(0xA4, 0), 0, 0)
                win32api.keybd_event(0x73, win32api.MapVirtualKey(0x73, 0), 0, 0)
                win32api.keybd_event(0x73, win32api.MapVirtualKey(0x73, 0), win32con.KEYEVENTF_KEYUP, 0)
                win32api.keybd_event(0xA4, win32api.MapVirtualKey(0xA4, 0), win32con.KEYEVENTF_KEYUP, 0)

                stop()
            else:
                # TODO: Add right click to anvil to skip the animation.
                sleep(4.5)


while True:
    screenshot = wincap.get_screenshot()

    # rectangles = vision.find(screenshot, 0.7)
    # positions = vision.get_click_points(rectangles)
    # image = vision.draw_crosshairs(screenshot, positions)
    # image = vision.draw_rectangles(screenshot, rectangles)
    # cv.imshow('Display', image)

    if state != StateEnum.STOPPED:
        detect_upgrade_scroll()
        detect_confirm_button_one()
        initialize_upgradable_items()
        thread = Thread(target=run())

    key = cv.waitKey(1) & 0xFF

    if key == ord("q"):
        stop()
        break

# pyinstaller.exe -F .\main.py --paths C:\Users\undefined\AppData\Local\Programs\Python\Python39-32\Lib\site-packages
