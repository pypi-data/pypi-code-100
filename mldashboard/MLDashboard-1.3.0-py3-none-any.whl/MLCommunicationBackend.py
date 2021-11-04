import warnings

class MessageMode:
    #control characters
    Start = 0
    End = 1
    ForceUpdate = 2
    CustomData = 3 #handles status module comm
    Command = 4 #handles data return

    #callback messages
    Train_Begin = 10
    Train_End = 11
    Predict_Begin = 12
    Predict_End = 13
    Test_Begin = 14 #evaluate
    Test_End = 15

    Epoch_Begin = 16 #training only
    Epoch_End = 17

    Train_Batch_Begin = 18 #batch methods
    Train_Batch_End = 19
    Test_Batch_Begin = 20
    Test_Batch_End = 21
    Predict_Batch_Begin = 22
    Predict_Batch_End = 23

    #data request messages
    Train_Set_Sample = 30
    Test_Set_Sample = 31
    Pred_Sample = 32 #from test set
    Pred_Sample_Train = 33
    Wrong_Pred_Sample = 34 #from test set
    Wrong_Pred_Sample_Train = 35

def getMode(x: int):
    for y in [a for a in dir(MessageMode) if not a.startswith('__')]:
        if MessageMode().__getattribute__(y) == x:
            return y
    warnings.warn("No valid mode found.")

class Message:
    def __init__(self, mode: int, body: dict):
        self.mode = mode
        self.body = body

    def __repr__(self):
        return ("Message with mode: " + getMode(self.mode) + " and data payload: " + str(self.body) +
                " At location: " + object.__repr__(self))
