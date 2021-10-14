import time
import numpy as np
import pyscreenshot as ImageGrab
import cv2
import os
import pytesseract
import pyautogui
import pydirectinput
from pyautogui import Point
from ctypes import windll, Structure, c_long, byref

name_block_pos = []
light_value_pos = []
player_pos = []
see_angle = []


class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]


def queryMousePosition():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return pt.x, pt.y


# килибровка координат
def coordinate_calibration():
    time.sleep(0.5)
    print("Кординаты названий блоков")
    print("1:")
    time.sleep(5)
    name_block_pos.append(queryMousePosition())
    print("2:")
    time.sleep(5)
    name_block_pos.append(queryMousePosition())

    print("Кординаты значений освещения")
    print("1:")
    time.sleep(5)
    light_value_pos.append(queryMousePosition())
    print("2:")
    time.sleep(5)
    light_value_pos.append(queryMousePosition())

    print("Кординаты пизицыи игрока")
    print("1:")
    time.sleep(5)
    player_pos.append(queryMousePosition())
    print("2:")
    time.sleep(5)
    player_pos.append(queryMousePosition())

    print("Кординаты угол зрение")
    print("1:")
    time.sleep(5)
    see_angle.append(queryMousePosition())
    print("2:")
    time.sleep(5)
    see_angle.append(queryMousePosition())


class Bot:
    def __init__(self):
        self.work_values = self._correct_value(mode="start_works")
        self.current_values = {"pos": [], "see_angle": [], "value_light": [], "block_see_name": []}
        self.target = {"pos": [-172, 61, -286], "see_angle": [0.0, 0.0], "value_light": [], "block_see_name": []}
        self.value_for_action = {"go": [0, 0]}
        self.update_values = 0

    def update(self):
        if self.current_values["pos"] != self.target["pos"]:
            if self.value_for_action["go"] != self.current_values["see_angle"]:
                pass


    def _correct_value(self, mode):
        if mode == "start_works":
            # see_angle
            ScrolAngle_h1, ScrolAngle_v1 = self._value_from_screen(mode="see").split()
            pydirectinput.move(100, 100)
            ScrolAngle_h2, ScrolAngle_v2 = self._value_from_screen(mode="see").split()
            ScrolAngle_h_100, ScrolAngle_v_100 = int(ScrolAngle_h1) - int(ScrolAngle_h2), int(ScrolAngle_v1) - int(ScrolAngle_v2)

            # pos_move
            # pass
            return {"ScrolAngle_h_100": ScrolAngle_h_100, "ScrolAngle_v_100": ScrolAngle_v_100}



    @staticmethod
    def _value_from_screen(mode):
        # filename = 'Image.png'
        if mode == "pos":
            screen = np.array(ImageGrab.grab(bbox=(*player_pos[0], *player_pos[1])))
            text = pytesseract.image_to_string(screen, config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789')
            # cv2.imwrite(filename, screen)
            print(text)
            return text
        elif mode == "light":
            screen = np.array(ImageGrab.grab(bbox=(*light_value_pos[0], *light_value_pos[1])))
            text = pytesseract.image_to_string(screen)
            print(text)
            return text
        elif mode == "block_name":
            screen = np.array(ImageGrab.grab(bbox=(*name_block_pos[0], *name_block_pos[1])))
            text = pytesseract.image_to_string(screen)
            print(text)
            return text
        elif mode == "see":
            screen = np.array(ImageGrab.grab(bbox=(*see_angle[0], *see_angle[1])))
            text = pytesseract.image_to_string(screen)
            print(text)
            return text

        # index = text.find("You")
        # print(index)
        #
        # if index == -1:
        #     print("ТАКОГО СЛОВА НЕТЬ!!!")
        # else:
        #     print("Я НАШЕЛЬ ЕНТО СЛОВО!!!")


def main():
    bot_maincraft = Bot()
    while True:
        bot_maincraft.update()


if __name__ == "__main__":
    print("Запуск бота")
    time.sleep(0.5)
    print("Начало колибровки координат")
    coordinate_calibration()
    print(name_block_pos, light_value_pos, player_pos)
    print("---")
    time.sleep(5)
    print("---")
    main()