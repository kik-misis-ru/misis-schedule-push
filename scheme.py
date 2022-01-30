class PushTemplate:
    def __init__(self, day, count_lessons, lesson, start_time):
        self.day=day
        self.count_lesson=count_lessons
        self.lesson=lesson
        self.start_time=start_time
    day: str
    count_lesson: str
    lesson: str
    start_lesson_info: str
    start_time: str

class TimeFrame:
    def __init__(self, start_time, finish_time, start_date, end_date):
        self.start_time = start_time
        self.start_date = start_date
        self.finish_time = finish_time
        self.end_date = end_date
    start_time : str
    finish_time : str 
    start_date : str
    end_date : str
