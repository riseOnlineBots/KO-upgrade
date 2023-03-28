from threading import Thread, Lock
from time import time

import cv2 as cv


class BotState:
    INITIALIZING = 0
    SEARCHING_UPGRADE_SCROLL = 1
    SEARCHING_UPGRADABLE_ITEMS = 2
    MOVING = 2
    UPGRADING = 3
    UPGRADED = 4


class RiseOnlineBot:
    # Constants.
    INITIALIZING_SECONDS = 2
    UPGRADING_SECONDS = 5
    ITEM_MATCH_THRESHOLD = 0.7

    # Threading properties.
    stopped = True
    lock = None

    # Properties.
    state = None
    targets = []
    screenshot = None
    timestamp = None
    window_offset = (0, 0)
    window_w = 0
    window_h = 0
    upgrading_item = None
    sort_button = None

    upgrade_scroll_position = (0, 0)

    def __init__(self, window_offset, window_size):
        # create a thread lock object
        self.lock = Lock()

        # for translating window positions into screen positions, it's easier to just
        # get the offsets and window size from WindowCapture rather than passing in
        # the whole object
        self.window_offset = window_offset
        self.window_w = window_size[0]
        self.window_h = window_size[1]

        # pre-load the needle image used to confirm our object detection
        self.upgrading_item = cv.imread('item.jpg', cv.IMREAD_UNCHANGED)
        self.sort_button = cv.imread('sortButton.jpg', cv.IMREAD_UNCHANGED)

        # start bot in the initializing mode to allow us time to get setup.
        # mark the time at which this started, so we know when to complete it
        self.state = BotState.INITIALIZING
        self.timestamp = time()

    def update_targets(self, targets):
        self.lock.acquire()
        self.targets = targets
        self.lock.release()

    def update_screenshot(self, screenshot):
        self.lock.acquire()
        self.screenshot = screenshot
        self.lock.release()

    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.stopped = True

    def run(self):
        while not self.stopped:
            if self.state == BotState.INITIALIZING:
                # We don't take actions until the startup waiting period is complete.
                if time() > self.timestamp + self.INITIALIZING_SECONDS:
                    # Starts searching when the waiting period is over.
                    self.lock.acquire()
                    self.state = BotState.SEARCHING_UPGRADE_SCROLL
                    self.lock.release()
            elif self.state == BotState.SEARCHING_UPGRADE_SCROLL:
                print('SEARCHING_UPGRADE_SCROLL in bot')
                # success = self.

