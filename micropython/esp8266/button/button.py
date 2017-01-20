from machine import Pin, Timer
from time import ticks_ms, ticks_diff


class Button:
    IDLE = const(0)
    PRESS_WAIT = const(1)
    RELEASE_WAIT = const(2)
    RELEASE = const(3)

    COOLOFF = const(101)

    DEBOUNCE_TIME = const(10)
    COOLOFF_TIME = const(30)
    MULTICLICK_DELTA = const(450)

    def __init__(self, pin_number, max_clicks=3):
        self.timer = Timer(-1)
        self.pin = Pin(pin_number, Pin.IN, Pin.PULL_UP)
        self.state = self.IDLE
        self.last_event = 0
        self.last_click = 0
        # create bound version of debounce to avoid heap
        # allocation in IRQ handler
        self._debounce_callback = self.debounce
        self._click = 0
        self._clicks = [-1] * max_clicks
        self._max_clicks = max_clicks
        # setup irq as last init action
        self.pin.irq(handler=self.push, trigger=Pin.IRQ_FALLING)

    def push(self, _):
        if self.state != self.IDLE:
            return  # ignore fast repeated presses
        self._debounce_callback(self.timer)

    def ready(self):
        if self.state != self.IDLE:
            return False  # middle of release procedures
        if self._clicks == 0:
            return False  # no clicks present
        if self._clicks == self._max_clicks:
            return True  # allow to read max_clicks events w/o multiclick delay
        if ticks_diff(ticks_ms(), self.last_click) < self.MULTICLICK_DELTA:
            return False  # still waiting for multiclick
        return True

    @property
    def clicks(self):
        c = self._clicks.copy()
        self.reset_clicks()
        return c

    def register_click(self):
        if self._click == len(self._clicks):
            self.reset_clicks()
        now = ticks_ms()
        click_duration = ticks_diff(now, self.last_event)
        delta_form_last_release = ticks_diff(now, self.last_click) - click_duration
        if delta_form_last_release > self.MULTICLICK_DELTA:
            self.reset_clicks()

        self.last_click = now
        print("Click ", self._click, click_duration, delta_form_last_release)
        self._clicks[self._click] = click_duration
        self._click += 1

    def reset_clicks(self):
        self._click = 0
        for i in range(self._max_clicks):
            self._clicks[i] = -1

    def debounce(self, timer):
        state = self.state
        if state == self.IDLE:
            self.last_event = ticks_ms()
            self.state = self.PRESS_WAIT
            return self.schedule_debounce(timer, self.DEBOUNCE_TIME)
        if state == self.COOLOFF:
            self.state = self.IDLE
            return
        if state == self.PRESS_WAIT:
            self.state = self.COOLOFF if self.pin.value() else self.RELEASE_WAIT
            return self.schedule_debounce(timer, self.DEBOUNCE_TIME)
        if state == self.RELEASE_WAIT:
            if self.pin.value() == 0:
                return self.schedule_debounce(timer, self.DEBOUNCE_TIME)
            self.register_click()
            self.last_event = ticks_ms()
            self.state = self.COOLOFF
            self.schedule_debounce(timer, self.COOLOFF_TIME)

    def schedule_debounce(self, timer, period):
        timer.init(
            period=period,
            mode=Timer.ONE_SHOT,
            callback=self._debounce_callback
        )
