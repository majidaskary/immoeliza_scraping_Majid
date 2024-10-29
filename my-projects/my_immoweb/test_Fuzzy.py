
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------- input
# Define the input prompts for the user
def get_kitchen_type():
    print("\nSelect Kitchen Type:")
    print("1. Not Installed")
    print("2. Semi Installed")
    print("3. Installed")
    print("4. Hyper Installed")
    choice = int(input("Enter the number corresponding to the kitchen type: "))
    if choice == 1:
        return 1
    elif choice == 2:
        return 5
    elif choice == 3:
        return 8
    elif choice == 4:
        return 10
    else:
        print("Invalid choice. Defaulting to 'Installed'.")
        return 8

def get_kitchen_size():
    print("\nSelect Kitchen Size:")
    print("1. Small   (5-7 m²)")
    print("2. Medium (7-10 m²)")
    print("3. Large (10-12 m²)")
    choice = int(input("Enter the number corresponding to the kitchen size: "))
    if choice == 1:
        return 6
    elif choice == 2:
        return 8
    elif choice == 3:
        return 12
    else:
        print("Invalid choice. Defaulting to 'Medium'.")
        return 8

def get_country():
    print("\nSelect Country:")
    print("1. China")
    print("2. Belgium")
    print("3. USA")
    choice = int(input("Enter the number corresponding to the country: "))
    if choice == 1:
        return 1
    elif choice == 2:
        return 3
    elif choice == 3:
        return 5
    else:
        print("Invalid choice. Defaulting to 'Belgium'.")
        return 3

# ---------------------------------------------------------------------- Fyzzy

# Define lists for kitchen type, size, country, and cost
kitchen_types_list = [
    [0, 0, 2, 'not_installed'], 
    [2, 4, 6, 'semi_installed'], 
    [6, 8, 10, 'installed'], 
    [9, 10, 10, 'hyper_installed']
]

kitchen_sizes_list = [
    [5, 5, 7, 'small'], 
    [7, 8, 10, 'medium'], 
    [10, 12, 12, 'large']
]

countries_list = [
    [0, 0, 2, 'china'], 
    [2, 3, 4, 'belgium'], 
    [4, 5, 5, 'usa']
]

cost_categories_list = [
    [0, 0, 3000, 'low'], 
    [3000, 5000, 7000, 'medium'], 
    [7000, 10000, 10000, 'high']
]

# ----------------------------------------------------------------------
# Create input variables for the fuzzy system
kitchen_type = ctrl.Antecedent(np.arange(0, 11, 1), 'kitchen_type')
kitchen_size = ctrl.Antecedent(np.arange(5, 13, 1), 'kitchen_size')
country = ctrl.Antecedent(np.arange(0, 6, 1), 'country')

# Create output variable for the fuzzy system (cost)
cost = ctrl.Consequent(np.arange(0, 10001, 500), 'cost')

# ----------------------------------------------------------------------
# Create dynamic Membership Functions from the defined lists
for kt in kitchen_types_list:
    kitchen_type[kt[3]] = fuzz.trimf(kitchen_type.universe, [kt[0], kt[1], kt[2]])

for ks in kitchen_sizes_list:
    kitchen_size[ks[3]] = fuzz.trimf(kitchen_size.universe, [ks[0], ks[1], ks[2]])

for c in countries_list:
    country[c[3]] = fuzz.trimf(country.universe, [c[0], c[1], c[2]])

for cc in cost_categories_list:
    cost[cc[3]] = fuzz.trimf(cost.universe, [cc[0], cc[1], cc[2]])

# ----------------------------------------------------------------------
# Define rules
rule1 = ctrl.Rule(kitchen_type['not_installed'] & kitchen_size['small'] & country['china'], cost['low'])
rule2 = ctrl.Rule(kitchen_type['installed'] & kitchen_size['large'] & (country['usa'] | country['belgium']), cost['high'])
rule3 = ctrl.Rule(kitchen_type['hyper_installed'] & kitchen_size['large'] & country['usa'], cost['high'])
rule_catch_all = ctrl.Rule(kitchen_type['installed'], cost['medium'])

# ----------------------------------------------------------------------
# Create fuzzy control system and simulation
cost_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule_catch_all])
cost_simulation = ctrl.ControlSystemSimulation(cost_ctrl)

# ----------------------------------------------------------------------
kitchen_type_input = get_kitchen_type()     # input kitchen type     
kitchen_size_input = get_kitchen_size()     # input kitchen size
country_input = get_country()               # input country

# Default values for inputs (for testing without user input)
# You can modify these values to test different combinations
# kitchen_type_input = 8  # Installed kitchen     
# kitchen_size_input = 12  # Large kitchen
# country_input = 5  # USA

cost_simulation.input['kitchen_type'] = kitchen_type_input
cost_simulation.input['kitchen_size'] = kitchen_size_input
cost_simulation.input['country'] = country_input

# Compute the fuzzy system output
cost_simulation.compute()

# ---------------------------------------------------------------------- print
# Function to print Membership Values for each input
def print_membership_values(variable, label, value):
    print(f"\nMembership values for {label} = {value}:")
    for term in variable.terms:
        membership_value = fuzz.interp_membership(variable.universe, variable[term].mf, value)
        print(f"  {term}: {membership_value:.2f}")

# ----------------------------------------------------------------------
# Get user inputs and simulate with default values
kitchen_type_input = 8  # Installed kitchen
kitchen_size_input = 12  # Large kitchen
country_input = 5  # USA

cost_simulation.input['kitchen_type'] = kitchen_type_input
cost_simulation.input['kitchen_size'] = kitchen_size_input
cost_simulation.input['country'] = country_input

# Print Membership Values for inputs
print_membership_values(kitchen_type, 'kitchen_type', kitchen_type_input)
print_membership_values(kitchen_size, 'kitchen_size', kitchen_size_input)
print_membership_values(country, 'country', country_input)

# ----------------------------------------------------------------------
# Compute the fuzzy system output
cost_simulation.compute()

# ----------------------------------------------------------------------
# Print the estimated cost
if 'cost' in cost_simulation.output:
    print(f"\nEstimated Kitchen Renovation Cost: €{cost_simulation.output['cost']:.2f}")
else:
    print("No cost output generated. Check the rules or input values.")

# ----------------------------------------------------------------------   chart 
# Plot Membership Functions for each input and output
fig, axs = plt.subplots(2, 2, figsize=(10, 8))

# Plot for Kitchen Type
for kt in kitchen_types_list:
    axs[0, 0].plot(kitchen_type.universe, kitchen_type[kt[3]].mf, label=kt[3].replace('_', ' ').capitalize())
axs[0, 0].set_title('Kitchen Type')
axs[0, 0].legend()

# Plot for Kitchen Size
for ks in kitchen_sizes_list:
    axs[0, 1].plot(kitchen_size.universe, kitchen_size[ks[3]].mf, label=ks[3].capitalize())
axs[0, 1].set_title('Kitchen Size')
axs[0, 1].legend()

# Plot for Country
for c in countries_list:
    axs[1, 0].plot(country.universe, country[c[3]].mf, label=c[3].capitalize())
axs[1, 0].set_title('Country')
axs[1, 0].legend()

# Plot for Cost
for cc in cost_categories_list:
    axs[1, 1].plot(cost.universe, cost[cc[3]].mf, label=cc[3].capitalize())
axs[1, 1].set_title('Cost')
axs[1, 1].legend()

# Adjust layout for charts
plt.tight_layout()
plt.show()
# ----------------------------------------------------------------------
