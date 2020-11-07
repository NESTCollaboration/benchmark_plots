'''
main.py

This is the function for launching flask app which will display benchmark plots. 
Calls on: 
- benchmark_plots.py: Holds functions to calculate yields, make plots, and save them into a dictionary.
- io, collections for storing the dictionary of objects locally.
- flask: Flask makes apps; 
send_file allows us to work with saved image dictionary in Flask; 
request processes arguments in url format.
'''
import io
import collections
from flask import Flask, send_file, request
from benchmark_plots import makeplots
import nestpy
version = nestpy.__nest_version__
nestpy_version = nestpy.__version__
nestpy_loc = nestpy.__file__

#  TODO: 
# In IMAGE_OBJECTS, check version of nestpy?  Or generate file upon request?

# Runs makeplots from benchmark_plots.py, stores all plots in IMAGE_OBJECTS
IMAGE_OBJECTS = collections.defaultdict(io.BytesIO)
makeplots(IMAGE_OBJECTS) 

app = Flask(__name__)

@app.route('/get_image')
def get_image():
    filename = request.args.get('interaction') + '_' + request.args.get('yieldtype') + '.png'                                            
    file_object = IMAGE_OBJECTS[filename]
    file_object.seek(0)

    return send_file(file_object,
                     mimetype='image/png')

@app.route('/')
def hello():
    message = "Welcome to your very first Flask app of NEST v"+ version + "! At the end of this URL Type in:"
    typecommand = " /get_image?interaction='type of interaction'&yieldtype='either LY (light yield) or QY (charge yield)' "
    return(message + typecommand)

@app.route('/info')
def get_info():
    info = "NEST v"+ version + "\n nestpy v" + nestpy_version + "\n nestpy location:" + nestpy_loc
    return(info)

if __name__ == '__main__':
    app.run(port=8080, debug=True)
