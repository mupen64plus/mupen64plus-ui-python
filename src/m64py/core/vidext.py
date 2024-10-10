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

import ctypes

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QSurfaceFormat

from sdl2 import SDL_WasInit, SDL_InitSubSystem, SDL_QuitSubSystem, SDL_INIT_VIDEO
from sdl2 import SDL_GetNumDisplayModes, SDL_DisplayMode, SDL_GetDisplayMode

from m64py.core.defs import *
from m64py.frontend.log import log

try:
    if not SDL_WasInit(SDL_INIT_VIDEO):
        SDL_InitSubSystem(SDL_INIT_VIDEO)
    MODES = []
    RATES = []
    display = SDL_DisplayMode()
    for m in range(SDL_GetNumDisplayModes(0)):
        ret = SDL_GetDisplayMode(0, m, ctypes.byref(display))
        if (display.w, display.h) not in MODES:
            MODES.append((display.w, display.h))
            RATES.append(display.refresh_rate)
    if SDL_WasInit(SDL_INIT_VIDEO):
        SDL_QuitSubSystem(SDL_INIT_VIDEO)
except Exception as err:
    log.warn(str(err))


class Video:
    """Mupen64Plus video extension"""

    def __init__(self):
        """Constructor."""
        self.parent = None
        self.widget = None
        self.glformat = None
        self.glcontext = None

    def set_widget(self, parent, widget):
        """Sets GL widget."""
        self.parent = parent
        self.widget = widget

    def init(self):
        """Initialize GL context."""
        if not self.glcontext:
            self.glformat = QSurfaceFormat.defaultFormat()
            self.glformat.setVersion(3, 3)
            self.glformat.setOption(QSurfaceFormat.FormatOption.DeprecatedFunctions, 1)
            self.glformat.setProfile(QSurfaceFormat.OpenGLContextProfile.CompatibilityProfile)
            self.glformat.setRenderableType(QSurfaceFormat.RenderableType.OpenGL)
            self.glformat.setDepthBufferSize(24)
            self.glformat.setSwapInterval(0)

            self.glcontext = self.widget.context()
            self.glcontext.setFormat(self.glformat)
        return M64ERR_SUCCESS

    def quit(self):
        """Shuts down the video system."""
        if self.glcontext:
            self.glcontext.doneCurrent()
            self.glcontext.moveToThread(QApplication.instance().thread())
            self.glcontext = None
        return M64ERR_SUCCESS

    def list_modes(self, size_array, num_sizes):
        """Enumerates the available resolutions
        for fullscreen video modes."""
        num_sizes.contents.value = len(MODES)
        for num, mode in enumerate(MODES):
            width, height = mode
            size_array[num].uiWidth = width
            size_array[num].uiHeight = height
        return M64ERR_SUCCESS

    def list_rates(self, size_array, num_rates, rates):
        """Enumerates the available rates
        for fullscreen video modes."""
        num_rates.contents.value = len(RATES)
        for num, rate in enumerate(RATES):
            rates[num] = rate
        return M64ERR_SUCCESS

    def set_mode(self, width, height, bits, mode, flags):
        """Creates a rendering window."""
        self.parent.vidext_init.emit(self.glcontext)
        while not self.parent._initialized:
            continue

        self.glcontext.makeCurrent(self.widget)

        if self.glcontext.isValid():
            # GL = self.glcontext.functions()
            # GL.glClearColor(0.0, 0.0, 0.0, 1.0)
            # GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
            # self.glcontext.swapBuffers(self.glcontext.surface())
            # GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
            return M64ERR_SUCCESS
        else:
            return M64ERR_SYSTEM_FAIL

    def set_mode_with_rate(self, width, height, rate, bits, mode, flags):
        """Creates a rendering window."""
        return self.set_mode(width, height, bits, mode, flags)

    def set_caption(self, title):
        """Sets the caption text of the
        emulator rendering window. """
        title = "M64Py :: %s" % title.decode()
        self.parent.set_caption.emit(title)
        return M64ERR_SUCCESS

    def toggle_fs(self):
        """Toggles between fullscreen and
        windowed rendering modes. """
        self.parent.toggle_fs.emit()
        return M64ERR_SUCCESS

    def gl_get_proc(self, proc):
        """Used to get a pointer to
        an OpenGL extension function."""
        addr = self.glcontext.getProcAddress(proc)
        if addr is not None:
            return addr.__int__()
        else:
            log.warn("VidExtFuncGLGetProc: '%s'" % proc.decode())

    def gl_set_attr(self, attr, value):
        """Sets OpenGL attributes."""
        attr_map = {
            M64P_GL_DOUBLEBUFFER: self.set_doublebuffer,
            M64P_GL_BUFFER_SIZE: self.set_buffer_size,
            M64P_GL_DEPTH_SIZE: self.glformat.setDepthBufferSize,
            M64P_GL_RED_SIZE: self.glformat.setRedBufferSize,
            M64P_GL_GREEN_SIZE: self.glformat.setGreenBufferSize,
            M64P_GL_BLUE_SIZE: self.glformat.setBlueBufferSize,
            M64P_GL_ALPHA_SIZE: self.glformat.setAlphaBufferSize,
            M64P_GL_SWAP_CONTROL: self.glformat.setSwapInterval,
            M64P_GL_MULTISAMPLEBUFFERS: None,
            M64P_GL_MULTISAMPLESAMPLES: self.glformat.setSamples,
            M64P_GL_CONTEXT_MAJOR_VERSION: self.glformat.setMajorVersion,
            M64P_GL_CONTEXT_MINOR_VERSION: self.glformat.setMinorVersion,
            M64P_GL_CONTEXT_PROFILE_MASK: self.set_profile
        }

        set_attr = attr_map[attr]
        if set_attr:
            set_attr(value)

        return M64ERR_SUCCESS

    def gl_get_attr(self, attr, value):
        """Gets OpenGL attributes."""
        attr_map = {
            M64P_GL_DOUBLEBUFFER: self.get_doublebuffer,
            M64P_GL_BUFFER_SIZE: self.get_buffer_size,
            M64P_GL_DEPTH_SIZE: self.glformat.depthBufferSize,
            M64P_GL_RED_SIZE: self.glformat.redBufferSize,
            M64P_GL_GREEN_SIZE: self.glformat.greenBufferSize,
            M64P_GL_BLUE_SIZE: self.glformat.blueBufferSize,
            M64P_GL_ALPHA_SIZE: self.glformat.alphaBufferSize,
            M64P_GL_SWAP_CONTROL: self.glformat.swapInterval,
            M64P_GL_MULTISAMPLEBUFFERS: None,
            M64P_GL_MULTISAMPLESAMPLES: self.glformat.samples,
            M64P_GL_CONTEXT_MAJOR_VERSION: self.glformat.majorVersion,
            M64P_GL_CONTEXT_MINOR_VERSION: self.glformat.minorVersion,
            M64P_GL_CONTEXT_PROFILE_MASK: self.get_profile
        }

        get_attr = attr_map[attr]
        if get_attr:
            new_value = int(get_attr())
            value.contents.value = new_value
            if new_value != value.contents.value:
                return M64ERR_SYSTEM_FAIL

        return M64ERR_SUCCESS

    def gl_swap_buf(self):
        """Swaps the front/back buffers after
        rendering an output video frame. """
        if self.glcontext.isValid():
            self.glcontext.swapBuffers(self.glcontext.surface())
        return M64ERR_SUCCESS

    def resize_window(self, width, height):
        """Called when the video plugin has resized its OpenGL
        output viewport in response to a ResizeVideoOutput() call"""
        return M64ERR_SUCCESS

    def gl_get_default_framebuffer(self):
        """Gets default framebuffer."""
        return self.glcontext.defaultFramebufferObject()

    def init_with_render_mode(self, mode):
        return self.init()

    def vk_get_surface(self, a, b):
        return M64ERR_SUCCESS

    def vk_get_instance_extensions(self, a, b):
        return M64ERR_SUCCESS

    def set_profile(self, value):
        if value == M64P_GL_CONTEXT_PROFILE_CORE:
            self.glformat.setProfile(QSurfaceFormat.OpenGLContextProfile.CoreProfile)
        elif value == M64P_GL_CONTEXT_PROFILE_COMPATIBILITY:
            self.glformat.setProfile(QSurfaceFormat.OpenGLContextProfile.CompatibilityProfile)
        else:
            self.glformat.setProfile(QSurfaceFormat.OpenGLContextProfile.CompatibilityProfile)

    def get_profile(self):
        profile = self.glformat.profile()
        if profile == QSurfaceFormat.OpenGLContextProfile.CoreProfile:
            return M64P_GL_CONTEXT_PROFILE_CORE
        elif profile == QSurfaceFormat.OpenGLContextProfile.CompatibilityProfile:
            return M64P_GL_CONTEXT_PROFILE_COMPATIBILITY
        else:
            return M64P_GL_CONTEXT_PROFILE_COMPATIBILITY

    def set_doublebuffer(self, value):
        if value == 1:
            self.glformat.setSwapBehavior(QSurfaceFormat.SwapBehavior.DoubleBuffer)
        elif value == 0:
            self.glformat.setSwapBehavior(QSurfaceFormat.SwapBehavior.SingleBuffer)

    def get_doublebuffer(self):
        if self.glformat.swapBehavior() == QSurfaceFormat.SwapBehavior.DoubleBuffer:
            return 1
        return 0

    def set_buffer_size(self, value):
        val = int(value/4)
        self.glformat.setAlphaBufferSize(val)
        self.glformat.setRedBufferSize(val)
        self.glformat.setGreenBufferSize(val)
        self.glformat.setBlueBufferSize(val)

    def get_buffer_size(self):
        return (self.glformat.alphaBufferSize() + self.glformat.redBufferSize() +
                self.glformat.greenBufferSize() + self.glformat.blueBufferSize())

video = Video()
vidext = M64pVideoExtensionFunctions()
vidext.Functions = 17
vidext.VidExtFuncInit = FuncInit(video.init)
vidext.VidExtFuncQuit = FuncQuit(video.quit)
vidext.VidExtFuncListModes = FuncListModes(video.list_modes)
vidext.VidExtFuncListRates = FuncListRates(video.list_rates)
vidext.VidExtFuncSetMode = FuncSetMode(video.set_mode)
vidext.VidExtFuncSetModeWithRate = FuncSetModeWithRate(video.set_mode_with_rate)
vidext.VidExtFuncGLGetProc = FuncGLGetProc(video.gl_get_proc)
vidext.VidExtFuncGLSetAttr = FuncGLSetAttr(video.gl_set_attr)
vidext.VidExtFuncGLGetAttr = FuncGLGetAttr(video.gl_get_attr)
vidext.VidExtFuncGLSwapBuf = FuncGLSwapBuf(video.gl_swap_buf)
vidext.VidExtFuncSetCaption = FuncSetCaption(video.set_caption)
vidext.VidExtFuncToggleFS = FuncToggleFS(video.toggle_fs)
vidext.VidExtFuncResizeWindow = FuncResizeWindow(video.resize_window)
vidext.VidExtFuncGLGetDefaultFramebuffer  = FuncGLGetDefaultFramebuffer(video.gl_get_default_framebuffer)
vidext.VidExtFuncInitWithRenderMode  = FuncInitWithRenderMode(video.init_with_render_mode)
vidext.VidExtFuncVKGetSurface  = FuncVKGetSurface(video.vk_get_surface)
vidext.VidExtFuncVKGetInstanceExtensions  = FuncVKGetInstanceExtensions(video.vk_get_instance_extensions)
