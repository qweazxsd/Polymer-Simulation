# Polymer-Simulation

# Abstract

Polymers are long chains made of many identical sub-units called monomers. When no external forces act on the polymer, 
it assumes a random shape in space. In this project I will calculate the average end-to-end distance of a model polymer
in two and three dimensions. The model for a polymer will be a chain made of Nm = 50, 100, 200,... monomers, where the 
length of each monomer is constant but the angle between a monomer and the next one is random. To calculate the mean
end-to-end distance of a polymer with Nm monomers the program will simulate many polymers with the same characteristics
(same number of monomers and monomer length) where the only difference between one polymer to the next is the angle between each 
pair of monomers which is random. After many such simulations there will be many polymers, each with its own Radius. Then the program 
will calculate the average of all said Radii. The output of the program is a linear graph representing the mean Radius as a function of 
polymer length (Nm). In addition the program will output a histogram for each polymer length.

# Project overview

-What is a polymer?

Polymer are huge molecules made out of many repeating sub-units called monomers,
connected in a long thin chain. As the angles between two connected monomers
can take a range of values, the polymer can deform and bend in space.

-Project's Goals

Polymers can assume a range of random shapes. But random how? Are there
more probable shapes then others? The number of configurations is huge, therefore it is impossible to calculate all possible shapes. What can be
done is to calculate or measure the probability distribution of the linear distance between the two ends, which we'll denote as R. We can measure the
probability of a random event out of many random events simply by counting
how many times that event occurred relative to all of the events. Our first goal
will be to create such a graph.

First goal - We will plot a graph of "R counts" vs R. In other words, number
of chains with a given R vs R. This kind of graph is called 'histogram'.

When running such numerical calculations, the resulting end-to-end distances do not generally repeat exactly, the Rs are different for each realization. So seemingly we can't determine which R is more probable. This is where the Histogram helps. Instead of plotting the number of R's with each possible exact value (which generally will be
1 or zero), we divide the range of possible Rs into evenly-spaces bins, and count
how many R's fall into each bin. This gives us an approximate picture of the
probability distribution of R, which gets more accurate the more realizations
we have- this is the basic idea of histograms.

Second goal - We will calculate the average end-to-end distance R_avg for each
number of monomers Nm in a chain, and observe their dependency. Namely,
plot a graph of R_avg vs Nm.

-The 2D model

The following model for a polymer is an over simplification, and there many more
conditions we need to account for in order to fully describe polymer geometry.
First let us consider a two dimensional polymer made out of Nm monomers (See figure 1):

1) Assume the first end of the first monomer in the chain is pinned in one
place - say the origin of your coordinate system. The other end of the
chain is free.

2) In this model we ignore the internal structure of the monomers, and simplify it to be a stick-like line with a typical length denoted as l.

3) Assume the stick-like lines are of zero thickness so they can overlap in
space, i.e. cross each other (Although this is not very physical, we'll allow
it to make things easier).

4) Now, assume the two ends of each monomer to be a sphere with radius r,
which cannot overlap in space with other spheres. So a chain with
N monomers will have N "sticks" and N + 1 spheres.

5) Allow the angle between two monomers to assume any value between 0
and 2 pi, as long as no spheres overlap.

Comments about the model: 

1) Simplifying the monomers to be a stick-like line might look like a bad assumption but keep in mind that we're simulating a long chain,
so the inner structure of a monomer are small compared to the scale of the entire chain.

2) Allowing the monomers to cross eachother is not a very good way to simulate monomers. But trying to code the 'no overlapping'
condition with 2 "sticks", can be a bit more difficult. In addition the execution time might be too long for domestic computers if this condition is implemented.


![Screenshot (137)](https://user-images.githubusercontent.com/79839619/109489827-17e9a700-7a90-11eb-9699-77285265c5fa.png)

Figure 1: Illustration of a simplified 2D model describing a chain of N
monomers. Here the angle between two monomers is denotes as alpha_i, where i
denotes the i-th monomer.

-The 3D model

The 3 dimensional model is similar in philosophy, with the only difference that
we have another coordinate to consider. The obvious coordinate system might
be spherical.

-Random Walk

So how can we generate a random structure of a chain? We will use
the concept of 'Random Walks'. Random walk is a simple idea of taking
many small steps with the same length but in a randomized direction, repeatedly over some mathematical/physical space. This simple concept is used in
describing a variety of phenomena, such as the diffusion of gas molecules, movement of motile bacteria, processes in population genetics, and even processes in
financial economics and more. Here we will use this idea to create the track of
the polymer by randomizing the angle between every couple of monomers (See figure 2), thus creating random polymer configurations.

![Screenshot (138)](https://user-images.githubusercontent.com/79839619/109490984-b0345b80-7a91-11eb-888a-82cbebdbe683.png)

Figure 2: Two examples illustrating two polymers each with two monomers, where phi_0 and phi_1 can take any value between 0 and 2 pi.

Comment regarding the angle: In this program one of the input parameters is Angle Interval. The program then uses said interval to create a list of evenly spaced angles 
in the range of 0 and 2 pi, resulting in a list of discrete angle intervals. Afterwards the program picks one of the items in the list. For example: if the interval given is 
30 degrees, then possible phi's are phi = (0, 1/6 pi, 1/3 pi, ..., 11/6 pi). Note that 2 pi is not included so there will be equal probability for 0 degrees (0 = 2 pi). 
We use discrete values for the angle to better simulate random walk, the smaller Angle Interval is the closer the list is to a continues range, but a continues range can be 
implemented just as easily.


# Program's layout

1. The program will read all the data from the supplied input file, input.txt. This file will contain the parameters of the run and must be of a precise format for the program to parce correctly:

 - Polymer Lengths (list of Nm=total number of monomers per polymer)
 
 - Monomer Length (length of each monomer)
 
 - Edge Diameter (diameter of the spheres at the ends of each monomer)
 
 - Dim (dimension)
 
 - Angle Interval (d_theta and d_phi of the simulation)
 
 - Mean Error (condition for stopping polymers simulations)
 
 - Max Tries (maximum number of polymers simulated per polymer's
  length)
  
  
2. The program will have a function that simulates a single polymer:

single_polymer_sim()

- For single polymer simulation: the program will build the polymer,
one monomer at a time using the random walk principle.

- Before creating the next monomer the function will call another function wich checks if the monomer that would be creatred will collide with any of the monomers that had already been created.

- The program will output each coordinate into a file: coordinates.txt
(the file will be overwritten for each polymer simulated).

- The function will return the radius (R, end-to-end distance) of the
polymer.

 3. The program will output each radius into a file, after it's returned from
the function single_polymer_sim():

- The file name includes the dimension, the total number of monomers for each polymer and the length of every monomer. For example: 'radii_2d_N300_l10.txt'

 4. For each Polymer length (in the list given PolymerLengths), the program
will calculate the polymer's Mean Radius, by simulating as many polymers
as needed (condition given below).

- The Mean Radius is calculated using arithmetic mean 

- How do we know when we found the Mean Radius and can stop the
run (for a single polymers Length)? when the Stopping Criteria is
true:

![Screenshot (139)](https://user-images.githubusercontent.com/79839619/109499466-9d278880-7a9d-11eb-808e-933ae8ed5d5a.png)

R_k is the mean radius which is calculated after every simulation and R_k-1 is the mean radius that had previously been calculated (before the simulation that just happened)

the stopping criteria checks that the size we are calculating (in this
case, Mean Radius) is not significantly affected by anymore calculations, and has already converged to the desired value. In other
words - we want to make sure that if we were to add more calculations (in our case - more simulations), the change in the Mean Radius 
(numerator of the fraction) will only be a small fraction of the value, and so we can deduce there is no need for more calculations. we
decide what is that 'small fraction' by defining MeanErr.

- The program will also stop the run (for a single Polymers Length)
if the number of maximum polymers (Max Tries) is reached.

 5. For each Polymer length, the program will produce a Histogram graph of
all the radii calculated.

- The program will read all the radii from the files (e.g. 'radii_2d_N300_l10.txt')
and will produce an histogram using matplotlib package in python.

 - The program saves all radii calculated in the files for a reason: so every time the program executes the data will not be lost and the histogram will have more data to plot.

6. The program will produce a graph of the Mean Radius Vs. Polymers
Length.








