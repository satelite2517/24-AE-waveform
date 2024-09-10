from WF_SDK import device, scope, wavegen, tools, error   # import instruments

import matplotlib.pyplot as plt   # needed for plotting
from time import sleep            # needed for delays

"""-----------------------------------------------------------------------"""

# connect to the device
device_data = device.open(device = "Analog Discovery 2")

"""-----------------------------------"""

# handle devices without analog I/O channels

# initialize the scope with default settings
scope.open(device_data, sampling_frequency=10e4, amplitude_range=10)#, buffer_size=1024, sampling_frequency=100

# set up triggering on scope channel 1
scope.trigger(device_data, enable=True, source=scope.trigger_source.analog, channel=1, level=0)
scope.trigger(device_data, enable=True, source=scope.trigger_source.analog, channel=2, level=0)

# generate a 10KHz sine signal with 2V amplitude on channel 1
wavegen.generate(device_data, channel=1, function=wavegen.function.ramp_up, symmetry=100, offset=2, frequency=20, amplitude=2)

sleep(3)    # wait 1 second

# record data with the scopeon channel 1
buffer = scope.record(device_data, channel=1)
buffer_2 = scope.record(device_data, channel=2)

# generate buffer for time moments
time = []
for index in range(len(buffer)):
    time.append(index * 1e03 / scope.data.sampling_frequency)   # convert time to ms

# plot
plt.plot(time, buffer)
plt.xlabel("time [ms]")
plt.ylabel("voltage [V]")


plt.plot(time, buffer_2)
plt.xlabel("time [ms]")
plt.ylabel("voltage [V]")


plt.show()

# reset the scope
scope.close(device_data)

# reset the wavegen
wavegen.close(device_data)

device.close(device_data)