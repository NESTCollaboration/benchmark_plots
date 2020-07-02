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
4. Install requirements: `pip install -r requirements.txt` 
5. Check that the nestpy version installed is the one that you want to work with.

Next, there are three main python files for you to keep track of. 
## 1. `interaction_keys.py`
- A great little tool that allows you to identify interaction types as the following (so that you don't have to memorize numbers used in the wrappers!)
  - nr: Nuclear recoil 
  - wimp: WIMP
  - b8: Boron-8
  - And so on. They are straightforward if you look in this code, and you'll see what you want to make. 
- Should make your life easier. Just any time you want to specify NEST interaction_type, just say `interaction_type='nr'`, or whatever. 
  
