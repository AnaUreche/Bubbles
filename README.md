# Bubbles - Maya Tool #

Bubbles – Python script for Maya to generate bubble animation resembling real-world movement and interaction.

[Video results here](https://vimeo.com/653191393)

![image](https://user-images.githubusercontent.com/78536620/144664648-743d31db-2607-4e82-8dbc-d13693542f11.png)

Manual
------
1. Open Maya
2. Open Bubbles.py, copy the content and paste it into the Maya script editor
3. Select all the code and run
4. The window on the right should pop up

![image](https://user-images.githubusercontent.com/78536620/144664261-3522447b-3e6d-4ef8-8421-680daa4f0ac6.png)

How to use the UI
-----------------
Button Create new container and creates a cube that should be resized and moved by the user before the animation starts. The button next to it adds any selected object(s) as emitter(s) from where the bubbles will appear. You need both a container and at least an emitter to start. You can reuse the emitter and the container, but the new bubbles will not interact with the old ones. To see the bubbles, you will need to use a transparent shading material on the container.
You can choose the environment and the bubble properties as you like.
If you want to add new forces, please do not forget to press Add force. If you do not like the forces, you can always delete ALL of them by clicking Delete additional forces.
Please do not forget to give the bubbles the lifespan and to introduce the number of frames of your animation, otherwise there will be no movement.
Depending on the number of bubbles and the number of animation frames, the program can run for a few seconds or for a really long time, so I recommend keeping the number of bubbles under 250 and the animation frames under 1000.

In folder 'maya-help-files' you can find my setup for the scene, but it is not necessary to use it.

For in-depth detail on the maths that I used 'help_docs'.
