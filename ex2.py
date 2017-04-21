# Running times:
# 1 process - 20.46 sec
# 2 processes - 17.43 sec
# 4 processes - 17.08 sec
# 8 processes - 20.90 sec
# 16 processor - 30.875 sec
# As I have 2 cores with hyperthreding - we achive minimun at 4 process 
# And above 4 - the overhead of running more process is too costly for this problem

from matplotlib import pyplot
import multiprocessing
import time

def init_process(y_to_share, new_y_to_share):
	global y, new_y
	y = y_to_share
	new_y = new_y_to_share

start = time.time()

BUFFER_SIZE = 1000

# initial conditions
num_processes = 16 # either 1,2,4,8 or 16
y = multiprocessing.Array('d', BUFFER_SIZE, lock=False)
y[:] = [0] * BUFFER_SIZE
y[480:520] = [1] * 40

new_y = multiprocessing.Array('d', BUFFER_SIZE, lock=False)
new_y[:] = [0] * BUFFER_SIZE
new_y[480:520] = [1] * 40

dt = 0.01

# chunk range to equal parts
def chunk(seq, num):
  avg = len(seq) / float(num)
  out = []
  last = 0.0

  while last < len(seq):
    out.append(seq[int(last):int(last + avg)])
    last += avg

  return out

# our rule for reaction-diffusion
def advance(chunk): # work of part of Y
	n = len(y)
	for j in chunk:
		new_y[j] += dt * (20 * (y[j - 1] - 2 * y[j] + y[(j + 1) % n])
						   - y[j] * (1 - y[j]) * (0.3 - y[j]))

if __name__ == '__main__': 
	multiprocessing.freeze_support()
	p = multiprocessing.Pool(num_processes, 
                         initializer=init_process,
						 initargs=(y, new_y))

	# advance through t (t = i * dt) is at least 100; plot
	# every 20
	i = 0
	chunks = chunk(range(BUFFER_SIZE), num_processes)
	while i * dt <= 100:
		if i * dt % 20 == 0:
			pyplot.plot(y, label='t = %g' % (i * dt))
		p.map(advance,chunks)
		i += 1
		y[:] = new_y
		print i * dt

	end = time.time()
	print 'simulation time:', end - start

	pyplot.legend()
	pyplot.show()