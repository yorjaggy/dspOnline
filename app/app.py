import os
import pywt
import numpy as np
from scipy import signal
from flask import Flask
from flask import jsonify, request, abort

#https://stackoverflow.com/questions/7703797/need-to-close-python-socket-find-the-current-running-server-on-my-dev-environm
#https://stackoverflow.com/questions/26646362/numpy-array-is-not-json-serializable

app = Flask(__name__)

def is_wname_allowed(wname):
    list = pywt.wavelist();
    if( (wname is not None) and wname != '' ):
        if wname in list:
            return True;
        else:
            return False;

def process_signal(zValue,wname):
    if ( len(zValue)==0 or zValue is None):
        return 0;
    elif is_wname_allowed(wname):
        deco = pywt.dwt(zValue,wname);
        c_a,c_d = deco;
        return signal.resample(c_d,len(c_a)+len(c_d));
    else:
        return 1;

@app.route('/dsp_wave/', methods=['POST'])
def get_wavelet():
    if not request.json or not 'values' in request.json:
        abort(400)
    
    zValue=request.json['values'];
    wname=request.json['wname'];
    #print('zValue-{0}'.format(len(zValue)));
    #print(zValue);
    #print('wname input: ' +wname);
    newZValue=cut_limits(zValue);
    #newZValue=zValue;
    #print('newZValue-{0}'.format(len(newZValue)));
    signal = process_signal(newZValue,wname);
    if( len(str(signal)) == 1):
        if(signal == 0):
            return jsonify({'ans':'values are empty or not valid'})
        elif signal == 1:
            return jsonify({'ans':'incorrect wname'})
    else:
        #print('signal1-{0}'.format(len(newZValue)));
        signal = signal[0:len(newZValue)]
        signal = np.absolute(signal)
        #print('signal2-{0}'.format(len(newZValue)));
        bin = signal
        #print('bin-{0}'.format(len(bin)));
        #print type(bin.tolist());
        #print(bin.tolist());
        return jsonify({'ans':bin.tolist()}), 201

@app.route('/')
def index():
    return "Hello, Wavelet World!"

@app.route('/dsp_wave/wnames/')
def get_wnames():
    _list = pywt.wavelist();
    return jsonify({'wnames':_list}), 200


@app.route('/dsp_peak/', methods=['POST'])
def get_peak_dsp():
    
    return jsonify({'ans':'url under construction'})


if __name__ == '__main__':
    env_debug = int(os.environ["DEBUG"]);
    local_access = int(os.environ["LOCAL"]);

    if env_debug:
        if local_access:
            app.run(debug=True)
        else:
            app.run(debug=True,host= '0.0.0.0')
    else:
        if local_access:
            app.run()
        else:
            app.run(host= '0.0.0.0')