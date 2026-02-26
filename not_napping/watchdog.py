"""Monitor for real user input to auto-cancel when the user returns."""


class InputWatchdog:
    """Listens for real mouse/keyboard input via pynput daemon threads.

    The watchdog is "disarmed" while behaviors execute (so synthetic input
    from pyautogui doesn't trigger a false stop) and "armed" during the
    delay periods between behaviors.
    """

    MOUSE_THRESHOLD = 5  # Manhattan-distance pixels to ignore jitter

    def __init__(self, callback):
        """
        callback: called once (no args) when real input is detected while armed.
        """
        from pynput import mouse, keyboard

        self._callback = callback
        self._armed = False
        self._mouse_origin = (0, 0)
        self._fired = False  # prevent duplicate triggers

        self._mouse_listener = mouse.Listener(
            on_move=self._on_move,
            on_click=self._on_click,
            on_scroll=self._on_scroll,
        )
        self._keyboard_listener = keyboard.Listener(
            on_press=self._on_press,
        )

        self._mouse_listener.daemon = True
        self._keyboard_listener.daemon = True

    def start(self):
        """Start both listeners."""
        self._mouse_listener.start()
        self._keyboard_listener.start()

    def arm(self, mouse_pos):
        """Enable detection. mouse_pos is the current (x, y) from pyautogui."""
        self._mouse_origin = mouse_pos
        self._fired = False
        self._armed = True

    def disarm(self):
        """Disable detection (tool is performing an action)."""
        self._armed = False

    def stop(self):
        """Shut down both listeners."""
        self._armed = False
        self._mouse_listener.stop()
        self._keyboard_listener.stop()

    # -- pynput callbacks --------------------------------------------------

    def _trigger(self):
        """Fire the callback once, then disarm."""
        if self._armed and not self._fired:
            self._fired = True
            self._armed = False
            self._callback()

    def _on_move(self, x, y):
        if not self._armed:
            return
        ox, oy = self._mouse_origin
        if abs(x - ox) + abs(y - oy) >= self.MOUSE_THRESHOLD:
            self._trigger()

    def _on_click(self, x, y, button, pressed):
        if pressed:
            self._trigger()

    def _on_scroll(self, x, y, dx, dy):
        self._trigger()

    def _on_press(self, key):
        self._trigger()
