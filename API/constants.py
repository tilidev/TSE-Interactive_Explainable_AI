from enum import Enum

class ExplanationMethod(str, Enum):
    lime = "lime"
    shap = "shap"
    dice_lvl3 = "dice_lvl3"

class AttributeNames(str, Enum):
    '''This class is used to have a central definition of how the attributes are referenced'''
    # attributes in the dataset
    balance = "balance"
    duration = "duration"
    history = "history"
    purpose = "purpose"
    amount = "amount"
    savings = "savings"
    employment = "employment"
    available_income = "available_income"
    #status_sex = "status_sex"
    residence = "residence"
    assets = "assets"
    age = "age"
    other_loans = "other_loans"
    housing = "housing"
    previous_loans = "previous_loans"
    job = "job"
    #telephone = "telephone"
    #foreign_worker = "foreign_worker"
    other_debtors = "other_debtors"
    people_liable = "people_liable"

    # meta-attributes
    ident = "id"
    NN_recommendation = "NN_recommendation"
    NN_confidence = "NN_confidence"


class ResponseStatus(str, Enum):
    accepted = "accepted"
    scheduled = "scheduled"
    running = "running"
    terminated = "terminated"
    timeout = "timeout"

# standard configuration for table view
standard_attributes = [
    AttributeNames.amount,
    AttributeNames.duration,
    AttributeNames.balance,
    AttributeNames.age,
    AttributeNames.employment,
    AttributeNames.NN_recommendation,
    AttributeNames.NN_confidence
]

# number definitions to re-use through the entire code
row_limit = 20

# strings to use throughout the entire code (important for coherence in response-key names)
attr_name = "attribute"
type = "type"
values = "values"
categorical = "categorical"
continuous = "continuous"
lower_bound = "lower_bound"
upper_bound = "upper_bound"
attr_description = "description"
influence = "influence"
positive_influence = "positive_influence"
category = "category"
financial_cat = "financial"
personal_cat = "personal"
loan_cat = "loan"
filter = "filter"
attributes = "attributes"
sort_by = "sort_by"
limit = "limit"
offset = "offset"
num_features = "num_features"
base_value = "base_value"
counterfactuals = "counterfactuals"
status = "status"
process_id = "process_id"
href = "href"
lime_result = "lime_result"
display_name = "display_name"
sort_ascending = "sort_ascending"