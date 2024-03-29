# C Degree -> K
def celciusDegreeToKelvin(temperature):
    const0CelciusDegreeInKelvin = 273.15

    if temperature < -const0CelciusDegreeInKelvin:
        raise ValueError("Temperature under absolute 0")

    return temperature + const0CelciusDegreeInKelvin


# C Degree -> K
def kelvinToCelciusDegree(temperature):
    const0CelciusDegreeInKelvin = 273.15

    if temperature < 0:
        raise ValueError("Temperature under absolute 0")

    return temperature - const0CelciusDegreeInKelvin


# F Degree -> K
def fahrenheitDegreeToCelcius(fahrenheit):
    const0CelciusDegreeInKelvin = 273.15
    temperature = (fahrenheit - 32) / 1.8

    if temperature < -const0CelciusDegreeInKelvin:
        raise ValueError("Temperature under absolute 0")

    return temperature


# In [ J/(kg * K) ]
SpecificHeats = {
    'air': 1005,
}

# In [ J/(kg*K) ]
AirSpecificGasConstant = 287.056

# In [ Kg / m^3 ]
MaterialDensity = {
    'air': lambda temperature, pressure: pressure / (AirSpecificGasConstant * celciusDegreeToKelvin(temperature)),
}
