
from pydantic.errors import DurationError
from API.main import attribute_informations
from constants import AttributeNames
from constants import ResponseStatus

table_Response = [
   {
            AttributeNames.ident : 0,
            AttributeNames.amount : 1913.0,
            AttributeNames.duration : 18,
            AttributeNames.balance : "no balance",
            AttributeNames.age : 36,
            AttributeNames.employment : "less than 1 year",
            AttributeNames.NN_recommendation : False,
            AttributeNames.NN_confidence : 0.78
   },
      {
            AttributeNames.ident : 1,
            AttributeNames.amount : 1860.0,
            AttributeNames.duration : 12,
            AttributeNames.balance : "no balance",
            AttributeNames.age : 34,
            AttributeNames.employment : "unemployed",
            AttributeNames.NN_recommendation : False,
            AttributeNames.NN_confidence : 0.78
   },
      {
            AttributeNames.ident : 2,
            AttributeNames.amount : 1024.0,
            AttributeNames.duration : 24,
            AttributeNames.balance : "no account",
            AttributeNames.age : 48,
            AttributeNames.employment : "less than 1 year",
            AttributeNames.NN_recommendation : True,
            AttributeNames.NN_confidence : 0.78
   },
      {
            AttributeNames.ident : 3,
            AttributeNames.amount : 3104.0,
            AttributeNames.duration : 18,
            AttributeNames.balance : "no account",
            AttributeNames.age : 31,
            AttributeNames.employment : "between 1 and 4 years",
            AttributeNames.NN_recommendation : False,
            AttributeNames.NN_confidence : 0.78
   },
      {
            AttributeNames.ident : 4,
            AttributeNames.amount : 2520.0,
            AttributeNames.duration : 27,
            AttributeNames.balance : "no balance",
            AttributeNames.age : 23,
            AttributeNames.employment : "between 1 and 4 years",
            AttributeNames.NN_recommendation : True,
            AttributeNames.NN_confidence : 0.78
   },
      {
            AttributeNames.ident : 5,
            AttributeNames.amount : 882.0,
            AttributeNames.duration : 13,
            AttributeNames.balance : "no balance",
            AttributeNames.age : 23,
            AttributeNames.employment : "less than 1 year",
            AttributeNames.NN_recommendation : False,
            AttributeNames.NN_confidence : 0.78
   },
      {
            AttributeNames.ident : 6,
            AttributeNames.amount : 3612.0,
            AttributeNames.duration : 24,
            AttributeNames.balance : "no balance",
            AttributeNames.age : 37,
            AttributeNames.employment : "more than 7 years",
            AttributeNames.NN_recommendation : False,
            AttributeNames.NN_confidence : 0.78
   },
      {
            AttributeNames.ident : 7,
            AttributeNames.amount : 1352.0,
            AttributeNames.duration : 18,
            AttributeNames.balance : "no account",
            AttributeNames.age : 23,
            AttributeNames.employment : "unemployed",
            AttributeNames.NN_recommendation : False,
            AttributeNames.NN_confidence : 0.78
   },
      {
            AttributeNames.ident : 8,
            AttributeNames.amount : 6260.0,
            AttributeNames.duration : 16,
            AttributeNames.balance : "no balance",
            AttributeNames.age : 28,
            AttributeNames.employment : "between 1 and 4 years",
            AttributeNames.NN_recommendation : False,
            AttributeNames.NN_confidence : 0.78
   },
      {
            AttributeNames.ident : 9,
            AttributeNames.amount : 1322.0,
            AttributeNames.duration : 18,
            AttributeNames.balance : "no balance",
            AttributeNames.age : 40,
            AttributeNames.employment : "between 1 and 4 years",
            AttributeNames.NN_recommendation : False,
            AttributeNames.NN_confidence : 0.78
   },
      {
            AttributeNames.ident : 10,
            AttributeNames.amount : 2299.0,
            AttributeNames.duration : 11,
            AttributeNames.balance : "above 200 EUR",
            AttributeNames.age : 39,
            AttributeNames.employment : "more than 7 years",
            AttributeNames.NN_recommendation : False,
            AttributeNames.NN_confidence : 0.78
   },
      {
            AttributeNames.ident : 11,
            AttributeNames.amount : 4843.0,
            AttributeNames.duration : 36,
            AttributeNames.balance : "no account",
            AttributeNames.age : 43,
            AttributeNames.employment : "more than 7 years",
            AttributeNames.NN_recommendation : False,
            AttributeNames.NN_confidence : 0.78
   },
      {
            AttributeNames.ident : 12,
            AttributeNames.amount : 1544.0,
            AttributeNames.duration : 12,
            AttributeNames.balance : "above 200 EUR",
            AttributeNames.age : 42,
            AttributeNames.employment : "more than 7 years",
            AttributeNames.NN_recommendation : True,
            AttributeNames.NN_confidence : 0.78
   },
      {
            AttributeNames.ident : 13,
            AttributeNames.amount : 2570.0,
            AttributeNames.duration : 14,
            AttributeNames.balance : "above 200 EUR",
            AttributeNames.age : 21,
            AttributeNames.employment : "between 1 and 4 years",
            AttributeNames.NN_recommendation : False,
            AttributeNames.NN_confidence : 0.78
   },
      {
            AttributeNames.ident : 14,
            AttributeNames.amount : 2124.0,
            AttributeNames.duration : 27,
            AttributeNames.balance : "no account",
            AttributeNames.age : 24,
            AttributeNames.employment : "between 1 and 4 years",
            AttributeNames.NN_recommendation : True,
            AttributeNames.NN_confidence : 0.78
   },
      {
            AttributeNames.ident : 15,
            AttributeNames.amount : 3448.0,
            AttributeNames.duration : 18,
            AttributeNames.balance : "above 200 EUR",
            AttributeNames.age : 74,
            AttributeNames.employment : "between 1 and 4 years",
            AttributeNames.NN_recommendation : True,
            AttributeNames.NN_confidence : 0.78
   },
      {
            AttributeNames.ident : 16,
            AttributeNames.amount : 1175.0,
            AttributeNames.duration : 15,
            AttributeNames.balance : "above 200 EUR",
            AttributeNames.age : 68,
            AttributeNames.employment : "between 4  and 7 years",
            AttributeNames.NN_recommendation : False,
            AttributeNames.NN_confidence : 0.78
   },
      {
            AttributeNames.ident : 17,
            AttributeNames.amount : 1154.0,
            AttributeNames.duration : 16,
            AttributeNames.balance : "no account",
            AttributeNames.age : 57,
            AttributeNames.employment : "unemployed",
            AttributeNames.NN_recommendation : False,
            AttributeNames.NN_confidence : 0.78
   },
      {
            AttributeNames.ident : 18,
            AttributeNames.amount : 5954.0,
            AttributeNames.duration : 11,
            AttributeNames.balance : "above 200 EUR",
            AttributeNames.age : 38,
            AttributeNames.employment : "unemployed",
            AttributeNames.NN_recommendation : False,
            AttributeNames.NN_confidence : 0.78
   },
      {
            AttributeNames.ident : 19,
            AttributeNames.amount : 2279.0,
            AttributeNames.duration : 30,
            AttributeNames.balance : "no balance",
            AttributeNames.age : 37,
            AttributeNames.employment : "between 4  and 7 years",
            AttributeNames.NN_recommendation : False,
            AttributeNames.NN_confidence : 0.78
   }
]

instance_by_Id_Response = {

            AttributeNames.ident : 0,
            AttributeNames.amount : 1913.0,
            AttributeNames.duration : 18,
            AttributeNames.balance : "no balance",
            AttributeNames.age : 36,
            AttributeNames.employment : "less than 1 year",
            AttributeNames.history : "paid back all previous loans",
            AttributeNames.purpose : "retraining",
            AttributeNames.savings : "between 500 and 1000 EUR",
            AttributeNames.available_income : "between 20 and 25%",
            AttributeNames.residence : "between 4 and 7 years",
            AttributeNames.assets : "real estate",
            AttributeNames.other_loans : "at other banks",
            AttributeNames.housing : "own",
            AttributeNames.previous_loans : "1",
            AttributeNames.job : "skilled",
            AttributeNames.NN_recommendation : False,
            AttributeNames.NN_confidence : 0.78
}

attributes_information_Response = [
   { 
           AttributeNames.ident,
           0.0,
           999.0
   },
   {
           AttributeNames.amount,
           0.0,
           100000000.0
   },
   {
           AttributeNames.duration,
           0.0,
           100000000.0
   },
   {
           AttributeNames.balance,
           [{"no balance"}, {"no account"}, {"above 200 EUR"}, {"below 200 EUR"}]
   },
   {
           AttributeNames.age,
           14.0,
           100.0
   },
   {
           AttributeNames.employment,
           [{"unemployed"}, {"less than 1 year"}, {"between 1 and 4 years"}, {"between 4  and 7 years"}]
   },
      {
           AttributeNames.history,
           [{"paid back all previous loans"}, {"paid back previous loans at this bank"}, {"no problems with current loans"}, {"delay payment of previous loans"}, {"other loans exist at other banks"}]
   },
      {
           AttributeNames.purpose,
           [{"retraining"}, {"new car"}, {"furniture"}, {"used car"}, {"other"}, {"domestic appliances"}, {"vacation"}, {"business"}, {"television"}, {"repair"}]
   },
      {
           AttributeNames.savings,
           [{"no savings account at this bank"}, {"between 100 and 500 EUR"}, {"between 500 and 1000 EUR"}, {"above 1000 EUR"}]
   },
      {
           AttributeNames.available_income,
           [{"less than 20%"}, {"between 20 and 25%"}, {"between 25 and 35%"}, {"more than 35%"}]
   },
      {
           AttributeNames.residence,
           [{"less than 1 year"}, {"between 1 and 4 years"}, {"between 4 and 7 years"}, {"more than 7 years"}]
   },
      {
           AttributeNames.assets,
           [{"real estate"}, {"car"}, {"life insurance"}, {"none"}]
   },
      {
           AttributeNames.other_loans,
           [{"no additional loans"}, {"at other banks"}, {"at department store"}]
   },
      {
           AttributeNames.housing,
           [{"own"}, {"rent"}, {"for free"}]
   },
   {
           AttributeNames.previous_loans,
           [{"1"}, {"2 or 3"}, {"4 or more"}]
   },
   {
           AttributeNames.job,
           [{"skilled"}, {"executive or self-employed"}, {"unskilled (permanent resident)"}, {"unskilled (non-resident)"}]
   }
]



explanations_Response = {
            ResponseStatus.accepted,
            12,
            "http://127.0.0.1:8000/explantion-href"
}

explanations_Lime_Response = {

}

explanations_Shap_Response = {
    
}

explanations_Dice_Response = {
    
}

