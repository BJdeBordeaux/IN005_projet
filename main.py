from automate import * 

#s1 : State
s1 = State(0,True,False)
#s2 : State
s2 = State(1,False,False)
#s3 : State
s3 = State(2,False ,True)
#t1 : Transition 
t1 = Transition(s1,"a",s1)
#t2 : Transition 
t2 = Transition(s1,"b",s2)
#t3 : Transition 
t3 = Transition(s2,"a",s3)
#t4 : Transition 
t4 = Transition(s2,"b",s3)
#t5 : Transition 
t5 = Transition(s3,"a",s1)
#t6 : Transition 
t6 = Transition(s3,"b",s2)
#liste : list[Transition]
liste = [t1,t2,t3,t4,t5,t6]

#auto : Automate
aut = Automate(liste)
print(aut)

#


auto_fichier = Automate.creationAutomate("auto.txt")
# print(auto_fichier)
