import synapseclient
from synapseutils import syncFromSynapse

syn = synapseclient.Synapse()
syn.login('bigbigorg','bigorg111x')

# Obtain a pointer and download the data
# syn18895959 = syn.get(entity='syn18895959', version=1 )

# Get the path to the local copy of the data file
# filepath = syn18895959.path
# print(filepath)

entities = syncFromSynapse(syn, "syn18895955")
# for f in entities:
#     print(f.path)