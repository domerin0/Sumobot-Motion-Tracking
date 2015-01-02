Sumobot2014
===========

Code for raspberry pi object tracking. Developed for McMaster sumobot competition 2014/2015. This was done to try something new, and ultimately wasn't bad, but the pi lacked the processing power required to make this really useful.

How it works:

1. Takes images, and finds the difference between them.
2. Finds the largest rectangular region of change.
3. Sends a value to an Arduino indicating the yaw.

Some problems with this include:
1. Sumobot needs to be stopped when tracking for best results
2. The framerate is slow (approx 1fps)
