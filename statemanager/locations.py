from enum import Enum

class Locations(Enum):
    Unknown = 0
    Cooperate = 1
    Center = 2
    Defect = 3


    @staticmethod
    def map_enum_to_location(input_enum):
        if input_enum == Locations.Cooperate:
            return [1, 0, 0]
        elif input_enum == Locations.Center:
            return [0, 1, 0]
        elif input_enum == Locations.Defect:
            return [0, 0, 1]
        else:
            return [0, 0, 0]  # Represents Locations.Unknown
    def map_num_to_location(input_enum):
        if input_enum == 0:
            return [1, 0, 0]
        elif input_enum == 1:
            return [0, 1, 0]
        elif input_enum == 2:
            return [0, 0, 1]
        else:
            return [0, 0, 0]  # Represents Locations.Unknown

# Example usage
# location = Locations.Cooperate.map_to_location()
