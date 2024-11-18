import os
import sys

import numpy as np
from PyQt5.QtCore import QPoint, QTimer
from PyQt5.QtGui import QColor, QPainter, QPen
from PyQt5.QtWidgets import (
    QWidget,
)

sys.path.append(os.getcwd())
from algoritm.common import FIGHT, HISS, WALK, EAT, HIT, SLEEP
from algoritm.states_update import update_states
from generator.generator import CatGenerator


def state2color(state: int) -> str:
    if state == WALK:
        return "green"
    if state == HISS:
        return "orange"
    if state == EAT:
        return "purple"
    if state == HIT:
        return "black"
    if state == SLEEP:
        return "blue"
    else:
        return "red"


def update_extra_states(sleepy_ids, hit_ids, eating_ids, states):
    for i in sleepy_ids:
        states[i] = SLEEP
    for j in hit_ids:
        states[j] = HIT
    for k in eating_ids:
        states[int(k)] = EAT


class CatsDrawer(QWidget):
    def __init__(self, n, generator: CatGenerator, r0: int, r1: int):
        super().__init__()

        self.is_paused = False

        self.cats_num = n
        self.states = np.full(self.cats_num, WALK, dtype=np.uint8)

        self.generator = generator
        self.coordinates = self.generator.cats
        self.prev_coordinates = self.generator.cats

        update_states(self.coordinates, r0, r1, self.states)

        self.sleepy_cat_ids = self.generator.sleepy_cat_ids
        self.hit_cat_ids = self.generator.hit_cat_ids
        self.eating_cat_ids = self.generator.eating_cat_ids

        update_extra_states(
            self.sleepy_cat_ids, self.hit_cat_ids, self.eating_cat_ids, self.states
        )
        self.food_num = len(self.generator.food[0])

        # Set up a timer to update positions
        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda: self.update_positions(r0, r1))
        self.timer.start(16)

    def paintEvent(self, event):
        # Create a QPainter object to perform the drawing
        painter = QPainter(self)
        pen = QPen()
        pen.setWidth(10)

        # * Smoother animation
        min_factor = 1
        if self.cats_num <= 500:
            max_factor = 101
        if self.cats_num <= 5000:
            max_factor = 51
        else:
            min_factor = 0
            max_factor = 1
        for factor in range(min_factor, max_factor):
            for i in range(self.cats_num):
                pen.setColor(QColor(state2color(self.states[i])))
                painter.setPen(pen)
                x = int(
                    self.prev_coordinates[0][i]
                    + (self.coordinates[0][i] - self.prev_coordinates[0][i])
                    * factor
                    * 0.1
                )
                y = int(
                    self.prev_coordinates[1][i]
                    + (self.coordinates[1][i] - self.prev_coordinates[1][i])
                    * factor
                    * 0.1
                )

                painter.drawPoint(QPoint(x, y))

        for j in range(self.food_num):
            pen.setColor(QColor("magenta"))
            painter.setPen(pen)
            painter.drawPoint(
                QPoint(int(self.generator.food[0][j]), int(self.generator.food[1][j]))
            )

    def update_positions(self, r0, r1):
        if not self.is_paused:
            self.prev_coordinates = self.coordinates
            self.generator.update_cats()

            self.coordinates = self.generator.cats

            self.sleepy_cat_ids = self.generator.sleepy_cat_ids
            self.hit_cat_ids = self.generator.hit_cat_ids
            self.eating_cat_ids = self.generator.eating_cat_ids

            update_states(self.coordinates, r0, r1, self.states)
            update_extra_states(
                self.sleepy_cat_ids, self.hit_cat_ids, self.eating_cat_ids, self.states
            )

            self.update()  # Trigger another iteration of painting
