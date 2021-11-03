# SPDX-FileCopyrightText: 2020 G2Elab / MAGE
#
# SPDX-License-Identifier: Apache-2.0

from typing import List

class Solution:
    """
    iData = list : model inputs (optimization variables)
    oData = list : model outputs (objective functions + constraints)
    """
    iData = []
    oData = []

    def __init__(self, inp, out):
        self.iData = inp
        self.oData = out


class Iterations:
    """
    At each gradient computation, gets the inputs and outputs of the model.
    solutions: class Solution
    iNames = list : model inputs
    oNames = list : model outputs
    """
    solutions: Solution = []
    iNames = []
    oNames = []

    def __init__(self, iNames, oNames, handler = None):
        self.iNames = iNames
        self.oNames = oNames
        self.solutions = []
        self.handler = handler #TODO : n'est plus utilisé. Modifier la création
        # automatique du Handler (dans constructeur Wrapper) lorsqu'il s'agit d'un affichage dynamique : dynamicPlot.update

    def updateData(self, inp, out):
        """
        Adds the inputs and outputs of the model computed at each iteration
        to the Solution class.
        :param inp: list of model inputs
        :param out: list of model outputs
        :return: /
        """
        self.solutions.append(Solution(inp.copy(), out.copy()))
        if (self.handler):
            self.handler(self.solutions)

    def print(self):
        """
        Displays the inputs and outputs of the model at each iteration.
        :return: /
        """
        print([sol.iData for sol in self.solutions])
        print([sol.oData for sol in self.solutions])

    def plotXY(self):
        import noload.gui.plotIterations as pi
        pi.plotXY(self)
    def plotIO(self):
        import noload.gui.plotIterations as pi
        pi.plotIO(self)


def printHandler(sols:List[Solution]):
    """
    Displays the inputs and outputs of the model computed during the last
    iteration.
    :param sols: class Solution
    :return: /
    """
    sols
    print(sols[-1].iData)
    print(sols[-1].oData)

