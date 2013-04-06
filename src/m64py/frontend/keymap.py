# -*- coding: utf-8 -*-
# Author: Milan Nikolic <gen2brain@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from PyQt4.QtCore import Qt

from SDL.constants import *

SDL_KEYMAP = {
        Qt.Key_0: SDLK_0,
        Qt.Key_1: SDLK_1,
        Qt.Key_2: SDLK_2,
        Qt.Key_3: SDLK_3,
        Qt.Key_4: SDLK_4,
        Qt.Key_5: SDLK_5,
        Qt.Key_6: SDLK_6,
        Qt.Key_7: SDLK_7,
        Qt.Key_8: SDLK_8,
        Qt.Key_9: SDLK_9,
        Qt.Key_Ampersand: SDLK_AMPERSAND,
        Qt.Key_Asterisk: SDLK_ASTERISK,
        Qt.Key_At: SDLK_AT,
        Qt.Key_QuoteLeft: SDLK_BACKQUOTE,
        Qt.Key_Backslash: SDLK_BACKSLASH,
        Qt.Key_Backspace: SDLK_BACKSPACE,
        Qt.Key_CapsLock: SDLK_CAPSLOCK,
        Qt.Key_AsciiCircum: SDLK_CARET,
        Qt.Key_Clear: SDLK_CLEAR,
        Qt.Key_Colon: SDLK_COLON,
        Qt.Key_Comma: SDLK_COMMA,
        Qt.Key_Delete: SDLK_DELETE,
        Qt.Key_Dollar: SDLK_DOLLAR,
        Qt.Key_Down: SDLK_DOWN,
        Qt.Key_End: SDLK_END,
        Qt.Key_Equal: SDLK_EQUALS,
        Qt.Key_Escape: SDLK_ESCAPE,
        Qt.Key_Exclam: SDLK_EXCLAIM,
        Qt.Key_F1: SDLK_F1,
        Qt.Key_F10: SDLK_F10,
        Qt.Key_F11: SDLK_F11,
        Qt.Key_F12: SDLK_F12,
        Qt.Key_F13: SDLK_F13,
        Qt.Key_F14: SDLK_F14,
        Qt.Key_F15: SDLK_F15,
        Qt.Key_F2: SDLK_F2,
        Qt.Key_F3: SDLK_F3,
        Qt.Key_F4: SDLK_F4,
        Qt.Key_F5: SDLK_F5,
        Qt.Key_F6: SDLK_F6,
        Qt.Key_F7: SDLK_F7,
        Qt.Key_F8: SDLK_F8,
        Qt.Key_F9: SDLK_F9,
        Qt.Key_Greater: SDLK_GREATER,
        Qt.Key_NumberSign: SDLK_HASH,
        Qt.Key_Help: SDLK_HELP,
        Qt.Key_Home: SDLK_HOME,
        Qt.Key_Insert: SDLK_INSERT,
        Qt.Key_Left: SDLK_LEFT,
        Qt.Key_BracketLeft: SDLK_LEFTBRACKET,
        Qt.Key_ParenLeft: SDLK_LEFTPAREN,
        Qt.Key_Less: SDLK_LESS,
        Qt.Key_Menu: SDLK_MENU,
        Qt.Key_Minus: SDLK_MINUS,
        Qt.Key_Mode_switch: SDLK_MODE,
        Qt.Key_NumLock: SDLK_NUMLOCK,
        Qt.Key_PageDown: SDLK_PAGEDOWN,
        Qt.Key_PageUp: SDLK_PAGEUP,
        Qt.Key_Pause: SDLK_PAUSE,
        Qt.Key_Period: SDLK_PERIOD,
        Qt.Key_Plus: SDLK_PLUS,
        Qt.Key_PowerOff: SDLK_POWER,
        Qt.Key_Print: SDLK_PRINT,
        Qt.Key_Question: SDLK_QUESTION,
        Qt.Key_Apostrophe: SDLK_QUOTE,
        Qt.Key_QuoteDbl: SDLK_QUOTEDBL,
        Qt.Key_Return: SDLK_RETURN,
        Qt.Key_Enter: SDLK_RETURN,
        Qt.Key_Right: SDLK_RIGHT,
        Qt.Key_BracketRight: SDLK_RIGHTBRACKET,
        Qt.Key_ParenRight: SDLK_RIGHTPAREN,
        Qt.Key_ScrollLock: SDLK_SCROLLOCK,
        Qt.Key_Semicolon: SDLK_SEMICOLON,
        Qt.Key_Slash: SDLK_SLASH,
        Qt.Key_Space: SDLK_SPACE,
        Qt.Key_SysReq: SDLK_SYSREQ,
        Qt.Key_Tab: SDLK_TAB,
        Qt.Key_Underscore: SDLK_UNDERSCORE,
        Qt.Key_unknown: SDLK_UNKNOWN,
        Qt.Key_Up: SDLK_UP,
        Qt.Key_A: SDLK_a,
        Qt.Key_B: SDLK_b,
        Qt.Key_C: SDLK_c,
        Qt.Key_D: SDLK_d,
        Qt.Key_E: SDLK_e,
        Qt.Key_F: SDLK_f,
        Qt.Key_G: SDLK_g,
        Qt.Key_H: SDLK_h,
        Qt.Key_I: SDLK_i,
        Qt.Key_J: SDLK_j,
        Qt.Key_K: SDLK_k,
        Qt.Key_L: SDLK_l,
        Qt.Key_M: SDLK_m,
        Qt.Key_N: SDLK_n,
        Qt.Key_O: SDLK_o,
        Qt.Key_P: SDLK_p,
        Qt.Key_Q: SDLK_q,
        Qt.Key_R: SDLK_r,
        Qt.Key_S: SDLK_s,
        Qt.Key_T: SDLK_t,
        Qt.Key_U: SDLK_u,
        Qt.Key_V: SDLK_v,
        Qt.Key_W: SDLK_w,
        Qt.Key_X: SDLK_x,
        Qt.Key_Y: SDLK_y,
        Qt.Key_Z: SDLK_z,
        Qt.Key_Alt: SDLK_LALT,
        Qt.Key_Control: SDLK_LCTRL,
        Qt.Key_Meta: SDLK_LMETA,
        Qt.Key_Shift: SDLK_LSHIFT,
        Qt.Key_Super_L: SDLK_LSUPER,
        Qt.Key_Super_R: SDLK_RSUPER
        }

QT_MODIFIERS = {
        Qt.Key_Alt: Qt.AltModifier,
        Qt.Key_Control: Qt.ControlModifier,
        Qt.Key_Meta: Qt.MetaModifier,
        Qt.Key_Shift: Qt.ShiftModifier
        }

QT_KEYSTRING = {
        "Alt": Qt.Key_Alt,
        "Ctrl": Qt.Key_Control,
        "Meta": Qt.Key_Meta,
        "Shift": Qt.Key_Shift
        }
