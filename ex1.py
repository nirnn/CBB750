import matplotlib.pyplot as plt
import numpy as np

# the maximum theoretical speedup possible on a machine with infinite processors
# is 1/(1-p)

def sdpeedup(p):
	n = np.array(range(1, 16834))
	s = 1 / ((1 - p) + (p/n))
	plt.semilogx(s) # using semilox x axes
	
if __name__ == '__main__':
	sdpeedup(0.5)
	sdpeedup(0.67)
	sdpeedup(0.95)
	sdpeedup(0.99)

	plt.ylabel('Maximum Speedup')
	plt.xlabel('Number of processors')
	plt.legend()
	plt.show()