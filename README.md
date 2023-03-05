# NYUv2_to_npy
 Convert NYUv2 dataset from matlab format to npy. 

The program do the following:
 - Download (if not there) the file 'nyu_depth_v2_labeled.mat' from https://cs.nyu.edu/~silberman/datasets/nyu_depth_v2.html. The download link is: http://horatio.cs.nyu.edu/mit/silberman/nyu_depth_v2/nyu_depth_v2_labeled.mat
 - Convert images, labels and depth files to .npy files.
 - Create a test and train dataset randomly seleted from converted data.


## Convert data:
* images
* labels
* depths

## Run:
On a terminal:
```
# Go to project dir
cd go/to/project/

# Activate the virtual environement
source venv_NYUv2/bin/activate

# Run the script
python3 NYUv2_to_npy.py
```

## Set the environment:
Open a terminal and type the followig commands:
```
# Go where the project will be cloned
cd /go/to/dir

# Clone the project
git clone '...'

# Go to project dir
cd NYUv2_to_npy

# Create virtual environment
python3 -m venv venv_NYUv2

# Activate virtual environment
source venv_NYUv2/bin/activate

# Install requirements
pip install -r requirements.txt

# To deactivate the virtual environment
deactivate
```
## Project files architecture/
```
NYU2_to_nyp
| - NYU2_to_nyp.py
| - requirement.txt
| - [nyu_depth_v2_labeled.mat]
| + [data]
|   |   + datset
|   |   |   + depth
|   |   |   |   - 0.npy
|   |   |   |   - ...
|   |   |   + image
|   |   |   |   - 0.npy
|   |   |   |   - ...
|   |   |   + label
|   |   |   |   - 0.npy
|   |   |   |   - ...
|   |   + test
|   |   |   + depth
|   |   |   |   - 0.npy
|   |   |   |   - ...
|   |   |   + image
|   |   |   |   - 0.npy
|   |   |   |   - ...
|   |   |   + label
|   |   |   |   - 0.npy
|   |   |   |   - ...
|   |   + train
|   |   |   + depth
|   |   |   |   - 0.npy
|   |   |   |   - ...
|   |   |   + image
|   |   |   |   - 0.npy
|   |   |   |   - ...
|   |   |   + label
|   |   |   |   - 0.npy
|   |   |   |   - ...
```