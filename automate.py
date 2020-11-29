# -*- coding: utf-8 -*-
from transition import *
from state import *
import os
import copy
from sp import *
from parser import *
from itertools import product
from automateBase import AutomateBase



class Automate(AutomateBase):
        
    def succElem(self, state, lettre):
        """State x str -> list[State]
        rend la liste des états accessibles à partir d'un état
        state par l'étiquette lettre
        """
        successeurs = []
        # t: Transitions
        for t in self.getListTransitionsFrom(state):
            if t.etiquette == lettre and t.stateDest not in successeurs:
                successeurs.append(t.stateDest)
        return successeurs


    def succ (self, listStates, lettre):
        """list[State] x str -> list[State]
        rend la liste des états accessibles à partir de la liste d'états
        listStates par l'étiquette lettre
        """
        # res: list[State]
        res = []
        # state : State
        for state in listStates :
            # transition : Transition
            for dest_state in self.succElem(state, lettre):
                if dest_state not in res : 
                    res.append(dest_state)
        return res
    

    """ Définition d'une fonction déterminant si un mot est accepté par un automate.
    Exemple :
            a=Automate.creationAutomate("monAutomate.txt")
            if Automate.accepte(a,"abc"):
                print "L'automate accepte le mot abc"
            else:
                print "L'automate n'accepte pas le mot abc"
    """
    @staticmethod
    def accepte(auto,mot) :
        """ Automate x str -> bool
        rend True si auto accepte mot, False sinon
        """
        # accepte : bool
        accepte = False
        # stateList : list[State]
        stateList = auto.getListInitialStates()
        for lettre in mot :
            stateList = auto.succ(stateList, lettre)
        for state in stateList:
            if state in auto.getListFinalStates():
                accepte = True
        return accepte


    @staticmethod
    def estComplet(auto,alphabet) :
        """ Automate x str -> bool
         rend True si auto est complet pour alphabet, False sinon
        """
        # stateList : list[State]
        stateList = auto.getListInitialStates()
        # currentList : list[State]
        currentList = auto.getListInitialStates()
        # nextList : list[State]
        nextList = []
        # end : bool
        end = False
        while(not end):
            for state in currentList:
                for lettre in alphabet:
                    if auto.succElem(state, lettre) == []:
                        return False
            for lettre in alphabet :
                nextList += auto.succ(currentList, lettre)
            for state in nextList:
                    if state not in stateList:
                        stateList.append(state)
            # # 上面那段或者这么写
            # stateList = list(set(nextList+ stateList))
            currentList = list(set(nextList))
            if set(auto.listStates) == set(stateList): 
                end = True
        return True


        
    @staticmethod
    def estDeterministe(auto) :
        """ Automate  -> bool
        rend True si auto est déterministe, False sinon
        """
        # currentList : list[State]
        currentList  = auto.getListInitialStates()
        if len(currentList) > 1:
            return False
        # stateList : list[State]
        stateList = auto.getListInitialStates()
        # nextList : list[State]
        nextList = []
        # end : bool
        end = False
        # alphabet : list[str]
        alphabet = []
        # deterministe : bool
        while(not end):
            for state in currentList:
                alphabet = []
                nextList = []
                for transition in auto.getListTransitionsFrom(state):
                    if(transition.etiquette in alphabet) : 
                        return False
                    alphabet.append(transition.etiquette)
                    if(transition.stateDest not in nextList) : 
                        nextList.append(transition.stateDest)
                if stateList == auto.listStates: 
                    end = True
                currentList = list(set(nextList))
                for state in nextList:
                    if state not in stateList:
                        stateList.append(state)
                # # or we can write
                # stateList = list(set(stateList + nextList))
        return True
        

       
    @staticmethod
    def completeAutomate(auto,alphabet) :
        """ Automate x str -> Automate
        rend l'automate complété d'auto, par rapport à alphabet
        """
        if(Automate.estComplet(auto, alphabet)):
            return auto
        auto_new = copy.deepcopy(auto)
        # currentList : list[State]
        currentList = auto_new.getListInitialStates()
        # stateList : list[State]
        stateList = auto_new.getListInitialStates()
        # nextList : list[State]
        nextList = []
        # end : bool
        end = False
        # pureState : State
        pureState = State(-1, False, False)
        while(not end):
            for state in currentList:
                for lettre in alphabet:
                    if auto_new.succElem(state, lettre) == []:
                        auto_new.addTransition(Transition(state, lettre, pureState))
                    nextList = list(set(nextList + auto_new.succ(currentList, lettre)))
            if set(stateList) > set(auto.listStates): 
                end = True
            stateList = list(set(stateList + nextList))
            currentList = list(set(nextList))
        for lettre in alphabet:
            auto_new.addTransition(Transition(pureState, lettre, pureState))
        return auto_new

       

    @staticmethod
    def determinisation(auto) :
        """ Automate  -> Automate
        rend l'automate déterminisé d'auto
        """
        if(Automate.estDeterministe(auto)):
            return copy.deepcopy(auto)
        # # auto_new : Automate 
        # auto_new = copy.deepcopy(auto)
        def isFinal(listState):
            """ list[State] -> bool
            Pour voir si l'etat comprenant listState est final
            """
            for state in listState:
                if state in auto.getListFinalStates():
                    return True
            return False
        
        # def createNewState(cpt, listState):
        #     """ int * list[State] -> State
        #     Creer un nouveau etat a partir d'une liste d'etats
        #     """
        #     return Automate(cpt, False, isFinal(listState))
        # currentList : list[State]
        currentList = auto.getListInitialStates()
        # stateList : list[list[[State]]]
        stateListList = []
        stateListList.append(currentList)
        # newStateList : list[State]
        newStateList = []
        if isFinal(currentList):
            isFinal = True
        initialState = State(0, True, isFinal)
        # dictListStateToState : dict{list[State] : State}
        dictListStateToState = dict()
        dictListStateToState[frozenset(set(currentList))] = initialState
        newStateList.append(initialState)
        # nextList : list[State]
        nextList = []
        # alphabet
        alphabet = []
        for transition in auto.listTransitions:
            alphabet.append(transition.etiquette)
        # newTransitionList : list[transition]
        newTransitionList = []
        entrer = 0
        sortir = 1
        while(entrer != sortir):
            entrer = sortir
            for lettre in alphabet:
                # print(stateListList)
                for listOfStates in stateListList.copy():
                    currentList = listOfStates
                    nextList = []
                    while(currentList != nextList):
                        nextList = auto.succ(currentList, lettre)
                        if nextList not in stateListList:
                            stateListList.append(nextList)
                            newState = State(sortir,False, isFinal(nextList))
                            newStateList.append(newState)
                            dictListStateToState[frozenset(set(nextList))] = newState
                            if Transition(dictListStateToState[frozenset(set(listOfStates))], lettre, newState) not in newTransitionList:
                                newTransitionList.append(Transition(dictListStateToState[frozenset(set(listOfStates))], lettre, newState))
                                sortir += 1
                            currentList = nextList
                        else:
                            break
        return Automate(newTransitionList)
            # # transitionList : list[transition]
            # transitionList = auto.getListTransitionsFrom(currentList)
            # for transition in transitionList:
            #     if transition.etiquette not in alphabet:
            #         alphabet.append(transition.etiquette)
            #     if transition.stateDest not in nextList:
            #         nextList.append(transition.stateDest)
            #     # auto.succ(stateSrc, )
            # if stateList != auto.listStates:
            #     end = True
        # # obtenir l'ensemble de parties
        # stateList = auto.listStates
        # basicStateList = []
        # for state in stateList:
        #     basicStateList.append({state})
        # stateSetList = basicStateList
        # currentSetList = basicStateList
        # nextSetList = []
        # end = False
        # while(not end):
        #     nextSetList = []
        #     for part in currentSetList:
        #         for basicPart in basicStateList:
        #             if basicPart <= part:
        #                 continue
        #             nextSetList.append(part | basicPart)
        #     for stateL in nextSetList:
        #         if stateL not in stateSetList:
        #             stateSetList.append(stateL)
        #     if currentSetList == nextSetList:
        #         end = True
        #     currentSetList = nextSetList
        # assert(len(stateSetList) == 2**len(stateList)-1)
        # # # obtenir l'ensemble de transition
        # alphabet = set()
        # for transition in auto.listTransitions:
        #     alphabet.add(transition.etiquette)
        # newListTransitions = []
        # newListInitialStates = []
        # newListFinalStates = []
        # for stateSetX in stateSetList:
        #     if stateSetX & set(auto.getListFinalStates()) != set():
        #         newListFinalStates.append(stateSetX)
        # newListStates = []
        # matchIwithCpt = []
        # matchIwithCpt.append((-1,-1))
        # print(matchIwithCpt)
        # newSetInitialStates = set()
        # for element in auto.getListInitialStates():
        #     newSetInitialStates.add(element)
        # newSetFinalStates = set()
        # for element in auto.getListFinalStates():
        #     newSetFinalStates.add(element)
        # for i in range(len(stateSetList)):
        #     cpt = 0
        #     # stateSetList[i] == stateSetX
        #     for lettre in alphabet:
        #         srcDest = []
        #         h = "here"
        #         try:
        #             destIndex = stateSetList.index(set(auto.succ(list(stateSetList[i]), lettre)))
        #             if destIndex != -1:
        #                 if stateSetList[i] == newSetInitialStates and stateSetList[i] & newSetFinalStates != set():
        #                     initial = True
        #                     final = True
        #                 elif stateSetList[i] == newSetInitialStates:
        #                     initial = True
        #                     final = True
        #                 elif stateSetList[i] & newSetFinalStates != set():
        #                     initial = False
        #                     final = True
        #                 else:
        #                     initial = False
        #                     final = False
        #                 existe = False
        #                 for a,b in matchIwithCpt:
        #                     if a == i:
        #                         existe = True
        #                 if existe:
        #                     srcDest.append(newListStates.index(b))
        #                 else:
        #                     srcDest.append((State(cpt, initial, final)))
        #                     newListStates.append(srcDest[0])
        #                     matchIwithCpt.append((i, cpt))
        #                     cpt += 1
        #                 # pour etat d'arrivee
        #                 if stateSetList[destIndex] == newSetInitialStates and stateSetList[destIndex] & newSetFinalStates != set():
        #                     initial = True
        #                     final = True
        #                 elif stateSetList[destIndex] == newSetInitialStates:
        #                     initial = True
        #                     final = True
        #                 elif stateSetList[destIndex] & newSetFinalStates != set():
        #                     initial = False
        #                     final = True
        #                 else:
        #                     initial = False
        #                     final = False
        #                 existe = False
        #                 for a,b in matchIwithCpt:
        #                     if a == i:
        #                         existe = True
        #                 if existe:
        #                         srcDest.append(newListStates.index(b))
        #                 else:
        #                     srcDest.append(State(cpt, initial, final))
        #                     newListStates.append(srcDest[1])
        #                     matchIwithCpt.append((destIndex, cpt))
        #                     cpt += 1
        #             if srcDest != []:
        #                 newListTransitions.append(Transition(srcDest[0], lettre, srcDest[1]))
        #         except ValueError:
        #             continue
        # if auto.label == None:
        #     return Automate(newListTransitions, newListStates)
        # return Automate(newListTransitions, newListStates, label = "det("+auto.label+")")
        
    @staticmethod
    def complementaire(auto,alphabet):
        """ Automate -> Automate
        rend  l'automate acceptant pour langage le complémentaire du langage de a
        """
              
   
    @staticmethod
    def intersection (auto0, auto1):
        """ Automate x Automate -> Automate
        rend l'automate acceptant pour langage l'intersection des langages des deux automates
        """
        return

    @staticmethod
    def union (auto0, auto1):
        """ Automate x Automate -> Automate
        rend l'automate acceptant pour langage l'union des langages des deux automates
        """
        return
        

   
       

    @staticmethod
    def concatenation (auto1, auto2):
        """ Automate x Automate -> Automate
        rend l'automate acceptant pour langage la concaténation des langages des deux automates
        """
        return
        
       
    @staticmethod
    def etoile (auto):
        """ Automate  -> Automate
        rend l'automate acceptant pour langage l'étoile du langage de a
        """
        return




