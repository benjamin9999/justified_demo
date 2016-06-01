from __future__ import absolute_import

from .constants import *


def grow_text_width():
    return {'type': GROW_TEXT_WIDTH}


def shrink_text_width():
    return {'type': SHRINK_TEXT_WIDTH}


def update_text(new_text, who):
    return {'type': UPDATE_TEXT, 'text': new_text, 'who': who}


def toggle_frame():
    return {'type': TOGGLE_FRAME}


def toggle_edit():
    return {'type': TOGGLE_EDIT}


def toggle_method():
    return {'type': TOGGLE_METHOD}


def quit_app():
    return {'type': QUIT_APP}
