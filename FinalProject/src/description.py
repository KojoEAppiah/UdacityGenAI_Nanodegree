from lancedb.pydantic import LanceModel, vector

class Description(LanceModel):
    neighborhood_name: str
    price: int
    bedrooms: int
    bathrooms: float
    size: int
    description: str
    neighborhood_description: str
    vector: vector(1024)

    def to_string(self):
        field_strings = [
            str(key) for key in self.__dict__.keys() if str(key) != "vector"
        ]
        value_strings = [
            str(value) for value in self.__dict__.values() if type(value) is not vector
        ]
        zipped_strings = list(zip(field_strings, value_strings))
        combined_string = " , ".join(
            zipped_strings[x][0] + ": " + zipped_strings[x][1]
            for x in range(len(zipped_strings))
        )
        return combined_string