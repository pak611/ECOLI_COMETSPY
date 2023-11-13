

import cobra
import pandas as pd

# Load the E. coli metabolic model
model = cobra.io.read_sbml_model('ecoli_model.xml')

# Load the transcriptomic data from a CSV file
# Assuming the CSV has two columns: 'gene_id' and 'expression'
transcriptomic_data = pd.read_csv('transcriptomic_data.csv', index_col='gene_id')

# Map the expression data onto the model genes
for gene in model.genes:
    if gene.id in transcriptomic_data.index:
        expression = transcriptomic_data.loc[gene.id, 'expression']
        # Here you might transform the expression into something that can be used
        # directly in the model, e.g., applying log transformation if necessary
        # For this example, we will just assign the expression value to the gene
        gene.expression = expression
    else:
        gene.expression = 0.0  # Assign a default low expression for missing genes

# An example function to update reaction bounds based on gene expression
def update_reaction_bounds_from_expression(model, threshold=50):
    for reaction in model.reactions:
        if reaction.gene_reaction_rule:
            # Get the maximum expression level of genes associated with this reaction
            max_expression = max(gene.expression for gene in reaction.genes)
            # If the maximum expression is below a threshold, set the reaction bounds to zero
            if max_expression < threshold:
                reaction.bounds = (0, 0)

# Update the model reaction bounds based on the gene expression
update_reaction_bounds_from_expression(model)

# Perform Flux Balance Analysis (FBA) on the updated model
solution = model.optimize()

# Print the objective value (e.g., growth rate)
print('Growth rate:', solution.objective_value)

# Print the fluxes of some reactions of interest
for reaction_id in ['ACALD', 'PGK', 'GLCpts']:
    reaction = model.reactions.get_by_id(reaction_id)
    print(f'{reaction.id}: {reaction.flux}')
