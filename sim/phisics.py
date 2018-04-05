# C Degree -> K
def celciusDegreeToKelvin(temperature):
    const0CelciusDegreeInKelvin = 273.15

    if temperature < -const0CelciusDegreeInKelvin:
        raise ValueError("Temperature under absolute 0")

    return temperature + const0CelciusDegreeInKelvin

# In [ J/(kg * K) ]
SpecificHeats = {
    'air': 1005,
}

# In [ W/(m*K) ] == [ J/(m*K*s) ]
MaterialHeatConductivity = {
    'reinforced concrete': 1.7,
    'brick': 0.8,
    'wood': 0.2,
}

# In [ J/(kg*K) ]
AirSpecificGasConstant = 287.056

# In [ Kg / m^3 ]
MaterialDensity = {
    'air': lambda temperature, pressure: pressure / (AirSpecificGasConstant * celciusDegreeToKelvin(temperature)),
}
