
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
#liste_trans : list[Transition]
liste_trans = [t1,t2,t3,t4,t5,t6]
#liste_etats
liste_etats = [s1,s2,s3]
#auto : Automate
aut = Automate(liste_trans, label = "A")
# print(aut)
#aut1 : Automate
aut1 = Automate(liste_trans, liste_etats, label = "A1" )
# print(aut1)

#aut.show("auto")

#3

auto_fichier = Automate.creationAutomate("auto.txt")



# # etat initial
# print(auto_fichier)

# # 2.2.1
# auto_fichier.removeTransition(t1)
# print(auto_fichier)
# auto_fichier.addTransition(t1)
# print(auto_fichier)

# # 2.2.2
# auto_fichier.removeState(s1)
# print(auto_fichier)
# auto_fichier.addState(s1)
# print(auto_fichier)

# # etat final

# # 2.2.3
# s1TranLi = auto_fichier.getListTransitionsFrom(s1)
# print(s1TranLi)

# # 3.1
# print(auto_fichier.succ(liste_etats, "a"))

# # 3.2
# assert(Automate.accepte(auto_fichier, "aaba"))
# assert(not Automate.accepte(auto_fichier, "a"))

# 3.3
tt1a = Transition(s1, "a", s2)
tt1b = Transition(s1, "b", s2)
tt1c = Transition(s1, "c", s2)
tt2a = Transition(s2, "a", s3)
tt2b = Transition(s2, "b", s3)
tt2c = Transition(s2, "c", s3)
tt3a = Transition(s3, "a", s1)
tt3b = Transition(s3, "b", s1)
tt3c = Transition(s3, "c", s1)
testListTransition = [tt1a, tt1b, tt1c, tt2a, tt2b, tt2c, tt3a, tt3b, tt3c]
auto_test = Automate(testListTransition, label = "Test1")
assert(Automate.estComplet(auto_test, "abc"))
auto_test.removeTransition(tt2c)
assert(not Automate.estComplet(auto_test, "abc"))
auto_test.addTransition(tt2c)
assert(Automate.estComplet(auto_test, "abc"))

# # 3.4 extends 3.3
assert(Automate.estDeterministe(auto_test))
faultTransition = Transition(s2, "a", s1)
auto_test.addTransition(faultTransition)
assert(not Automate.estDeterministe(auto_test))
auto_test.removeTransition(faultTransition)
auto_test.removeTransition(tt3c)
assert(Automate.estDeterministe(auto_test))

# # 3.5 extends 3.3
assert(Automate.estComplet(Automate.completeAutomate(auto_test, "abc"), "abc"))
assert(Automate.estComplet(Automate.completeAutomate(aut, "abc"), "abc"))
assert(Automate.estComplet(Automate.completeAutomate(auto_fichier, "abc"), "abc"))

# # 4
assert(Automate.estDeterministe(Automate.determinisation(auto_test)))
auto_test.removeTransition(faultTransition)
auto_test.removeTransition(tt3c)
assert(Automate.estDeterministe(Automate.determinisation(auto_test)))
assert(Automate.estDeterministe(Automate.determinisation(aut)))
assert(Automate.estComplet(Automate.determinisation(auto_test),"abc"))
s3 = State(2, False, False)
s4 = State(3, False, True)
tt0a = Transition(s1, "a", s1)
tt0b = Transition(s1, "b", s1)
tt3a = Transition(s3, "a", s4)
auto_test2 = Automate([tt0a, tt0b, tt1a, tt2b, tt3a])

# # 5
# # 5
s1 = State(0,True,False)
s2 = State(1,False,False)
s3 = State(2, False, False)
s4 = State(3, False, True)
tt0a = Transition(s1, "a", s1)
tt0b = Transition(s1, "b", s1)
tt1a = Transition(s1, "a", s2)
tt2b = Transition(s2, "b", s3)
tt3a = Transition(s3, "a", s4)
auto_test2 = Automate([tt0a, tt0b, tt1a, tt2b, tt3a])
auto_test2_det = Automate.determinisation(auto_test2)
# print(auto_test2)
# print(auto_test2_det)
assert(not Automate.estDeterministe(auto_test2))
assert(Automate.estDeterministe(Automate.determinisation(auto_test2)))
assert(Automate.estDeterministe(Automate.determinisation(auto_test)))

# 5.1
impaireA = Automate.creationAutomate("impaireA.txt")
termineParB = Automate.creationAutomate("termineParB.txt")
impaireA.show("impareA")
termineParB.show("termineParB")
assert(not Automate.accepte(impaireA,"aaababbbb"))
assert(Automate.accepte(impaireA,"aaababbbba"))
assert(Automate.accepte(termineParB,"aaababbbb"))
assert(not Automate.accepte(termineParB,"aaababbbba"))

# 5.1.1
assert(Automate.accepte(auto_fichier, "aaba"))
assert(not Automate.accepte(Automate.complementaire(auto_fichier,"ab"), "aaba"))
assert(not Automate.accepte(auto_fichier, "a"))
assert(Automate.accepte(Automate.complementaire(auto_fichier,"ab"), "a"))

# 5.1.2
intersection = Automate.intersection(impaireA, termineParB)
intersection.show("intersection")
assert(not Automate.accepte(intersection,"aaababbbb"))
assert(not Automate.accepte(intersection,"aaababbbba"))
assert(Automate.accepte(intersection,"aaababbbbab"))

# 5.1.3
union = Automate.union(impaireA, termineParB)
union.show("union")
assert(Automate.accepte(union,"aaababbbb"))
assert(Automate.accepte(union,"aaababbbba"))
assert(Automate.accepte(union,"aaababbbbab"))

# 5.2
motABA = Automate.creationAutomate("motABA.txt")
motABA.show("motABA")
assert(Automate.accepte(motABA,"aba"))
assert(not Automate.accepte(motABA,""))
assert(not Automate.accepte(motABA,"aaba"))
assert(not Automate.accepte(motABA,"abaaba"))
# cocatenation
conca = Automate.concatenation(motABA, impaireA)
conca.show("conca")
assert(Automate.accepte(conca,"abaa"))
assert(not Automate.accepte(conca,"aba"))
assert(Automate.accepte(conca,"abababaa"))

# etoile
ABAEtoile = Automate.etoile(motABA)
ABAEtoile.show("ABAEtoile")
assert(Automate.accepte(ABAEtoile,""))
assert(Automate.accepte(ABAEtoile,"abaabaabaaba"))
assert(not Automate.accepte(motABA,"ab"))

# fin
print("If this phrase is printed, all tests success.")