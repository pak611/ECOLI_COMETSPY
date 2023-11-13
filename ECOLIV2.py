import cobra
import cobra.io

# Define a function to print the model information
def print_model_info(model, logfile_path):
    with open(logfile_path, 'w') as logfile:
        # Function to print within the with statement context
        def print_to_log(*args, **kwargs):
            print(*args, file=logfile, **kwargs)
        
        # Log model validation errors if there are any
        if errors:
            print_to_log("Model validation errors:")
            for error in errors:
                print_to_log(error)
            print_to_log("-" * 40)

        # Print gene information
        for gene in model.genes:
            print_to_log("Gene ID:", gene.id)
            print_to_log("Name:", gene.name)
            print_to_log("Functional:", not gene.functional)
            print_to_log("Reactions:", [reaction.id for reaction in gene.reactions])
            print_to_log("-" * 20)

        # Print basic information about the model
        print_to_log("Reactions:", len(model.reactions))
        print_to_log("Metabolites:", len(model.metabolites))
        print_to_log("Genes:", len(model.genes))

        # List some of the reactions and metabolites
        print_to_log("First 10 reactions:", model.reactions[:10])  # print the first 10 reactions
        print_to_log("First 10 metabolites:", model.metabolites[:10])  # print the first 10 metabolites

        # Perform Flux Balance Analysis (FBA)
        solution = model.optimize()
        print_to_log("Growth rate:", solution.objective_value)

# Load and validate the model
model_path = '/Users/patrickkampmeyer/Desktop/MODEL1507180060_url.xml'
(model, errors) = cobra.io.validate_sbml_model(model_path)

# Define the path for the logfile
logfile_path = '/Users/patrickkampmeyer/Desktop/model_info_log.txt'

# Call the function with the model and the path to the logfile
print_model_info(model, logfile_path)
