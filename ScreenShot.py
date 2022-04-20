import os
import re

import cv2
from cnocr import CnOcr

from adb_variable import device_name
from button_pos import *


class ScreenShot:
    ocr = CnOcr()

    def __init__(self, name: str):
        self.file = 'screenshots/' + name + '.png'
        os.system('adb -s %s shell screencap -p /sdcard/01.png' % device_name)
        os.system('adb -s %s pull /sdcard/01.png %s' % (device_name, self.file))
        self.image = cv2.imread(self.file)

    def recruit_status(self, slot) -> str:
        if self.has_slot_button('聘用候选人', slot):
            return 'done'
        if self.has_slot_button('立即招募', slot):
            return 'recruiting'
        if self.has_slot_button('开始招募干员', slot):
            return 'empty'

    def has_slot_button(self, button: str, slot) -> bool:
        corp = get_slot_button_pos(button, slot)
        res = self.to_str(corp)
        if res == button:
            return True
        return False

    def get_tags(self) -> list:
        tags = []
        for i in range(0, 5):
            corp = get_tags_button_pos(i)
            tags.append(self.to_str(corp))
        return tags

    def refresh_status(self) -> bool:
        corp = recruit_button_pos['刷新标签']
        status = self.to_str(corp)
        if status == '点击刷新标签':
            return True
        return False

    def to_str(self, corp=None) -> str:
        if corp is not None:
            img = self.image[corp[1]:corp[3], corp[0]:corp[2]]
        else:
            img = self.image
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # cv2.imwrite('screenshots/test.png', img)
        res = self.ocr.ocr(255 - img)
        if res:
            res = ''.join([x for x in res[0][0]])
            res = re.sub(r'[^\u4e00-\u9fa5]', '', res)
        return res
