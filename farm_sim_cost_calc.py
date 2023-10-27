import sys

# vars to store input parameters
inRefHP = 0      # reference engine HP
inAddMinFP = .00 # additional minor failure rate
inAddMajFP = .00 # additional major failure rate

# default parameters
defaultRefHP = 50     # reference engine horse power
defaultAddMinFP = .00 # additional minor failure probability
defaultAddMajFP = .00 # additional major failure probability

if len(sys.argv) != 4:
    print("incorrect number of input parameters, will use defaults")
    inRefHP = defaultRefHP
    inAddMinFP = defaultAddMinFP
    inAddMajFP = defaultAddMajFP
else:
    inRefHP = sys.argv[1]
    inAddMinFP = float(sys.argv[2]) / 100
    inAddMajFP = float(sys.argv[3]) / 100

print(f"*** '{sys.argv[0]}' program start ***")
print(f"Ruleset: 0.7-dev")
print(f"reference engine HP: {inRefHP}")
print(f"additional minor failure chance: {inAddMinFP * 100:.0f}%")
print(f"additional major failure chance: {inAddMajFP * 100:.0f}%")

# tractor price by manufacturing decade, reference 50hp tractor but price is for
# cheapest HP class price available for that period, 1950s-2000s by decade then
# every five years i.e. 2010/14, 2015/19
periodName = ["1950s", "1960s", "1970s", "1980s", "1990s", "2000s", "2010/14", "2015/19"]
pricesHP = [150, 200, 215, 235, 250, 350, 445, 480] # price per HP
refHP = inRefHP

# minor and major failure probabilities for manufacturing decades 1950s to 2000s
minFPs = [.14, .09, .08, .07, .06, .05, .04, .03]
majFPs = [.08, .06, .05, .04, .03, .02, .01, .01]

# additional failure rates (e.g. pore storage conditions etc.)
addMinFP = inAddMinFP
addMajFP = inAddMajFP

# fix price for failures as percentage of original price of equipment
minFixP = .05
majFixP = .15

# rought estimate of additional yearly cost due to failures
for i in range(len(pricesHP)):
    cumMinFPs = minFPs[i] + addMinFP
    cumMajFPs = majFPs[i] + addMajFP
    failRate = 1 - (1 * ((1 - (cumMinFPs + cumMajFPs)) **12))
    minProportion = 1 / (cumMinFPs + cumMajFPs) * cumMinFPs
    majProportion = 1 / (cumMinFPs + cumMajFPs) * cumMajFPs

    minFailRate = failRate * minProportion
    majFailRate = failRate * majProportion

    machinePrice = pricesHP[i] * float(refHP)
    minFixCost = machinePrice * minFixP
    majFixCost = machinePrice * majFixP
    minMaintCostYear = minFixCost * minFailRate
    majMaintCostYear = majFixCost * majFailRate
    
    print(f"\n{periodName[i]}")
    print(f"FR: {failRate*100:.2f}% minFR: {minFailRate*100:.2f}% majFR: {majFailRate*100:.2f}% minFix: {minFixCost} majFix: {majFixCost}")
    print(f"price machine: {machinePrice} maint_min: {minMaintCostYear:.0f} maint_maj: {majMaintCostYear:.0f} maint_tot: {minMaintCostYear + majMaintCostYear:.0f}")
