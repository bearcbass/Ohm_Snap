import numpy as np

def three_band_solution(data):
    ohms = (10 * data[0] + data[1]) * (10**data[2])
    return ohms

# Keep in mind the plus or minus in the end, little confusing
def four_band_solution(data):
    ohms = (10 * data[0] + data[1]) * (10**data[2])
    resistance = data[3] * 100
    return ohms, resistance

# Keep in mind the plus or minus in the end, little confusing
def five_band_solution(data):
    ohms = (100 * data[0] + 10 * data[1] + data[2]) * (10**data[3]) 
    resistance = data[4] * 100
    return ohms, resistance

if __name__ == '__main__':
  
    # Need to set up a way in which data is recieved
    # My idea is that we just export a file called sol.dat
    # Let us assume we get one resistor at a time
    data_array = np.loadtxt("/Users/bearcbass/Ohm_Snap/sol.dat")
    print(data_array)

    """
    This color coordination gets a bit confusing.
    The first band can never be black since, we will
    be multiplying by 0 resistance. 
    Next, each color is associated with a value, 
    lets just stick to three bands for now
    
    Black = 0, brown = 1, red = 2, orange = 3, yellow = 4,
    Green = 5, blue = 6, violet = 7, grey = 8, white = 9

    Let us assume that each row in the matrix is already masked with the proper values.

    The next step is just caluclating. 

    DO NOT FORGET: -1 is a magic value, it indicates that there is no 4-6th band
    The reason for this data being kept is that we may have multiple resistors 
    with varying bands

    Cool lets get to coding. 

    """

    # Edge Case
    if len(data_array) > 5 or len(data_array) < 2:
        print("ERROR: Invalid amount of bands")

    # Lets calculate based on number of bands
    if len(data_array) == 3:
        ohms = three_band_solution(data_array)
    elif len(data_array) == 4:
        ohms, resistance = four_band_solution(data_array)
    elif len(data_array) == 5:
        ohms, resistance = five_band_solution(data_array)
    else:
        print("Invalid number of bands")

    if 'resistance' in locals():
        print("We have ohms, ", ohms , "with resistance ± ", int(resistance),"%")
    else:
        print("We have ohms, ", ohms)

    print(ohms)