# Sketch - Virtual Etch-A-Sketch #

Drawing interface inspired by the famous Etch-A-Sketch done for my programming assignment in 1st year at Bournemouth University.

![image](https://user-images.githubusercontent.com/78536620/144669398-720de0ec-9e18-4d42-83d8-fb8daedb6c0e.png)

1. To move the brush you press “a” for up, “d” for down, left key for left and right key for right.
2. New file button creates a new file.
3. Save file saves the file with the name written by the user in the textbox.
4. Open file button opens the file with the name written in the textbox.
5. You can write in the textbox after clicking on it once.
6. To delete what you just wrote you can press the “x” button on the right of the textbox.
7. You can choose which brush you want to use by clicking on one of them.
8. You can resize your brush by clicking on the “-” and “+” buttons.
9. The big button filled with black is the current colour of the brush. You can change it by choosing a colour from the colour palette.
10. To choose a colour of the palette you can just click on it.
11. The 2 small black buttons represent the colours you can use with the mix buttons. You can pick the colour for them by selecting the button and then the colour. To get the other colour you just do the same thing for the other small black button.
12. Mix 1 blends the colours selected above. The result is more beautiful if the colours you chose are from the same quadrant of the colour palette.
13. Mix 2 uses the selected colours for a more spontaneous transition,
14. The twin buttons 1, 2, 3 create a twin brush which moves along with your brush. If you do not want to use the twin mode anymore you can click on
it to unselect it.
15. You can change the colour of the canvas by clicking on the small white button at the bottom of the menu and then selecting a colour. However, it
will fill the entire canvas so you might lose your work. Also, the background colour and the brush colour can be both selected and then they will
change the colour at the same time, leaving the whole canvas with the same colour.



Developed and tested on Linux
-----------------------------

build: Sketch
	./Sketch

Sketch: Sketch.c
	clang Sketch.c -l SDL2 -l SDL2_image -l SDL2_ttf -o Sketch

Dependencies
------------

SDL2



































Unfortunately, due to some technical difficulties, I was not able to upload animations of the latest version of my script. In the ones that I attached the was collision is a bit weird and unnatural. I managed to fix it and I also tested that it works, but when I wanted to start making the new animations Maya stopped working and after I restarted the computer it refused to open at all.
I put in dictionaries the values I used for the videos, except for the pill one.  You can use them by uncommenting the dictionary that you want to use. I also put the emitters I used in the Maya scene that I attached (templateScene). There are also the animations for the videos.
The 3 images I uploaded were rendered using the Arnold renderers aiStandardSurface texture, but the values I used are meant for glass texture. They are meant to give a better understanding of how the tool can be used and that the bubbles can pass as not questionable if rendered well. They could really fit in an animation placed underwater.
Pill.avi video is meant to show a practical use of the bubbles. In this case, the pill id the emitter and the container were placed inside the round glass in a way that it did not hit its walls.
bubbleRendered.mp4 has the same animation as Set1Playblast.avi.
Pop.avi video shows how bubbles pop when they touch. It is achieved with the values from the 3rd set.
Set4Playblast.avi shows how bubbles merge.
The texture used in the playblasts is Texture.ma
