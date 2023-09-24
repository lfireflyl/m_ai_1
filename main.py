import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
 
location = ctrl.Antecedent(np.arange(0, 200, 1), 'location')
condition = ctrl.Antecedent(np.arange(0, 100, 1), 'condition')
price = ctrl.Consequent(np.arange(20, 250, 1), 'price')  #в тысячах


# используем стандартную функцию принадлежности (треугольник)
price.automf(names=['low', 'medium', 'high'])

condition['bad'] = fuzz.trapmf(condition.universe, [0, 10, 25, 40])
condition['medium'] = fuzz.trapmf(condition.universe, [30, 40, 55, 70])
condition['good'] = fuzz.trapmf(condition.universe, [60, 70, 100, 100])

location['bad'] = fuzz.trapmf(location.universe, [25, 100, 200, 200])
location['averege'] = fuzz.trapmf(location.universe,[10, 15, 30, 45])
location['good'] = fuzz.trapmf(location.universe,[0, 5, 10, 15])
#построение графиков
condition.view()
location.view()
price.view()

# база правил
rule1 = ctrl.Rule(condition['bad'] & location['bad'], price['low'])
rule2 = ctrl.Rule(condition['bad'] & location['averege'], price['low'])
rule3 = ctrl.Rule(condition['bad'] & location['good'], price['medium'])
rule4 = ctrl.Rule(condition['medium'] & location['bad'], price['low'])
rule5 = ctrl.Rule(condition['medium'] & location['averege'], price['medium'])
rule6 = ctrl.Rule(condition['medium'] & location['good'], price['high'])
rule7 = ctrl.Rule(condition['good'] & location['bad'], price['medium'])
rule8 = ctrl.Rule(condition['good'] & location['averege'], price['medium'])
rule9 = ctrl.Rule(condition['good'] & location['good'], price['high'])
price_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
price_simulator= ctrl.ControlSystemSimulation(price_ctrl)

#
price_simulator.input['condition'] = 71
price_simulator.input['location'] = 20

#результат
price_simulator.compute()
print(price_simulator.output['price'])
condition.view(sim=price_simulator)
location.view(sim=price_simulator)
price.view(sim=price_simulator)
input()