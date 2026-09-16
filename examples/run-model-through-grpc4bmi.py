# Run the SoilGrids Data Component through *grpc4bmi*

import pathlib
import numpy as np
import matplotlib.pyplot as plt

from grpc4bmi.bmi_client_docker import BmiClientDocker

# Set variables:
# * which Docker image to use,
# * the port exposed through the image, and
# * the location of the configuration file used for the tool.
DOCKER_IMAGE = "csdms/bmi-soilgrids-grpc4bmi"
BMI_PORT = 55555
CONFIG_FILE = pathlib.Path("config.yaml")


# Create a model instance, `m`, through the grpc4bmi Docker client.
# It may take moment to download the model image from Docker Hub.
m = BmiClientDocker(image=DOCKER_IMAGE, image_port=BMI_PORT, work_dir=".")

# The first step in using a BMI is calling the `initialize` method.
# This method requires a configuration file that provides initial values for the SoilGrids Data Component.
# This step may take a moment as the Data Component fetches and downloads the data from the SoilGrids server.
m.initialize(str(CONFIG_FILE))

# Now that we've fetched the data, let's access it through the BMI.
# This will take a few steps.
# It may seem cumbersome at first, but there's payoff at the end.
# Start by displaying the name of the one variable exposed through the BMI.
m.get_output_var_names()
varname, = _
print(varname)

# Find the data type of the soil pH data.
dtype = m.get_var_type(varname)
print(dtype)

# Within the BMI, functions that describe the grids that variables are defined on take an index instead of a variable name.
# Get the grid index for the soil pH variable.
grid = m.get_var_grid(varname)
print(grid)

# Then find the total size of the data.
size = m.get_grid_size(grid)
print(size)

# Next, get the soil pH values.
# 
# Two notes, however:
# 
# * As a rule, memory should not be allocated within a BMI. This leads to the un-Pythonic way that we get the data--first creating an empty array, then passing it to a BMI function to receive values.
# * BMI arrays are flattened. This obviates array ordering issues between languages, but it does make >1D data harder to work with.
# 
# Allocate an array for the soil pH data.
soil_pH = np.ndarray(size, dtype)

# Get the data.
m.get_value(varname, soil_pH)

# Note that the data array is one-dimensional.
print(soil_pH.shape)

# Like all BMI arrays, the pH values returned from the BMI `get_value` function are flattened.
# Let's restore their original dimensionality.
# 
# First, determine the dimensionality of the soil pH variable.
rank = m.get_grid_rank(grid)
print(rank)

# Get the dimensions of the soil pH data, first creating an array to store their values.
shape = np.ndarray(rank, dtype=int)
m.get_grid_shape(grid, shape)
print(shape)

# Reshape the soil pH data, creating a new array.
soil_pH2D = soil_pH.reshape(shape)
print(soil_pH2D.shape)

# Let's visualize the soil pH data as an image.
plt.imshow(soil_pH2D)

# Stop the model and clean up the resources it allocates.
m.finalize()

# Stop the container running through grpc4bmi.
# This is needed by grpc4bmi to properly deallocate the resources it uses.
# It may take a few moments.
del m

# This demonstration of the BMI took a lot of code to reproduce a simple result.
# So why would anyone want to use the BMI?
# The key is that, in this demonstration, only the functions belonging to the BMI were used to access the data.
# No knowledge of the calling syntax of the underlying `Topography` class was used.
# 
# The lesson is: once you've seen one BMI, you've seen them all!
