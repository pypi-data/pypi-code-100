class ConductivityValidator:
    def __init__(self, df) -> None:
        self.df = df

    def standard_deviation_is_less_than(self, threshold):
        deviation = self.df["conductivity"].std()
        return deviation < threshold

    def standard_deviation_is_more_than(self, threshold):
        deviation = self.df["conductivity"].std()
        return deviation > threshold

    def average_is_less_than(self, threshold):
        average = self.df["conductivity"].mean()
        return average < threshold

    def average_is_more_than(self, threshold):
        average = self.df["conductivity"].mean()
        return average > threshold

    def variance_is_less_than(self, threshold):
        variance = self.df["conductivity"].var()
        return variance < threshold

    def variance_is_more_than(self, threshold):
        variance = self.df["conductivity"].var()
        return variance > threshold
