# NESTplots
This code is here to show the process of performing computations for benchmark plots. 
<br>
Updated 7/2/20 to include better documentation. 
<br>
Goal:
<br>
Get benchmark plots for website to appear in a more convenient way. This includes using a local flask app, which for now is all run locally. 
<br>
The TODOs are at the bottom, and we must finish this before we can integrate automatic plot-creation on the website! 

## Setup your environment
1. Open your terminal, change to the directory you want to work in.
2. Create or activate python 3.7 environment: `conda activate <envname>`
3. Clone this repository: `git clone https://github.com/sophiaandaloro/NESTplots/` 
4. Install requirements: `pip install -r requirements.txt`  **open an issue if I am missing other requirements!**
5. Check that the nestpy version installed is the one that you want to work with.

## The code 
Next, there are three main python files for you to keep track of. 
### 1. `interaction_keys.py`: 
- This one should stay out of your way and you should be able to ignore it except when it makes your life easier.
- A great little tool that allows you to identify interaction types as the following (so that you don't have to memorize numbers used in the wrappers!)
  - nr: Nuclear recoil 
  - wimp: WIMP
  - b8: Boron-8
  - And so on. They are straightforward if you look in this code, and you'll see what you want to make. 
- Should make your life easier. Just any time you want to specify NEST interaction_type, just say `interaction_type='nr'`, or whatever. 
  
### 2. `benchmark_plots.py`
- Makes plots using nestpy of various yields.
- This contains all of the functions that are used to make the plots  which will be called via flask on main.py
<br>
The main components are: 
1. Getting the yields for the interaction types of interest (done via numpy vectorized, rather than a loop)
2. Defining the plots for each of the yields (these aren't looped over because each of them slightly differs)
3. Making the plots via one function so that in main.py, you only have to call the one makeplots() function to make all plots.

Main ingredients for the above steps:
1. np.vectorize, dictionary with yields, field array and energy array.
    - Note: some of the yields will crash the plots at too high of energies (way above physical meaning) so np.nan is returned to keep things running.
2. Plotting tools via matplotlib, but note that all plots are saved in an arbitrary "IMAGE_OBJECTS" object, which, rather than a file, will store the images in a dictionary when called in main.py 
    - (easier for using with flask.)

### 3. `main.py`
- You will call this once you have finished setup. 
- This is the function for launching flask app which will display benchmark plots. 
- All nestpy and NEST code is contained inside of the previous file, `benchmark_plots.py`. We only *call* it here. So, if you see something odd in nestpy, your issue isn't with here.
- io, collections for storing the dictionary of objects locally rather than to disk.
- flask: Flask makes apps...
    - send_file allows us to work with saved image dictionary in Flask; 
    - request processes arguments in url format.
- Returns: an app (!) hosted locally, by you. 

## Tutorial
So you've set up your environment and you're ready to make some benchmark plots. 
This *should* work, if you followed setup correctly. If it doesn't, open an issue please. 
1. Go into this directory on your machine if you aren't already. 
2. Run: `python main.py`.
3. You should see some warnings, ignore (as we always do!)
4. You'll start to see messages from NEST, telling you you're using the default detector. Then you'll see messages from Flask, hopefully, telling you that you're running in debug mode, and give you a port number. 
5. That means you're ready. In your browser, type in `localhost:8080` and hit enter. You should see a welcome message with some instructions for seeing your plots. 
6. Try going here: http://localhost:8080/get_image?interaction=gamma&yieldtype=LY. If your Flask app is working, you should see the Light yields benchmark plot for gamma-ray Electronic Recoils. You did it, take a break. 
7. Fork this repo, improve upon it, make a PR and help make this a much more useful tool. 

## TODOs:
The most important section. Listed in order of urgency/importance/feasibility <br>
- Get the global data also on this local app. 
- Update these plots to new nestpy version, confirm this app works, and update website accordingly. 
- Ideally, make this not a local server running this app, but a remote app that is running with the plots at certain locations: accessible by the NEST website, so we don't have to always download new plots upon new NEST versions.
- Then, we would like a GitHub version to trigger the nestpy to be upgraded on our remote Flask app, then the plots to be remade. A physicist can dream.

## Versions:
v 0.1.0: Finalized July 2, 2020 
