import sqlite3
import scoreItem

class main:
	result = 0 
	threshold = 0.59 # threshold for malicious web pages
		
	def __init__(self,db_name = None,db_name1 = None):

		conn = sqlite3.connect(db_name)
		c = conn.cursor()
		
		db = c.execute('select distinct url, frameRatio, jsRatio,linkRatio from Frame group by url')
		
		#declare and store URL into scoreItemList
		scoreItemList = []
		for row in db:
			x = scoreItem.urlScoreItem(row[0],row[1],row[2],row[3])
			scoreItemList.append(x)	
			
		#calculate zeroiFrame
		sampleLst = ["height='0'","width='0'","display:none","opacity:0","visibility:hidden"]
		db1 = c.execute('select * from Frame')
		for row in db1:
			for index in range(len(sampleLst)):			
				if row[2].find(sampleLst[index]) != -1:
					for item in scoreItemList:
						if item.url == row[0]:
							item.incrementZeroiFrame()
					break
			
		#calculate jsFunction
		sampleLst = ["eval","setTimeout","link","unescape","exec","search","unbound","escape"]		
		for row in db1:
			for index in range(len(sampleLst)):
				if row[5].find(sampleLst[index]) != -1:
					for item in scoreItemList:
						if item.url == row[0]:
							item.incrementScript()
					break
		

		conn2 = sqlite3.connect(db_name1)
		c2 = conn2.cursor()
		db2 = c2.execute('select * from Scripts')
		#calculate jsFunction
		sampleLst = ["eval","setTimeout","link","unescape","exec","unbound","escape"]		
		for row in db2:
			for index in range(len(sampleLst)):
				if row[1].find(sampleLst[index]) != -1:
					for item in scoreItemList:
						if row[0].find(item.url) != -1:
							item.incrementScript()
					break
				
		percentage = 0		
		for item in scoreItemList:
			item.calScore()
			item.checkMalicious(self.threshold)
			if item.isMalicous == True:
				percentage += 1
			print(item)

		self.result = (str(percentage*100/len(scoreItemList)) + "%")

print(main("New_Mixed_bag_Frames.db","New_Mixed_bag.db").result)