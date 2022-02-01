import sys
from time import perf_counter

class ProgressBar:

    def __init__(self, total_steps:int, length=30, fill="=", end=">", fill_space=" "):
        self._total_steps = total_steps
        self._length = length
        self._fill = fill
        self._end = fill if end == "" else end
        self._fill_space = " " if fill_space == "" else fill_space
        self._increment = max(1, length // total_steps)
        self._bar_format = "{step_info} {bar} -{total_sec}{steps_per_sec:.4f}s/sample"
        self.reset()

    def reset(self):
        self._progress_bar_step = self._increment
        self._current_step = 1
        self._step_info = ""
        self._last_time = 0
        self._time_between_updates = list()

    def update(self, extra=None):
        self._increment_steps()

        if self._current_step <= self._total_steps:
            self._print(extra=extra)
        else:
            self.finish(extra)
    

    def _print(self, total_sec=" ", extra=None):
        step_info = self._get_step_info()
        bar = self._bar_format.format(
            step_info=step_info,
            bar=self._get_bar(),
            total_sec=total_sec,
            steps_per_sec=self._get_step_per_second()
        )

        bar = bar if extra is None else f"{bar} - {extra}"

        sys.stdout.write('\r' + bar)

    def _increment_steps(self):
        if self._current_step % (self._total_steps/self._length) < 1:
            self._progress_bar_step = min(self._progress_bar_step + self._increment, self._length)
        self._current_step = self._current_step + 1
        
        now = 0 if self._last_time == 0 else perf_counter()
        elapsed_time = now - self._last_time
        if elapsed_time > 0:
            self._time_between_updates.append(elapsed_time)
        self._last_time = perf_counter()

    def _get_step_info(self):
        digits = len(str(self._total_steps))
        current_step = str(self._current_step).rjust(digits)

        return f"{current_step}/{self._total_steps}"

    def _get_bar(self):
        fill = self._fill * self._progress_bar_step
        fill_space_length = (self._length - self._progress_bar_step)
        end = self._fill if fill_space_length == 0 else self._end
        fill_space = self._fill_space * (fill_space_length)

        return f"[{fill}{end}{fill_space}]"

    def _get_step_per_second(self):
        if len(self._time_between_updates) == 0:
            return 0

        return sum(self._time_between_updates) / len(self._time_between_updates)

    def finish(self, extra=None):
        elapsed_time = perf_counter() - self._last_time
        self._current_step = self._total_steps
        self._progress_bar_step = self._length
        self._time_between_updates.append(elapsed_time)

        total_exec = sum(self._time_between_updates)
        self._print(total_sec=f" {total_exec:.2f}s ", extra=extra)
        sys.stdout.write("\n")
        self.reset()
