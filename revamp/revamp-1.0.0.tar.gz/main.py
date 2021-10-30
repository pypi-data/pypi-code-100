# Import library
from tests.functions import DataPreperation

# Initiate object
transformation = DataPreperation()

# Call the object method
print(transformation.Transform(X=train, cleansing_step="all"))