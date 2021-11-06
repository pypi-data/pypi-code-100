from dataclasses import dataclass


@dataclass
class Indicator:
    Id: str
    Name: str
    Script: str
    FirstLevel: str
    SecondLevel: str


SuperTrend = Indicator(Id="STD;Supertrend",
                       Name="SuperTrend",
                       Script="Script@tv-scripting-101!",
                       FirstLevel="",
                       SecondLevel="")

TripleMovingAverages = Indicator(Id="PUB;y784PkOKflCjfhCiCB4ewuC0slMtB8PQ",
                                 Name="TripleMovingAverages",
                                 Script="Script@tv-scripting-101!",
                                 FirstLevel="",
                                 SecondLevel="")
Volume = Indicator(Id="",
                   Name="Volume",
                   Script="Volume",
                   FirstLevel="",
                   SecondLevel="")
