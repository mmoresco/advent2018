from util import Input
from collections import namedtuple, Counter
from operator import attrgetter
import re
from datetime import datetime

# https://adventofcode.com/2018/day/4

Log = namedtuple('Log', ['ts', 'message'])
Guard = namedtuple('Guard', ['id', 'minutes'])


def parse(lines):
    logs = []
    for l in lines:
        ts, message = l.split(']')
        ts = datetime.strptime(ts,"[%Y-%m-%d %H:%M")
        log = Log(ts, message.strip())
        logs.append(log)

    logs.sort(key=attrgetter('ts'))
    return logs


def tally_guards(logs):
    guards = {}
    current_guard = None
    nap_start = 0
    for log in logs:
        message = log.message
        ts = log.ts

        if 'begins' in message:
            current_id = int(re.findall(r'\d+', message)[0])
            if current_id not in guards:
                current_guard = Guard(current_id, Counter())
                guards[current_id] = current_guard
            else:
                current_guard = guards[current_id]

        elif 'falls' in message:
            nap_start = ts

        elif 'wake' in message:

            slept_minutes = int((ts - nap_start).total_seconds() / 60)
            for i in range(0, slept_minutes):
                current_guard.minutes[(i + nap_start.minute) % 60] += 1

    return guards


def sleepiest_guard(guards):
    return max([(name, sum(guard.minutes.values())) for name, guard in guards.items()],
                       key=lambda x: x[1])[0]


def most_common_minute(guard):
    return guard.minutes.most_common(1)[0][0]


def predictable_minute(guards):
    guards_favorite_minutes = [(guard.id, guard.minutes.most_common(1)[0])
                               for guard in guards.values() if guard.minutes]
    guard, (minute, count) = max(guards_favorite_minutes, key=lambda x: x[1][1])
    return (guard, minute)

test = ["[1518-11-01 23:58] Guard #99 begins shift",
        "[1518-11-01 00:05] falls asleep",
        "[1518-11-01 00:55] wakes up",
        "[1518-11-02 00:40] falls asleep",
        "[1518-11-01 00:30] falls asleep",
        "[1518-11-02 01:01] wakes up",
        "[1518-11-01 00:00] Guard #10 begins shift",
        "[1518-11-01 00:25] wakes up"]

test_logs = parse(test)
assert test_logs[0].message == 'Guard #10 begins shift'
assert test_logs[-1].message == 'wakes up'

logs = parse(Input(4))
guards = tally_guards(logs)

# Part 1
sleepiest = sleepiest_guard(guards)
print(sleepiest * most_common_minute(guards[sleepiest]))

# Part 2
guard, minute = predictable_minute(guards)
print(guard * minute)