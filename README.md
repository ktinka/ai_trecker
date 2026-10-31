# AI Trecker
### What is it, exactly?
AI-Trekker is a convenient tool for tracking a person's physical position or orientation in space.

It can be used as a fitness tracker, an assistive device for the elderly (or anyone requiring supervision), or even as a tool to monitor the status of cargo during transit.

### Setup
First, you’ll need to assemble the enclosure: the required materials are listed in the schematic.
Next, flash the Arduino using the code provided in `arduino_sketch`.
Once that’s done, the possibilities are endless. My version uses a model trained on open-source data from Kaggle; it can predict a person’s position based solely on accelerometer data.

### How does it work?
The project consists of two main parts:
1. The logical component (data loading, model processing, and outputting results in a human-readable format).
2. The physical component (the enclosure, circuit board, and hardware).

The tracker relies on several key components:
- Arduino Nano
- Bluetooth module
- Accelerometer
- Battery (accumulator)

The model used is logistic regression.

### What’s next?
Big things are on the horizon:
- A sleek UI.
- Model improvements for more precise position detection.
- Replacing the Bluetooth module (because the HC-05 just isn’t good enough for my highly esteemed iPhone)

meow
