class FPS:
    def __init__(self, maxLength):
        self.list = []
        self.maxLength = maxLength
    
    def addFrameTime(self, time):
        self.list.append(time)
        if len(self.list) > self.maxLength:
            del self.list[0]

    def getFps(self):
        return 1//(sum(self.list)/len(self.list))