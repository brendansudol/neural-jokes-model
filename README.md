**Joke Generation Neural Network**

Multi-layer Recurrent Neural Network (RNN, LSTM) for character-level language
models in Python (Tensorflow) and modified to work with JavaScript
(deeplearn.js, ML5.js)

Based on:

* https://github.com/sherjilozair/char-rnn-tensorflow
* https://github.com/ml5js/ml5-library/tree/master/training/lstm

Develop:

```
virtualenv venv -p python3
source venv/bin/activate
pip install -r requirements
```

Example command:

```
python train.py \
    --data_dir=./data/conan \
    --rnn_size 512 \
    --num_layers 2 \
    --seq_length 100 \
    --batch_size 50 \
    --input_keep_prob 0.75 \
    --output_keep_prob 0.5 \
    --num_epochs 100
```
