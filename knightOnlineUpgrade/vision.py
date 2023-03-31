import glob

import cv2
import numpy as np


class Vision:
    # properties
    upgrade_scroll_img = None
    upgrade_scroll_w = 0
    upgrade_scroll_h = 0
    upgrade_scroll_position = None

    upgradable_item_img_list = []
    upgradable_item_w_list = []
    upgradable_item_h_list = []

    confirm_button_one_img = None
    confirm_button_one_w = 0
    confirm_button_one_h = 0

    confirm_button_two_img = None
    confirm_button_two_w = 0
    confirm_button_two_h = 0

    method = None

    # constructor
    def __init__(self, upgrade_scroll_path, upgradable_item_path_list, confirm_button_one_path, confirm_button_two_path,
                 method=cv2.TM_CCOEFF_NORMED):
        if upgrade_scroll_path:
            # load the image we're trying to match
            # https://docs.opencv2.org/4.2.0/d4/da8/group__imgcodecs.html
            self.upgrade_scroll_img = cv2.imread(upgrade_scroll_path, cv2.IMREAD_UNCHANGED)

            # Save the dimensions of the needle image
            self.upgrade_scroll_w = self.upgrade_scroll_img.shape[1]
            self.upgrade_scroll_h = self.upgrade_scroll_img.shape[0]

        if confirm_button_one_path:
            # load the image we're trying to match
            # https://docs.opencv2.org/4.2.0/d4/da8/group__imgcodecs.html
            self.confirm_button_one_img = cv2.imread(confirm_button_one_path, cv2.IMREAD_UNCHANGED)

            # Save the dimensions of the needle image
            self.confirm_button_one_w = self.confirm_button_one_img.shape[1]
            self.confirm_button_one_h = self.confirm_button_one_img.shape[0]

        if confirm_button_two_path:
            self.confirm_button_two_img = cv2.imread(confirm_button_two_path, cv2.IMREAD_UNCHANGED)
            self.confirm_button_two_w = self.confirm_button_two_img.shape[1]
            self.confirm_button_two_h = self.confirm_button_two_img.shape[0]

        if upgradable_item_path_list:
            path = '{}/*.jpg'.format(upgradable_item_path_list)

            for img in glob.glob(path):
                image = cv2.imread(img, cv2.IMREAD_UNCHANGED)

                # image = cv2.resize(image, (100, 100))
                self.upgradable_item_img_list.append(image)

                # Save the dimensions of the needle image
                self.upgradable_item_w_list.append(image.shape[1])
                self.upgradable_item_h_list.append(image.shape[0])

        # There are 6 methods to choose from:
        # TM_CCOEFF, TM_CCOEFF_NORMED, TM_CCORR, TM_CCORR_NORMED, TM_SQDIFF, TM_SQDIFF_NORMED
        self.method = method

    def findConfirmButtonTwo(self, screenshot, threshold):
        # run the OpenCV algorithm
        result = cv2.matchTemplate(screenshot, self.confirm_button_two_img, self.method)

        # Get the all the positions from the match result that exceed our threshold
        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))

        # if we found no results, return now. this reshapes of the empty array allows us to
        # concatenate together results without causing an error
        if not locations:
            print('No location found for the confirm button 2.')
            return np.array([], dtype=np.int32).reshape(0, 4)

        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), self.confirm_button_two_w, self.confirm_button_two_h]
            # Add every box to the list twice in order to retain single (non-overlapping) boxes
            rectangles.append(rect)
            rectangles.append(rect)
        # Apply group rectangles.
        # The groupThreshold parameter should usually be 1. If you put it at 0 then no grouping is
        # done. If you put it at 2 then an object needs at least 3 overlapping rectangles to appear
        # in the result. I've set eps to 0.5, which is:
        # "Relative difference between sides of the rectangles to merge them into a group."
        rectangles, weights = cv2.groupRectangles(rectangles, groupThreshold=1, eps=0.5)

        return rectangles

    def findConfirmButtonOne(self, screenshot, threshold):
        # run the OpenCV algorithm
        result = cv2.matchTemplate(screenshot, self.confirm_button_one_img, self.method)

        # Get the all the positions from the match result that exceed our threshold
        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))

        # if we found no results, return now. this reshapes of the empty array allows us to
        # concatenate together results without causing an error
        if not locations:
            print('No location found for the confirm button.')
            return np.array([], dtype=np.int32).reshape(0, 4)

        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), self.confirm_button_one_w, self.confirm_button_one_h]
            # Add every box to the list twice in order to retain single (non-overlapping) boxes
            rectangles.append(rect)
            rectangles.append(rect)
        # Apply group rectangles.
        # The groupThreshold parameter should usually be 1. If you put it at 0 then no grouping is
        # done. If you put it at 2 then an object needs at least 3 overlapping rectangles to appear
        # in the result. I've set eps to 0.5, which is:
        # "Relative difference between sides of the rectangles to merge them into a group."
        rectangles, weights = cv2.groupRectangles(rectangles, groupThreshold=1, eps=0.5)

        return rectangles

    def findUpgradeScroll(self, screenshot, threshold):
        # run the OpenCV algorithm
        result = cv2.matchTemplate(screenshot, self.upgrade_scroll_img, self.method)

        # Get the all the positions from the match result that exceed our threshold
        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))

        # if we found no results, return now. this reshape of the empty array allows us to
        # concatenate together results without causing an error
        if not locations:
            print('No location found for the upgrade scroll.')
            return np.array([], dtype=np.int32).reshape(0, 4)

        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), self.upgrade_scroll_w, self.upgrade_scroll_h]
            # Add every box to the list twice in order to retain single (non-overlapping) boxes
            rectangles.append(rect)
            rectangles.append(rect)
        # Apply group rectangles.
        # The groupThreshold parameter should usually be 1. If you put it at 0 then no grouping is
        # done. If you put it at 2 then an object needs at least 3 overlapping rectangles to appear
        # in the result. I've set eps to 0.5, which is:
        # "Relative difference between sides of the rectangles to merge them into a group."
        rectangles, weights = cv2.groupRectangles(rectangles, groupThreshold=1, eps=0.5)

        return rectangles

    def find(self, screenshot, threshold=0.5, max_results=36):
        rectangles = []

        for i in range(len(self.upgradable_item_img_list)):
            # run the OpenCV algorithm
            result = cv2.matchTemplate(screenshot, self.upgradable_item_img_list[i], self.method)

            # Get the all the positions from the match result that exceed our threshold
            locations = np.where(result >= threshold)
            locations = list(zip(*locations[::-1]))

            # if we found no results, return now. this reshape of the empty array allows us to
            # concatenate together results without causing an error
            if not locations:
                # print('Items not found.')
                # return np.array([], dtype=np.int32).reshape(0, 4)
                continue

            # You'll notice a lot of overlapping rectangles get drawn. We can eliminate those redundant
            # locations by using groupRectangles().
            # First we need to create the list of [x, y, w, h] rectangles
            for loc in locations:
                rect = [int(loc[0]), int(loc[1]), self.upgradable_item_w_list[i], self.upgradable_item_h_list[i]]
                # Add every box to the list twice in order to retain single (non-overlapping) boxes
                rectangles.append(rect)
                rectangles.append(rect)
            # Apply group rectangles.
            # The groupThreshold parameter should usually be 1. If you put it at 0 then no grouping is
            # done. If you put it at 2 then an object needs at least 3 overlapping rectangles to appear
            # in the result. I've set eps to 0.5, which is:
            # "Relative difference between sides of the rectangles to merge them into a group."

        rectangles, weights = cv2.groupRectangles(rectangles, groupThreshold=1, eps=0.5)
        # print(rectangles)

        # for performance reasons, return a limited number of results.
        # these aren't necessarily the best results.
        # if len(rectangles) > max_results:
        #     print('Warning: too many results, raise the threshold.')
        #     rectangles = rectangles[:max_results]

        return rectangles

    # given a list of [x, y, w, h] rectangles returned by find(), convert those into a list of
    # [x, y] positions in the center of those rectangles where we can click on those found items
    def get_click_points(self, rectangles):
        points = []

        # Loop over all the rectangles
        for (x, y, w, h) in rectangles:
            # Determine the center position
            center_x = x + int(w / 2)
            center_y = y + int(h / 2)
            # Save the points
            points.append((center_x, center_y))

        return points

    # given a list of [x, y, w, h] rectangles and a canvas image to draw on, return an image with
    # all of those rectangles drawn
    def draw_rectangles(self, haystack_img, rectangles):
        # these colors are actually BGR
        line_color = (0, 255, 0)
        line_type = cv2.LINE_4

        for (x, y, w, h) in rectangles:
            # determine the box positions
            top_left = (x, y)
            bottom_right = (x + w, y + h)
            # draw the box
            cv2.rectangle(haystack_img, top_left, bottom_right, line_color, lineType=line_type)

        return haystack_img

    # given a list of [x, y] positions and a canvas image to draw on, return an image with all
    # of those click points drawn on as crosshairs
    def draw_crosshairs(self, haystack_img, points):
        # these colors are actually BGR
        marker_color = (255, 0, 255)
        marker_type = cv2.MARKER_CROSS

        for (center_x, center_y) in points:
            # draw the center point
            cv2.drawMarker(haystack_img, (center_x, center_y), marker_color, marker_type)

        return haystack_img
