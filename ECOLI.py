
#%%
#import cometspy as c
import cobra
import cobra.io

#%%
(model, errors) = cobra.io.validate_sbml_model('/Users/patrickkampmeyer/Desktop/MODEL1507180060_url.xml')
# Replace with your model_id
#%%
for gene in model.genes:
    print("Gene ID:", gene.id)
    print("Name:", gene.name)
    print("Functional:", not gene.functional)
    print("Reactions:", [reaction.id for reaction in gene.reactions])
    print("-" * 20)


# %%


# Print some basic information about the model
print("Reactions:", len(model.reactions))
print("Metabolites:", len(model.metabolites))
print("Genes:", len(model.genes))

# List some of the reactions and metabolites
print(model.reactions[:10])  # print the first 10 reactions
print(model.metabolites[:10])  # print the first 10 metabolites



solution = model.optimize()
print("Growth rate:", solution.objective_value)




with model:
    model.reactions.get_by_id("DURIPP").lower_bound = -10.0  # simulate 10 mmol/gDW/hr glucose uptake
    print("Growth rate with 10 mmol/gDW/hr glucose:", model.optimize().objective_value)



with model:
    model.genes.b1723.knock_out()
    print("Growth rate with b1723 gene knockout:", model.optimize().objective_value)
