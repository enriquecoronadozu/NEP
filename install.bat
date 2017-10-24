echo Installing  third party libraries ...

python -m pip install --upgrade pip
pip install zmq
pip install tinydb
pip install SpeechRecognition
pip install simplejson
python -m pip install pyaudio
pip install matplotlib
pip install numpy
pip install scipy
pip install -U scikit-learn
pip install sphinx
pip install sphinxcontrib-napoleon
pip install gevent
pip install Flask

pip install dtw

echo Building NEP libraries and packages

python make_nep.py
python make_packages.py
python make_blocks.py
