import os
import numpy as np
import matplotlib.pyplot as plt
from connections import connections

# Clear the terminal screen
os.system('clear' if os.name == 'posix' else 'cls')

#Input data
N = 20                        # number of nodes in the horizontal direction
M = 20                        # number of nodes in the vertical direction
xi = 1                        # initial point of lattice - x
yi = 1                        # initial point of lattice - y
xe = 2                        # end point of lattice - x
ye = 2                        # end point of lattice - y
t2 = 70                       # final time
dt = 0.05                     # time increments
a0 = 0                        # initial acceleration
v0 = 0                        # initial velocity
m = 1                         # mass of each node
threshold_length = 0.022       # ultimate strech of each spring
K=400                       #Spring Stiffness matrix constant

# External forces
external_force_bottom = np.array([0, 0])
external_force_right = np.array([0.35, 0])
external_force_top = np.array([0, 0])
external_force_left = np.array([-0.35, 0])

# Lattice construction section
xcoord = np.linspace(xi, xe, N)
ycoord = np.linspace(yi, ye, M)
x, y = np.meshgrid(xcoord, ycoord)
x = x.flatten()
y = y.flatten()

# if you need to add randomness to the coordinate distribution
random_offset = 0.002
x += random_offset * np.random.randn(N * M)
y += random_offset * np.random.randn(N * M)

# Construct lattice connections (springs)
pos = np.vstack((x, y)).T
cx, cy = connections(N, M)

# Calculate spring initial length
L = np.sqrt((pos[cx, 0] - pos[cy, 0])**2 + (pos[cx, 1] - pos[cy, 1])**2)

#Calculate spring stiffness
k = np.zeros_like(cx)
k[:]=K*L[:]

# Introduce a defect by weakening a specific spring (spring index = 10)
defect_spring_index1 = 2
k[defect_spring_index1] = 0
defect_spring_index2 = 21
k[defect_spring_index2] = 0
defect_spring_index3 = 762
k[defect_spring_index3] = 0
defect_spring_index4 = 1123
k[defect_spring_index4] = 0
fig = plt.figure(figsize=(4,4), dpi=80)
plt.plot(pos[:, 0], pos[:, 1], marker='.', color='k', linestyle='none')  # Plot nodes
plt.plot(pos[[cx, cy], 0], pos[[cx, cy], 1], color='blue')  # Plot spring connections
plt.plot(pos[[cx[defect_spring_index1], cy[defect_spring_index1]], 0], pos[[cx[defect_spring_index1], cy[defect_spring_index1]], 1], color='red')
plt.plot(pos[[cx[defect_spring_index2], cy[defect_spring_index2]], 0], pos[[cx[defect_spring_index2], cy[defect_spring_index2]], 1], color='red')
plt.plot(pos[[cx[defect_spring_index3], cy[defect_spring_index3]], 0], pos[[cx[defect_spring_index3], cy[defect_spring_index3]], 1], color='red')
plt.plot(pos[[cx[defect_spring_index4], cy[defect_spring_index4]], 0], pos[[cx[defect_spring_index4], cy[defect_spring_index4]], 1], color='red')
plt.show()

# Initial conditions
a = np.zeros_like(pos)
v = np.zeros_like(pos)
v[:] = v0
a[:] = a0

# Initialize crack length and width
crack_length = 0
crack_width = 0

# Prepare figure
fig = plt.figure(figsize=(4, 4), dpi=80)
ax = fig.add_subplot(111)

# Store information about fractured springs
fractured = np.zeros(len(cx), dtype=bool)  # Initialize as all springs intact
stress = np.zeros_like(cx)
strain = np.zeros_like(cx)
frac_pos = []

#Main loop
for t in range(0, t2):

    # Calculate forces using Hooke's law
    spring_lengths = np.sqrt((pos[cx, 0] - pos[cy, 0])**2 + (pos[cx, 1] - pos[cy, 1])**2)
    spring_forces = (spring_lengths - L) * -k

    # Check for spring fracture
    for i in range(np.size(fractured)):
        if fractured[i]:
            pass
        else:
            stress[i] = spring_forces[i] / (np.pi * (threshold_length**2))
            strain[i] = (spring_lengths[i] - L[i]) / L[i]
            if (spring_lengths[i]-L[i]) > threshold_length:
                fractured[i] = True
                frac_pos.append(cx[i])
                frac_pos.append(cy[i])

    spring_forces[fractured] = 0

    # Sum up forces acting on each node
    forces = np.zeros_like(pos)
    np.add.at(forces, (cx, 0), spring_forces * (pos[cx, 0] - pos[cy, 0]) / spring_lengths)
    np.add.at(forces, (cy, 0), spring_forces * (pos[cy, 0] - pos[cx, 0]) / spring_lengths)
    np.add.at(forces, (cx, 1), spring_forces * (pos[cx, 1] - pos[cy, 1]) / spring_lengths)
    np.add.at(forces, (cy, 1), spring_forces * (pos[cy, 1] - pos[cx, 1]) / spring_lengths)

    # Apply external forces to boundaries
    forces[0::N, :] += external_force_left              #forces on the left side of network
    forces[(M - 1) * N::, :] += external_force_top      #forces on the top side of the network
    forces[0:M, :] += external_force_bottom             #forces on the bottom side of the network
    forces[N - 1::N, :] += external_force_right         #forces on the right side of the network

    stress_min = 0
    stress_max = 600
    stress_max1 = np.max(np.abs(stress))
    print(stress_max1)
    str_dist = stress_max1-stress_min
    if str_dist!=0:
        stress_norm = np.abs(stress/(str_dist))
    else:
        stress_norm = np.abs(stress)

    blue = 1-stress_norm
    red = stress_norm

    # Update accelerations, velocity and position
    a = forces / m
    v += a * dt
    pos += v * dt

    # Clear previous plot
    plt.cla()
    
    plt.plot(pos[:, 0], pos[:, 1], marker='.', color='k', linestyle='none')
    for i in range(len(cx)):
        if fractured[i]==False:
            plt.plot([pos[cx[i], 0], pos[cy[i], 0]], [pos[cx[i], 1], pos[cy[i], 1]], color=(red[i],0,blue[i]))

    #Calculate crack length
    d_max = 0
    d_max_1 = 0
    d_max_2 = 0
    for i in range(np.size(frac_pos)):
        for j in range(np.size(frac_pos)):
            dx = pos[frac_pos[i],0]-pos[frac_pos[j],0]
            dy = pos[frac_pos[i],0]-pos[frac_pos[j],0]
            d = np.sqrt(dx**2+dy**2)
            if d>d_max:
                d_max = d
                d_max_1 = frac_pos[i]
                d_max_2 = frac_pos[j]
    plt.plot([pos[d_max_1,0], pos[d_max_2,0]],[pos[d_max_1,1], pos[d_max_2,1]], marker='.',linestyle='--', color=(1,0,0))

    plt.xlabel("x [mm]")
    plt.ylabel("y [mm]")
    plt.pause(0.0001)

print(d_max)
plt.show()