import random
import numpy as np

class QLearning:
    def __init__(self,nbAction:int,gamma:float=0.9,learningRate:float=0.1):
        """
        nbParam : Number of action in state
        gamma : Reward power [0;1] (0.1 long path priority, 0.9 short path priority)
        learningRate : Learning power [0;1]
        """
        #Number of action
        self.nbAction = nbAction
        #Qtable
        self.QTable = np.zeros(shape=(0,nbAction))
        #Qtable link between index and state value
        self.Qlink = np.chararray(shape=(0,1))
        #gamma
        self.gamma = gamma
        #Learning Rate
        self.learningRate = learningRate
        #Old action
        self.oldAction = -1
        #New action
        self.newAction = -1
    def takeAction(self,state:str,epsilon:int):
        """
        state : Current State
        epsilone : exploration value [0;1]
        Return action
        """
        #Epsilon greedy
        if random.uniform(0,1) < epsilon:   #Exploration
            #Get random action
            action = random.randint(0,self.nbAction-1)
        else:   #Greedy action
            #Index of the state in QTable
            stateIndex = None
            #If state are not registred in the Qlink
            if not(state in self.Qlink):
                #Register new state
                self.Qlink = np.append(self.Qlink,[state])
                self.QTable = np.append(self.QTable,[np.zeros(shape=(self.nbAction))],axis=0)
            stateIndex = np.where(self.Qlink == state)[0][0]

            #Get the action with the highest Value Function in our state
            action = np.argmax(self.QTable[stateIndex])
        #Change the actions order
        self.oldAction = self.newAction
        self.newAction = action
        return action
    def updateQFunction(self,currentState:str,oldState:str,reward:int):
        """
        """
        #We get the best option for the next state
        self.takeAction(currentState,0.0)
        #Index of the next state in QTable
        nextStateIndex = None
        #If state are not registred in the Qlink
        if not(currentState in self.Qlink):
            #Register new state
            self.Qlink = np.append(self.Qlink,currentState)
            self.QTable = np.append(self.QTable,[np.zeros(shape=(self.nbAction))],axis=0)
        nextStateIndex = np.where(self.Qlink == currentState)[0][0]
        
        #Index of the current state in QTable
        currentStateIndex = None
        #If state are not registred in the Qlink
        if not(oldState in self.Qlink):
            #Register new state
            self.Qlink = np.append(self.Qlink,oldState)
            self.QTable = np.append(self.QTable,[np.zeros(shape=(self.nbAction))],axis=0)
        currentStateIndex = np.where(self.Qlink == oldState)[0][0]

        #On prend la difference entre l'etat+1 et l'etat de base
        a = self.QTable[nextStateIndex][self.newAction] - self.QTable[currentStateIndex][self.oldAction]
        #on le multiplie au gamma
        a = self.gamma*a
        #on additionne le reward
        a = reward + a
        #on le multiplie au learning rate
        a = self.learningRate*a
        #on ajoute la difference
        self.QTable[currentStateIndex][self.oldAction] += a
    def saveQTable(self,path:str):
        """
        path : path+filename (without file extension)
        """
        np.savez(path,self.QTable,self.Qlink)
    def loadQTable(self,path:str):
        """
        Args:
            path (str): Path to the QTable file (without file extension)
        """
        path = path+".npz"
        self.QTable = np.load(path)["arr_0"]
        self.Qlink = np.load(path)["arr_1"]