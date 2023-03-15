# Assign Preload to a Fastener
# This script is for a beam connection
# Applies a "Load" condition to the first step, and then will "Lock" the bolt for subsequent steps

BOLT_PREFIX = "TIEROD_ "
NO_BOLTS = 28
BOLT_TYPE = 19 # 0=geometry selection, 1=named selection, 19=beam connection, 21=pretension section
PRELOAD_MAGNITUDE = 5.8E6

# Load Steps
NO_STEPS = ExtAPI.DataModel.Project.Model.Analyses[0].AnalysisSettings.InternalObject.NumberOfSteps
DEFINE_BY = [BoltLoadDefineBy.Load]
for step in range(NO_STEPS):
    DEFINE_BY.append(BoltLoadDefineBy.Lock)

for n in range(NO_BOLTS):
    # Get tierod ID
    tierod = ExtAPI.DataModel.GetObjectsByName(BOLT_PREFIX+"{}".format(n+1))[0]
    tierodID = tierod.ObjectId
    # Add a new pretension load
    pretension = ExtAPI.DataModel.Project.Model.Analyses[0].AddBoltPretension()
    # Define pretension scoping method
    # 0=geometry selection, 1=named selection, 19=beam connection, 21=pretension section
    pretension.InternalObject.GeometryDefineBy = 19
    # Assign beam connection to preload
    pretension.InternalObject.BeamConnectionSelection = tierodID
    # Setup load steps
    for step, define in zip(steps, DEFINE_BY):
        pretension.SetDefineBy(step, define)
    # Apply pretension load
    pretension.InternalObject.Preload = PRELOAD_MAGNITUDE
