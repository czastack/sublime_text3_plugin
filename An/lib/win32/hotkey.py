from ctypes import windll, byref, Structure, wintypes
from utils.thread import newthread
from .keys import getVK
from .sendkey import sendVKey, sendComb
import sys
import time

WM_HOTKEY    = 0x0312
WM_KEYUP     = 0x0101

# class MSG(Structure):
#     _fields_ = [
#         ('hWnd', wintypes.HWND),
#         ('message', wintypes.UINT),
#         ('wParam', wintypes.WPARAM),
#         ('lParam', wintypes.LPARAM),
#         ('time', wintypes.DWORD),
#         ('pt', wintypes.POINT)
#     ]


class HotKeyHelper:
    __slots__ = ('callbackMap', 'stopKey')

    def __init__(self):
        self.callbackMap = {
            '__looping': False,
            '__stop': False,
        }

    @newthread
    def RegisterHotKey(self, args):
        """
        :param callback: fn(hotkeyId)
        """

        callbackMap = self.callbackMap

        if (callbackMap['__looping']):
            return

        for hotkeyId, mod, key, callback in args:
            if isinstance(hotkeyId, str):
                hotkeyId = windll.Kernel32.GlobalAddAtomA(hotkeyId)

            if hotkeyId in callbackMap:
                raise ValueError('%d already in use' % hotkeyId)

            keyCode = getVK(key) if isinstance(key, str) else key
            if keyCode is 0:
                raise ValueError('invalid key ' + str(key))

            if windll.user32.RegisterHotKey(None, hotkeyId, mod, keyCode):
                callbackMap[hotkeyId] = callback
            else:
                raise ValueError('%d register failed' % hotkeyId)

        self.stopKey = (mod, keyCode)

        try:
            msg = wintypes.MSG()
            while True:
                if (windll.user32.GetMessageA(byref(msg), None, 0, 0) != 0):
                    if callbackMap['__stop']:
                        callbackMap['__stop'] = False
                        callbackMap['__looping'] = False
                        # print('stop')
                        break

                    if msg.message == WM_HOTKEY:
                        hotkeyId = msg.wParam
                        if hotkeyId in callbackMap:
                            callbackMap[hotkeyId](hotkeyId)
                        # if (time.time() - lastTime) < delta:
                        #     print("double")
                        # lastTime = time.time()
                    # if msg.message == WM_KEYUP:
                    #     print("up")
                    windll.user32.TranslateMessage(byref(msg))
                    windll.user32.DispatchMessageA(byref(msg))
        finally:
            for hotkeyId, mod, key, callback in args:
                self.UnRegisterHotKey(hotkeyId)

    def UnRegisterHotKey(self, hotkeyId):
        if isinstance(hotkeyId, str):
            hotkeyId = windll.Kernel32.GlobalAddAtomA(hotkeyId)

        if (self.callbackMap.pop(hotkeyId, None) is not None):
            return windll.user32.UnregisterHotKey(None, hotkeyId)
        else:
            return False


    def setCallback(self, hotkeyId, callback):
        self.callbackMap[hotkeyId] = callback 


    def stopLoop(self):
        self.callbackMap['__stop'] = True

    def stop(self):
        self.stopLoop()
        sendComb(*self.stopKey)
