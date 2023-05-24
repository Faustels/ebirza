import sched, time


def newSchedule(seconds, offset, function):
    def ScheduledFunction(seconds, function, scheduler):
        scheduler.enter(seconds, 1, ScheduledFunction, (seconds, function, scheduler))
        function()
    scheduler = sched.scheduler(time.time, time.sleep)
    scheduler.enter(seconds - ((time.time() - offset) % seconds), 1, ScheduledFunction, (seconds, function, scheduler))
    scheduler.run(blocking=False)