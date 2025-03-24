import time

class RunTimeAnalysis:
    def __init__(self, no_movement_threshold, no_trial_threshold, no_trial_period):
        self.stagnancy = no_movement_threshold
        self.sluggishness_limit = no_trial_threshold
        self.sluggishness_period = no_trial_period
        self.trial_list = []
        self.start_time = time.time()
        self.mouse_stagnant_time = [self.start_time, self.start_time]
        self.mouse_stagnant_reported = [False, False]
        self.session_sluggish_reported = False

    def reset_analysis_timers(self):
        self.start_time = time.time()
        self.mouse_stagnant_time = [self.start_time, self.start_time]

    def new_mouse_position(self, mouse):
        self.mouse_stagnant_time[mouse - 1] = time.time()

    def new_trial(self):
        self.trial_list.append(time.time())

    def is_mouse_stagnant(self, mouse):
        report_stagnancy = False
        if time.time() - self.mouse_stagnant_time[mouse - 1] > self.stagnancy:
            if not self.mouse_stagnant_reported[mouse - 1]:
                report_stagnancy = True
                self.mouse_stagnant_reported[mouse - 1] = True
        else:
            self.mouse_stagnant_reported[mouse - 1] = False
        return report_stagnancy

    def is_session_sluggish(self):
        start_sluggish_window = time.time() - self.sluggishness_period
        report_sluggishness = False

        if self.trial_list:   # if trial list not empty, delete all old trial entries
            for idx in range(len(self.trial_list)):
                if self.trial_list[idx] > start_sluggish_window:
                    break
            self.trial_list = self.trial_list[idx:]

        if len(self.trial_list) < self.sluggishness_limit:
            if not self.session_sluggish_reported:
                report_sluggishness = True
                self.session_sluggish_reported = True
        else:
            self.session_sluggish_reported = False

        return report_sluggishness

    def event_analysis(self, report_event: callable):
        message_time = time.time() - self.start_time
        minutes = int(message_time / 60)
        seconds = int(message_time) % 60
        msgTimeText = f'{minutes:02d}:{seconds:02d}'

        if self.is_mouse_stagnant(0):
            report_event(f'{msgTimeText} Mouse 1 did not change location in the last {self.stagnancy} seconds')
        if self.is_mouse_stagnant(1):
            report_event(f'{msgTimeText} Mouse 2 did not change location in the last {self.stagnancy} seconds')
        if time.time() - self.start_time > self.sluggishness_period and self.is_session_sluggish():
            report_event(f'{msgTimeText} Less than {self.sluggishness_limit} trials in the last {self.sluggishness_period} seconds')

