#include <math.h>

float calculate_temperature(float R)
{
    float inv_coef[4] = {3.34e-3, 2.57e-4, 2.62e-6, 6.38e-8};
    float roll = 0;
    float R_ref = 9500; // resistance at 25 degrees kelvin
    float x;

    x = log(R/R_ref);
    
    for(int i=0; i<4; i++){
        roll += inv_coef[i] * pow(x, i);
    }
    return (1.0 / roll) - 273.15;
}
