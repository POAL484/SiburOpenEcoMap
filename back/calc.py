#представьте типо расчеты

class CalculationsFund:
    def __init__(self):
        ### подгрузка из дб
        self.last_temp = 0
        self.temperature_speed = 0
        self.last_timestamps = {"05a3c7d1-e7d0-46c8-bc13-3a0358a0d287": "2024-07-04 00:55:34"} #представьте подгрузку из дб. Она тут есть честно честно

    def __call__(self, uid: str):
        ### представьте интересные данные
        return self.temperature_speed

fund = CalculationsFund()

def calc_new_vals(vals: dict):
    fund.temperature_speed = vals["temp"] - fund.last_temp
    fund.last_temp = vals["temp"]
