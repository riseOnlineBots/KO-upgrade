from threading import Thread, Lock


class Detection:
    stopped = True
    lock = None

    screenshot = None

    upgradable_item_positions = []
    upgrade_scroll_position = None

    def __init__(self):
        # create a thread lock object
        self.lock = Lock()
        # self.cascade = cv.CascadeClassifier(model_file_path)

    def set_upgrade_scroll_position(self, upgrade_scroll_position):
        print('Setting the position of the upgrade scroll. - ', upgrade_scroll_position)
        self.upgrade_scroll_position = upgrade_scroll_position

    def set_upgradable_item_positions(self, upgradable_item_positions):
        print('Setting the positions of the upgradable items. - ', upgradable_item_positions)
        self.upgradable_item_positions = upgradable_item_positions

    def update(self, screenshot):
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
        # TODO: you can write your own time/iterations calculation to determine how fast this is
        while not self.stopped:
            if not self.screenshot is None:
                # do object detection
                # rectangles = self.cascade.detectMultiScale(self.screenshot)
                # lock the thread while updating the results
                self.lock.acquire()
                self.lock.release()
