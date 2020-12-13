# -*- coding: utf-8 -*-
from transition import *
from state import *
import os
import copy
from sp import *
from parser import *
from itertools import product
from automateBase import AutomateBase
from itertools import product 



class Automate(AutomateBase):
        
    def succElem(self, state, lettre):
        """State x str -> list[State]
        rend la liste des états accessibles à partir d'un état
        state par l'étiquette lettre
        """
        successeurs = []
        # t: Transitions
        for t in self.getListTransitionsFrom(state):
            if t.etiquette == lettre:
              successeurs.append(t.stateDest)
        return list(set(successeurs))


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
        # stateList : list[State]
        stateList = auto.getListInitialStates()
        for lettre in mot :
            stateList = auto.succ(stateList, lettre)
        for state in stateList:
            if state in auto.getListFinalStates():
              return True
        return False


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
        def isFinal(listState):
            """ list[State] -> bool
            Pour voir si l'etat comprenant listState est final
            """
            for state in listState:
                if state in auto.getListFinalStates():
                    return True
            return False
        # declaration des variables
        # currentList : list[State]
        currentList = auto.getListInitialStates()
        # stateList : list[list[[State]]]
        stateListList = []
        # newStateList : list[State]
        newStateList = []
        # dictListStateToState : dict{list[State] : State}
        dictListStateToState = dict()
        # nextList : list[State]
        nextList = []
        # alphabet
        alphabet = []
        # newTransitionList : list[transition]
        newTransitionList = []
        # preparation pour le premier etat
        stateListList.append(currentList)
        initialState = State(0, True, isFinal(currentList))
        # enregistrement pour la relation entre une liste d'etat et un etat correspondante
        dictListStateToState[frozenset(set(currentList))] = initialState
        newStateList.append(initialState)
        # recuperer toutes l'alphabet
        for transition in auto.listTransitions:
            alphabet.append(transition.etiquette)
        # Si on a des ajouts, on continue
        # Sinon, le nouvel automate est fait
        entrer = 0
        sortir = 1
        compte = 1
        while(entrer != sortir):
            entrer = sortir
            # iteration des lettre
            for lettre in alphabet:
                # iteration des etats existants
                for listOfStates in stateListList[:]:
                    currentList = listOfStates
                    nextList = []
                    # Si on n'est pas bloque
                    while(currentList != nextList):
                        nextList = auto.succ(currentList, lettre)
                        newTransition = Transition(dictListStateToState[frozenset(set(listOfStates))], lettre, dictListStateToState[frozenset(set(listOfStates))])
                        if currentList == nextList and  newTransition not in newTransitionList:
                            newTransitionList.append(newTransition)
                            sortir += 1
                        # ajout de nouvel etat et nouvelle transition s'ils n'existent pas
                        if nextList not in stateListList:
                            stateListList.append(nextList)
                            newState = State(compte ,False, isFinal(nextList))
                            compte += 1
                            sortir += 1
                            dictListStateToState[frozenset(set(nextList))] = newState
                            newStateList.append(newState)
                            newTransition = Transition(dictListStateToState[frozenset(set(listOfStates))], lettre, newState)
                            newTransitionList.append(newTransition)
                            # passe a la suivant
                            currentList = nextList
                        # S'ils existent, on etablit la transition et change la lettre 
                        else:
                            newTransition = Transition(dictListStateToState[frozenset(set(listOfStates))], lettre, dictListStateToState[frozenset(set(nextList))])
                            if newTransition not in newTransitionList:
                                newTransitionList.append(newTransition)
                            break
        return Automate(newTransitionList)
        
    @staticmethod
    def complementaire(auto, alphabet):
        """ Automate -> Automate
        rend  l'automate acceptant pour langage le complémentaire du langage de a
        """
        # on va creer un nouveau automate identique
        auto_new = copy.deepcopy(auto)
        # on va le determiniser si non determinise
        if not Automate.estDeterministe(auto_new):
            auto_new = Automate.determinisation(auto_new)
        # on va le completer si non complet
        if not Automate.estComplet(auto_new, alphabet):
            auto_new = Automate.completeAutomate(auto_new)
        # on change simplement les etats finaux
        newStateList = auto_new.listStates
        for index in range(len(newStateList)):
            newStateList[index].fin = not newStateList[index].fin
        return auto_new

    @staticmethod
    def test(auto):
        """This is a test module written par Junji / Fanxiang
        There is no need to copy this signature mdr"""
        return auto

    @staticmethod
    def intersectionIsFinal(stateTuple, auto0, auto1):
            """ (State,State) -> bool
            Pour voir si l'etat est final pour l'intersection
            """
            (state0,state1) = stateTuple
            if state0 not in auto0.getListFinalStates():
                return False
            if state1 not in auto1.getListFinalStates():
                return False
            return True

    @staticmethod
    def unionIsFinal(stateTuple, auto0, auto1):
            """ (State,State) -> bool
            Pour voir si l'etat est final pour l'union
            """
            (state0,state1) = stateTuple
            if state0 in auto0.getListFinalStates():
                return True
            if state1 in auto1.getListFinalStates():
                return True 
            return False

    @staticmethod
    def produitCartesien (auto0, auto1, isFinal):
        """ Automate x Automate x Fonction -> Automate
        rend l'automate acceptant pour langage l'intersection ou l'union des langages des deux automates suivant la fonction passe
        """
        def getNextTupleList(stateTuple, lettre):
            """(State,State)*str -> list[(State,State)]
            obtenir un tuple d'etats a partir d'un autre
            """
            (state0, state1) = stateTuple
            nextStateList0 = auto0.succElem(state0, lettre)
            if nextStateList0 == []:
                return []
            nextStateList1 = auto1.succElem(state1, lettre)
            if nextStateList1 == []:
                return []
            return product(nextStateList0, nextStateList1)
        # declaration des variables
        compte = 0
        initialStateTuples = product(auto0.getListInitialStates(), auto1.getListInitialStates())
        setStateTuples = set()
        dictStateTupleToState = dict()
        newTransitionList = []
        newStateList = []
        # etats initiaux
        for stateTuple in initialStateTuples:
            setStateTuples.add(stateTuple)
            dictStateTupleToState[stateTuple] = State(compte, True, isFinal(stateTuple,auto0, auto1))
            newStateList.append(dictStateTupleToState[stateTuple])
            compte += 1
        # # recuperer toutes l'alphabet
        alphabet = list(set(auto0.getAlphabetFromTransitions()) & set(auto1.getAlphabetFromTransitions()))
        # Si on a des ajouts, on continue
        # Sinon, le nouvel automate est fait
        entrer = 0
        sortir = 1
        while(entrer != sortir):
            entrer = sortir
            # iteration des lettre
            for lettre in alphabet:
                # iteration des etats existants
                for aStateTuple in copy.deepcopy(setStateTuples):
                    nextTupleList = getNextTupleList(aStateTuple, lettre)
                    if nextTupleList == []:
                        continue
                    for aNewTuple in nextTupleList:
                        if aNewTuple not in setStateTuples:
                            setStateTuples.add(aNewTuple)
                            newState = State(compte, False, isFinal(aNewTuple, auto0, auto1))
                            newStateList.append(newState)
                            dictStateTupleToState[aNewTuple] = newState
                            compte += 1
                            sortir += 1
                        nextTransition = Transition(dictStateTupleToState[aStateTuple], lettre, dictStateTupleToState[aNewTuple])
                        if nextTransition not in newTransitionList:
                            newTransitionList.append(nextTransition)
                            sortir += 1
        return Automate(newTransitionList)
    
    @staticmethod
    def intersection (auto0, auto1):
        return Automate.produitCartesien(auto0, auto1, Automate.intersectionIsFinal)

    @staticmethod
    def union (auto0, auto1):
        """ Automate x Automate -> Automate
        rend l'automate acceptant pour langage l'union des langages des deux automates
        """
        return Automate.produitCartesien(auto0, auto1, Automate.unionIsFinal)
        

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
        new_auto = copy.deepcopy(auto)
        # prend les Transition dont stateDest sont finaux
        # ajout des Transition vers l'etat initial a partir de stateSrc de ces Transition
        return new_auto




