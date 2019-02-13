How to run:
$python find\_results.py
This will produce console output about RMS error values along with images
showing the results in a graphical format. these images will be saved in the
images folder.

More information:
Each python file starts with a comment describing its purpose. the data folder
contains all data that was used, along with a lot that wasn't. The images folder contains images created by find\_results.py, but also contains images created
by old\_main.py. Those from find\_results.py start with tempc[number]. The number represents the month from which the data was taken.

There is a bash script (print\_from\_day.sh) that can be used to take data from
a particular day out of the full 2017 dataset. isolate\_xy.py can then be used
to create a file for like the ones used by find\_results.py. For April 30th,
2017, one would run the following command:
$./print\_from\_day.sh 04-20 > april30th.txt
The config variables at the beginning of isolate\_xy should be used to target the
correct file.
