# Wolf Algorithm for Images

Implementation of Wolf Algorithm applied for random-generated pictures. 

## Wolf Algorithm

Scientists usually use this algorithm when they simulate Ising Model. This algorithm use stack for
finding clusters with the same state (+1 or -1 in Ising Model). In this repository this idea
applied to images. 

### Steps
1. Generate picture and fill it with random pixels
2. Choose random pixel in the picture
3. Check if neighbour pixels have similar color
4. Change the color of whole cluster of similar pixels
5. Repeat the procedure while this the picture is not one color

## Results

TODO("add video")
