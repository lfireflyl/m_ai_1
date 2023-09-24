import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


bms = ctrl.Antecedent(np.arange(5, 35, 1), 'body mass index')
dki = ctrl.Antecedent(np.arange(1, 5, 0.1), 'daily calorie intake') #kcl
ti = ctrl.Consequent(np.arange(20, 250, 1), 'training intensity') #min activity per day
 


# используем стандартную функцию принадлежности (треугольник)
ti.automf(names=['low', 'medium', 'high'])

bms['flaw'] = fuzz.trapmf(bms.universe, [5, 10, 15, 18])
bms['norm'] = fuzz.trapmf(bms.universe, [15, 20, 25, 30])
bms['excess'] = fuzz.trapmf(bms.universe, [27, 30, 100, 100])

dki['low'] = fuzz.trapmf(dki.universe, [1, 1.4, 1.7, 1.85])
dki['norm'] = fuzz.trapmf(dki.universe,[1.7, 2.15, 3.8, 4.1])
dki['excess'] = fuzz.trapmf(dki.universe,[3.9, 4.2, 5, 5])
#построение графиков
bms.view()
dki.view()
ti.view()

# база правил
rule1 = ctrl.Rule(bms['flaw'] & dki['low'], ti['low'])
rule2 = ctrl.Rule(bms['flaw'] & dki['norm'], ti['low'])
rule3 = ctrl.Rule(bms['flaw'] & dki['excess'], ti['medium'])
rule4 = ctrl.Rule(bms['norm'] & dki['low'], ti['low'])
rule5 = ctrl.Rule(bms['norm'] & dki['norm'], ti['medium'])
rule6 = ctrl.Rule(bms['norm'] & dki['excess'], ti['high'])
rule7 = ctrl.Rule(bms['excess'] & dki['low'], ti['medium'])
rule8 = ctrl.Rule(bms['excess'] & dki['norm'], ti['high'])
rule9 = ctrl.Rule(bms['excess'] & dki['excess'], ti['high'])
ti_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
ti_simulator= ctrl.ControlSystemSimulation(ti_ctrl)

ti_simulator.input['body mass index'] = 22
ti_simulator.input['daily calorie intake'] = 2.2

ti_simulator.compute()
print(ti_simulator.output["training intensity"])
bms.view(sim=ti_simulator)
dki.view(sim=ti_simulator)
ti.view(sim=ti_simulator)

# #результат
# price_simulator.compute()
# print(price_simulator.output['price'])
# condition.view(sim=price_simulator)
# location.view(sim=price_simulator)
# price.view(sim=price_simulator)
input()