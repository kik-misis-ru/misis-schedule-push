class PushTemplate:
    def __init__(self, day, count_lessons, lesson, start_time):
        self.day=day
        self.count_lesson=count_lessons
        self.lesson=lesson
        self.start_time=start_time
    day: str
    count_lesson: str
    lesson: str
    start_time: str

class UserPush():
    sub: str
    hour: int
    minute: int