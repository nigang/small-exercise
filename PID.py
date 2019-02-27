import numpy as np
import matplotlib.pyplot as plt

Vin = 100
Vout = 5
I = 0.5
P = 0.1
D = 0.07

Error = Vin - Vout
PID_Vconv = []
Iteration_counter = []
PID_Vconv.append(Vout)
Iteration_counter.append(0)
error_sum = 0;
error_vec = []
error_vec.append(Vin - Vout)
for itor in np.arange(30):
    error = Vin - PID_Vconv[itor]
    error_sum += error
    error_vec.append(error)
    d_error = error_vec[itor+1] - error_vec[itor]
    PID_Vconv.append(I*error_sum + P*error + D*d_error)
    Iteration_counter.append(itor + 1)
    
plt.plot(Iteration_counter, PID_Vconv, color='r')
plt.plot(Iteration_counter, error_vec, color='g')
    
    