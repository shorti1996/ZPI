class Home:
    def __init__(self, initial_conditions):
        self.temp = initial_conditions("temp")


    def calc_state(self, weather_data, control_data, delta):
        self.temp = self.temp + delta * (control_data["temp"])
