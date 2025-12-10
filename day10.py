if __name__ == "__main__":
    import numpy as np
    from itertools import combinations
    from scipy.optimize import milp, LinearConstraint, Bounds

    light_diagrams = []
    wiring_schematics = []
    joltage_requirements = []
    with open("inputs/day10.txt") as f:
        for line in f:
            line = line.replace("[", "").replace("]", "").replace("{", "").replace("}", "")
            parts = line.strip().split(" ")
            light_diagrams.append([0 if c == '.' else 1 for c in parts[0]])
            joltage = tuple(int(x) for x in parts[-1].split(","))
            joltage_requirements.append(joltage)
            
            wiring = []
            for wire in parts[1:-1]:
                wire = wire.replace("(", "").replace(")", "")
                nums = tuple(int(x) for x in wire.split(","))
                wiring.append(nums)
            wiring_schematics.append(wiring)
    
    # Part 1: Fewest button presses to configure the indicator lights
    total_presses = 0
    for i, (target, buttons) in enumerate(zip(light_diagrams, wiring_schematics)):
        target = np.array(target, dtype=int)
        min_presses = -1
        found = False

        for n_presses in range(len(buttons) + 1):
            if found:
                break
            for combo in combinations(range(len(buttons)), n_presses):
                state = np.zeros(len(target), dtype=int)
                for button_idx in combo:
                    for light_idx in buttons[button_idx]:
                        state[light_idx] = (state[light_idx] + 1) % 2
                
                if np.array_equal(state, target):
                    min_presses = n_presses
                    found = True
                    break
        
        total_presses += min_presses
    
    print(f"Total button presses for indicator lights: {total_presses}")
    
    # Part 2: Fewest button presses to configure the joltage level counters
    total_presses_2 = 0
    for i, (target, buttons) in enumerate(zip(joltage_requirements, wiring_schematics)):
        Aa = np.zeros((len(target), len(buttons)), dtype=float)
        for j, button in enumerate(buttons):
            for counter_idx in button:
                Aa[counter_idx][j] = 1
        
        b = np.array(target, dtype=float)
        c = np.ones(len(buttons))
        constraints = LinearConstraint(Aa, lb=b, ub=b)
        bounds = Bounds(lb=0, ub=np.inf)
        integrality = np.ones(len(buttons), dtype=int)
        result = milp(c=c, constraints=constraints, bounds=bounds, integrality=integrality)
        
        total_presses_2 += int(np.sum(result.x))
    
    print(f"Total button presses for joltage level counters: {total_presses_2}")