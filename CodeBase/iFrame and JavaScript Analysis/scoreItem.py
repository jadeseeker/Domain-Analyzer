class urlScoreItem:
    #weight = frameRatio + zeroFrameRatio + linkRatio + jsRatio + scriptRatio
    url = ''
    iframeRatio = 0
    linkRatio = 0
    jsRatio = 0
    totalScore = 0
    isMalicous = False
    zeroiFrameCounter = 0
    scriptCounter = 0
    
    def __init__(self, url,iframeRatio,linkRatio,jsRatio):
        self.url = url
        self.iframeRatio = iframeRatio
        self.linkRatio = linkRatio
        self.jsRatio = jsRatio    
               
    def setScore(self,score):
        self.totalScore = score
        
    def setMalicious(self,result):
        self.isMalicous = result	
  
    def calScore(self):
        iframeRatioScore = -1
        zeroiFrameScore = -1
        scriptScore = -1
        if self.iframeRatio*10000 >1.43:
            iframeRatioScore = 1
        else:
            iframeRatioScore = 0
            
        if self.zeroiFrameCounter >1.82:
            zeroiFrameScore = 1
        else:
            zeroiFrameScore = 0
        
        if self.scriptCounter > 4.43:
            scriptScore = 1
        else:
            scriptScore = 0
       
        self.totalScore = iframeRatioScore*0.25 + zeroiFrameScore*0.4 + scriptScore*0.35
        
    def incrementZeroiFrame(self):
        self.zeroiFrameCounter += 1
        
    def incrementScript(self):
        self.scriptCounter += 1
 
    def checkMalicious(self, threshold):
        if self.totalScore < threshold:
            self.isMalicous = False
        else:
            self.isMalicous = True
            
    def __str__(self):
        return 'url:' + self.url + " frameRatio: " + str(self.iframeRatio) + " linkRatio:" + str(self.linkRatio) + " jsRatio:" + str(self.jsRatio) + " scriptNum:" + str(self.scriptCounter) + " zeroiFrameNum:" + str(self.zeroiFrameCounter) +" total Score:" + str(self.totalScore) + " isMalicious:" + str(self.isMalicous)