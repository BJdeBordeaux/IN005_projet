def concatenation (auto1, auto2):
    """ Automate x Automate -> Automate
    rend l'automate acceptant pour langage la concaténation des langages des deux automates
    """
    def addIdNumber(auto):
        max = 0
        for state in auto_new1.listStates:
        if max < state.id:
            max = state.id
        return max
    auto_new1 = copy.deepcopy(auto1)
    IdNumberToAdd = addIdNumber(auto_new1)
    auto_new2 = copy.deepcopy(auto2)
    listTransitionsAModifier = []
    for state in auto_new2.listStates:
        state.id += max
    for transition in new_auto1.listTransitions:
        if transition.stateDest.fin == True:
            listTransitionsAModifier.append(transition)
    for state in new_auto1.listStates:
        if state.fin == True:
            state.fin = False
    for transition in listTransitionsAModifier:
        for initialState in auto_new2.getListInitialStates():
            new_auto1.addTransition(Transition(transition.stateSrc, transition.etiquette, initialState))
    for state in new_auto2.listStates:
        if state.init == True:
            state.init = False
    for transition in new_auto2.listTransitions:
        auto_new1.addTransition(Transition(transition.stateSrc, transition.etiquette, transition.stateDest))
    return auto_new1