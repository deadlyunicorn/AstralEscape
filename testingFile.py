class Score:
    def __init__(self,difficulty,score,date):
        self.difficulty=difficulty
        self.date=date
        self.score=score

easy=[]
normal=[]
hard=[] 


with open("AstralEscapeScore.txt") as file:

  currentDifficulty=0

  entryFound=False
  registeredDifficulty="None"
  registeredScore="None"
  registeredDate="None"


  for line in file:

      if entryFound:
          if line.find("Difficulty:")!=-1:
              diffFinIndex=len("Difficulty:")
              registeredDifficulty=line[diffFinIndex:]
          elif line.find("Score:")!=-1:
              scoreFinIndex=len("Score:")
              registeredScore=line[scoreFinIndex:]
          elif line.find("Date:")!=-1:
              dateFinIndex=len("Date:")
              registeredDate=line[dateFinIndex:]
          elif line.find("END")!=-1:
              
              entryFound=False
              
              if registeredDifficulty.strip()=="EASY":
                  easy.append(Score(registeredDifficulty,registeredScore,registeredDate))
              elif registeredDifficulty.strip()=="NORMAL":
                  normal.append(Score(registeredDifficulty,registeredScore,registeredDate))
              elif registeredDifficulty.strip()=="HARD":
                  hard.append(Score(registeredDifficulty,registeredScore,registeredDate))
                  

      elif line.find("START"):
              entryFound=True

  hard_sorted=sorted(hard,key=lambda x:x.score)
  normal_sorted=sorted(normal,key=lambda x:x.score)
  easy_sorted=sorted(easy,key=lambda x:x.score)

  
  if registeredDifficulty=="None":
      print("No entries found.")
  else:
      
      for x in range(10):
        if(x>=len(hard_sorted)):
          break
        print("Hard")
        print(hard_sorted[x].score)
        print(hard_sorted[x].date)
      for x in range(10):
        if(x>=len(easy_sorted)):
          break
        print("Easy")
        print(easy_sorted[x].score)
        print(easy_sorted[x].date)
      for x in range(10):
        if(x>=len(normal_sorted)):
          break

        print("Normal")
        print(normal_sorted[x].score)
        print(normal_sorted[x].date)
        