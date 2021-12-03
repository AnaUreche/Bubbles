'''
Bubbles

This program has 2 main functions:
	1. start simulation - where the bubbles's characteristics are stored in a list, the bubbles then they are dispersed and the geometry is created 
	2. start keyframe - the bubbles are animated frame by frame while constanly checking collisions, lifespan, forces and the environement's attributes

'''

def checkCollision(r1, x1, y1, z1, r2, x2, y2, z2):
	'''
	Checks collision between two spheres in 3D space.
	
	Parameters:
		r1 (float) : radius of the first sphere
		x1 (float) : x coordinate of the first sphere
		y1 (float) : y coordinate of the first sphere
		z1 (float) : z coordinate of the first sphere 
		
		r1 (float) : radius of the second sphere
		x1 (float) : x coordinate of the second sphere
		y1 (float) : y coordinate of the second sphere
		z1 (float) : z coordinate of the second sphere
		
	Returns:
		1 - if the spheres collide
		0 - if the spheres don't collide    
	'''
	
	# the function uses difference between distance between the centers of the spheres and the sum of thei radius and then compares them with the treshold
	
	threshold = 0.001

	if(((x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2) - (r1 + r2) ** 2 < threshold):
		return 1
	
	return 0

def checkWallCollision(r, x, y, z, containerObj):
	'''
	Checks if a sphere is inside a container shaped as a rectangular parallelepiped in 3D space.
	
	Parameters:
		r          (float) : radius of the sphere
		x          (float) : x coordinate for the sphere
		y          (float) : y coordinate for the sphere
		z          (float) : z coordinate for the sphere 
		
		containerObj (list): the name of the object shaped as a rectangular parallelepiped serving as a container
		
	Returns:
		rez          (list): list of 6 elements of which each element is 1, if the sphere intersects the corresponding face  or is outside of the container on the same side with the face and 0 if it is not the case
	'''
	
	# this function requires that the container was not rotated at all
	
	# getting the object's world coordinates (translate and scale) to check if the sphere is inside 
	
	containerPos = cmds.xform(containerObj[0], q=True, t=True, worldSpace=True)
	containerSizes = []
	containerSizes.append(cmds.getAttr(containerObj[0][0] + ".scaleX"))
	containerSizes.append(cmds.getAttr(containerObj[0][0] + ".scaleY"))
	containerSizes.append(cmds.getAttr(containerObj[0][0] + ".scaleZ"))
 
	rez = [0, 0, 0, 0, 0, 0]
	
	# checking each side of the container considering the 3 axis
	
	if (x - r < containerPos[0] - containerSizes[0] / 2):
		rez[4] = 1
		
	if (r + x > containerPos[0] + containerSizes[0] / 2):
		rez[5] = 1

	if (r + y > containerPos[1] + containerSizes[1] / 2):        
		rez[1] = 1

	if (y - r < containerPos[1] - containerSizes[1] / 2):        
		rez[3] = 1

	if (z + r > containerPos[2] + containerSizes[2] / 2):
		rez[0] = 1

	if (z - r < containerPos[2] - containerSizes[2] / 2):
		rez[2] = 1
	
	return rez
	
def popBubble(i, listOfBubbles, frame):
	'''
	Turns off the visibility of bubble with the given index and for the given frame.
	
	Parameters:
		i              (int) : index of the bubble in list listOfBubbles
		listOfBubbles (list) : list containing all the bubble objects and their properties
    	                       contains [alive, name of the bubble geometry, radius, posX, posY, posZ, xVelocity, yVelocity, zVelocity, startF, stopF, mass]
		frame          (int) : the frame needed to keyframe thevisibility        
   '''

	cmds.setKeyframe(listOfBubbles[i][1], attribute="visibility", v=0, t=[frame], inTangentType="linear", outTangentType="linear")
	
	# updates the end frame for the bubble
	listOfBubbles[i][10] = frame
	
	# marks the bubble with index i as "dead"
	listOfBubbles[i][0] = 0
	
def mergeBubbles(i, j, frame, listOfBubbles, bubbleGroup):
	'''
	Merges 2 bubbles into one withe the corresponding attributes.
	
	i             (int)  : index of the first bubble in listOfBubbles
	j             (int)  : index of the second bubble in listOfBubbles
	frame         (int)  : the frame when the merging takes place
	listOfBubbles (list) : list containing all the bubble objects and their properties
                           contains [alive, name of the bubble geometry, radius, posX, posY, posZ, xVelocity, yVelocity, zVelocity, startF, stopF, mass]
	bubbleGroup          : the group for all of the bubbles created for this animation
	'''
	
	# calculating the end frame for the new bubble by using the end frame values from the bubbles which are merging
	endFrame = (listOfBubbles[i][10] + listOfBubbles[j][10]) / 2
	
	# getting rid of the bubbes which are merging
	popBubble(i, listOfBubbles, frame)
	popBubble(j, listOfBubbles, frame)

	# calculating velocity with the formula for the perfectly elastic collicion
	
	xVelocity = (listOfBubbles[i][6] * listOfBubbles[i][2]**3 + listOfBubbles[j][6] * listOfBubbles[j][2]**3) / (listOfBubbles[i][2]**3 + listOfBubbles[j][2]**3)
	yVelocity = (listOfBubbles[i][7] * listOfBubbles[i][2]**3 + listOfBubbles[j][7] * listOfBubbles[j][2]**3) / (listOfBubbles[i][2]**3 + listOfBubbles[j][2]**3)
	zVelocity = (listOfBubbles[i][8] * listOfBubbles[i][2]**3 + listOfBubbles[j][8] * listOfBubbles[j][2]**3) / (listOfBubbles[i][2]**3 + listOfBubbles[j][2]**3)
	
	# using the same formula for the perfectly elastic collision to calculate the first possition of the new bubble in order to get a smooth transition that resembles real life
	
	xPos = (listOfBubbles[i][3] * listOfBubbles[i][2]**3 + listOfBubbles[j][3] * listOfBubbles[j][2]**3) / (listOfBubbles[i][2]**3 + listOfBubbles[j][2]**3)
	yPos = (listOfBubbles[i][4] * listOfBubbles[i][2]**3 + listOfBubbles[j][4] * listOfBubbles[j][2]**3) / (listOfBubbles[i][2]**3 + listOfBubbles[j][2]**3)
	zPos = (listOfBubbles[i][5] * listOfBubbles[i][2]**3 + listOfBubbles[j][5] * listOfBubbles[j][2]**3) / (listOfBubbles[i][2]**3 + listOfBubbles[j][2]**3)
	
	# calculating the radius of the new bubble
	bubbleSize = (listOfBubbles[i][2]**3 + listOfBubbles[j][2]**3) ** (1.0 / 3.0)
	
	# adding the new bubble to the list, creating its geometry, keyframing its visibility, moving it into the first possition and parenting the geometry to the group of bubbles
	newBubbleList = [1, "", bubbleSize, xPos, yPos, zPos,  xVelocity, yVelocity, zVelocity, frame, endFrame, listOfBubbles[i][11] + listOfBubbles[j][11]]
	listOfBubbles.append(newBubbleList)
	CreateBubble(listOfBubbles,len(listOfBubbles) - 1)
	cmds.setKeyframe(newBubbleList[1], attribute="visibility", v=1, t=[frame], inTangentType="linear", outTangentType="linear")
	cmds.setKeyframe(newBubbleList[1], attribute="visibility", v=0, t=[endFrame], inTangentType="linear", outTangentType="linear")
	moveObject(newBubbleList[1], xPos, yPos, zPos, frame)
	cmds.parent( newBubbleList[1], bubbleGroup)


# source based on Xiaosong Yang: https://brightspace.bournemouth.ac.uk/d2l/le/content/67409/viewContent/672063/View
def disperseBubbles(listOfBubbles, containerObj, emitters, totalVertexNo):
	'''
	Disperses the bubbles/spheres in their container by using the vertexes of the emitter(s).
	
	Parameters:
		listOfBubbles (list) : list containing all the bubble objects and their properties
		                       contains [alive, name of the bubble geometry, radius, posX, posY, posZ, xVelocity, yVelocity, zVelocity, startF, stopF, mass]
		containerObj         : the name of the object shaped as a rectangular parallelepiped serving as a container
		emitters      (list) : list of list object(s) containing pairs of object and its number of vertices
		totalVertexNo  (int) : the total number of vertices in the emitter(s)
		
	Returns:
		0 - if the dispersion falied
		1 - if dispersing was possible
	'''
	
	vertexPos = [0.0, 0.0, 0.0]
	vertexIndex = 0
	countCollisions = 0
	iteration = 0
	i = 0
	while i < len(listOfBubbles):
		foundNewPos = False
		radius = listOfBubbles[i][2]
		while foundNewPos == False:
			foundNewPos = True
			
			# getting a random vertex and then finding which objects he corresponds to
			vertexIndex = random.randint(0, totalVertexNo - 1)
			k = 0
			while vertexIndex >= emitters[k][1]:
				vertexIndex = vertexIndex - emitters[k][1]
				k = k + 1
			
			# getting the world possition of the vertex
			vertexPos = cmds.xform( str(emitters[k][0])+".pnts["+str(vertexIndex)+"]", query=True, translation=True, worldSpace=True)
			xPos = vertexPos[0]
			yPos = vertexPos[1]
			zPos = vertexPos[2]
			j = 0
			countCollisions = 0
			# checking if the vertex possition is inside the container and then checking if the sphere intersects any other spheres in this position
			rez = checkWallCollision(listOfBubbles[i][2], xPos, yPos, zPos, containerObj)

			if rez[0] + rez[1] + rez[2] + rez[3] + rez[4] + rez[5] > 0:
				countCollisions = 1
			else:
				for j in range(i):
					if(checkCollision(listOfBubbles[i][2], xPos, yPos, zPos, listOfBubbles[j][2], listOfBubbles[j][3], listOfBubbles[j][4], listOfBubbles[j][5])):
						countCollisions+=1
						foundNewPos = False
						break
												
			iteration+=1
			
			# if the position is valid the listOfBubbles is updated
			if countCollisions == 0:    
				listOfBubbles[i][3] = xPos
				listOfBubbles[i][4] = yPos
				listOfBubbles[i][5] = zPos
				foundNewPos = True
				i+=1
			
			# if iteration hits 300 the loop is intrerupted
			if iteration >= 300:				
				cmds.confirmDialog( title='Ooops...', message="Can't disperse, please change the object emitter(s), container size or bubble sizes", button=['OK'], defaultButton='OK')
				return 0
	return 1
# source based on Xiaosong Yang ends here

def fillListOfBubbles(noBubbles, bubbleSize, randSize, density, xVelocity, yVelocity, zVelocity, startFrame, randStartFrame, lifeSpan, randLifespan):
	'''
	Fills the list with the bubbles' initiasl attributes.
	
	Parameters:
		noBubbles   (int)    : number of bubbles, indicating the number of initial enttries for the list
		bubbleSize   (float) : diameter of the bubbles
		randSize    (float)  : number used for calculating rando sizes for the bubbles when its valus is greater than 0
		density      (float) : theoretical density of the bubbles
		xVelocity    (float) : initial velocity of all of the bubbles in the x direction
		yVelocity    (float) : initial velocity of all of the bubbles in the y direction
		zVelocity    (float) : initial velocity of all of the bubbles in the z direction
		startFrame     (int) : starting frame for the bubble(s)
		randStartFrame (int) : number used to offset the starting frame randomly when it is greater than 0
		lifeSpan       (int) : the number of frames for which the bubble is visible if no external factor makes it pop/kills it
		randLifespan   (int) : number used to offset the lifespan randomly when it is greater than 0
		
	Returns:
		listOfBubbles (list) : list containing all the bubble's initial properties
	'''
	#initially all of the bubbles are considered alive, even if they might not be visible because it is more helpful and obvious to vheck bubble collision considering this parameter (ignore the bubble if it is dead)
	alive = 1    
	radius = 0
	startF = 0
	stopF = 0
	type = 0
	mass = 0

	listOfBubbles = []
			
	for i in range(noBubbles):
		if randSize > 0:
			radius = abs((bubbleSize + random.uniform(-randSize, randSize) ) / 2)
			if radius == 0:
				radius = bubbleSize / 2
		else:
			radius = bubbleSize / 2
 
		if randStartFrame > 0:
			startF = abs(startFrame + int(random.uniform(-randStartFrame, randStartFrame)))
			if startF == 0:
				startF = startFrame
		else:
			startF = startFrame
		
		if randLifespan > 0:
			stopF = lifeSpan + int(random.uniform(-randLifespan, randLifespan)) + startFrame
			if stopF == 0:
				stopF = lifeSpan + startFrame
		else:
			stopF = lifeSpan + startFrame
			
		mass = 4.19 * density * radius**3
		listOfBubbles.append([alive,"", radius, 0, 0, 0, xVelocity, yVelocity, zVelocity, startF, stopF, mass])
	
	return listOfBubbles
		
def CreateBubble(listOfBubbles, i):
	'''
	Creating a sphere and updating the listOfBubbles with object's name.
	
	Parameters:
		listOfBubbles (list) : list containing all the bubble's initial properties
		                       contains [alive, name of the bubble geometry, radius, posX, posY, posZ, xVelocity, yVelocity, zVelocity, startF, stopF, mass]
		i                    : index of the bubble inn listOfBubbles
	'''

	bubble = cmds.polySphere(r=listOfBubbles[i][2], o = True, ch = True)
	listOfBubbles[i][1] = bubble[0]
	# all of the bubbles are initially invisible
	cmds.setKeyframe(bubble, attribute="visibility", v=0, t=[1], inTangentType="linear", outTangentType="linear")
	
def moveObject(object, posX, posY, posZ, frame):
	'''
	Moving an object and keyframing it.
	
	Parameters:
		object (string) : short name of the object to be scaled
		posX    (float) : moving value in the x direction
		posY    (float) : moving value in the y direction
		posZ    (float) : moving value in the z direction
		frame     (int) : frame at which the object has to be keyframed
	'''    
	cmds.move(posX, posY, posZ, object)
	
	cmds.setKeyframe(object, attribute="tx", v=posX, t=[frame], inTangentType="linear", outTangentType="linear")
	cmds.setKeyframe(object, attribute="ty", v=posY, t=[frame], inTangentType="linear", outTangentType="linear")
	cmds.setKeyframe(object, attribute="tz", v=posZ, t=[frame], inTangentType="linear", outTangentType="linear")


def updateForces(listOfForces, frame):
	'''
	Updating the values of the additional forces and returning the resulting force.
	Parameters:
		listOfForces (list) : contains the attributes of the additional forces
    		                  forceType, x, y, z, startFrame, endFrame
		frame (int)         : the current frame of the animation
	'''
	
	# calculating the last element in the list listOfForces which is a value between 0 and 1
	# 0 when the force is inactive, especially outside its range of frames
	
	resultantForce = [0, 0, 0]
	x = 0
	y = 0
	z = 0
	
	# we calculate the resulting force by adding the forcrs active in the current frame
	for i in range (len(listOfForces)):
		if frame >= listOfForces[i][4] and frame <= listOfForces[i][5]:
			if listOfForces[i][0] == 1:
			    # in this case the force was set as constant
				listOfForces[i][6] = 1
			else:
				if listOfForces[i][6] == 3:
    			    # in this case the force was set as smooth random
					listOfForces[i][6] = abs(listOfForces[i][6] + random.uniform(-1, 1) / 10)
					#listOfForces[i][6] = abs(math.cos(math.radians(frame)))
				else:
    			    # in this case the force was set as random
					listOfForces[i][6] = random.uniform(0, 1)
		else:
			listOfForces[i][6] = 0
			
		resultantForce[0] = resultantForce[0] + listOfForces[i][1] * listOfForces[i][6]
		resultantForce[1] = resultantForce[1] + listOfForces[i][2] * listOfForces[i][6]
		resultantForce[2] = resultantForce[2] + listOfForces[i][3] * listOfForces[i][6]
	
	return resultantForce
			
def startKeyframing(listOfBubbles, listOfForces, containerObj, fps, animationFrames, envType, gravAcc, waterDensity, wallCollisionQ, bubbleCollisionQ, bubblePopQ, bounciness, bubbleGroup, bubbleDensity):
	'''
	Parameters:
		listOfBubbles   (list) : list containing all the bubble's initial properties
		                         contains [alive, name of the bubble geometry, radius, posX, posY, posZ, xVelocity, yVelocity, zVelocity, startF, stopF, mass]
		listOfForces    (list) : contains the attributes of the additional forces
                                 forceType, x, y, z, startFrame, endFrame
		containerObj    (list) : the name of the object shaped as a rectangular parallelepiped serving as a container 
		fps              (int) : the framerate (frames per second)
		animationFrames  (int) : the numeber of frames in the animation/to be keyframed 
		envType          (int) : the type of environement (1 - underwater, 2 - air) where the bubbles being animated
		gravAcc        (float) : gravitational acceleration value
		waterDensity   (float) : theoretical density of the water
		wallCollisionQ   (int) : 1 if wall collision is considered, 2 if it is ignored
		bubbleCollisionQ (int) : 1 if bubble collision is considered, 2 if it is ignored
		bubblePopQ       (int) : 1 - bubbles pop when they touch, 2 bubbles merge when they touch
		bounciness     (float) : 0 to 1 values, 0 when tehre is no collision response and 1 for full collision response
		bubbleGroup            : the group for all of the bubbles created for this animation
		bubbleDensity  (float) : theoretical density of the bubbles
		
	'''
	
	rez1 = [0, 0, 0, 0, 0, 0]
	force = [0, 0, 0] 
	
	# gets the translation and the scaling of the container to use them for checking wall collision   
	containerPos = cmds.xform(containerObj[0], q=True, t=True, worldSpace=True)
	containerSizes = []
	tempCollisionList = []
	containerSizes.append(cmds.getAttr(containerObj[0][0] + ".scaleX"))
	containerSizes.append(cmds.getAttr(containerObj[0][0] + ".scaleY"))
	containerSizes.append(cmds.getAttr(containerObj[0][0] + ".scaleZ"))
	
	# preset list of collision log in to compare them with the new results
	bubble = 0
	while bubble < (len(listOfBubbles)):
		tempCollisionList.append(rez1)
		cmds.setKeyframe(listOfBubbles[bubble][1], attribute="visibility", v=1, t=[listOfBubbles[bubble][9]], inTangentType="linear", outTangentType="linear")
		cmds.setKeyframe(listOfBubbles[bubble][1], attribute="visibility", v=0, t=[listOfBubbles[bubble][10]], inTangentType="linear", outTangentType="linear")
		bubble+=1
			
	i = 1
	# starting the main loop for keyframing
	while i <= animationFrames:
		j = 0        
		#cmds.currentTime( i, edit=True )
		force = updateForces(listOfForces, i)
		while j < (len(listOfBubbles)):        
			if listOfBubbles[j][9] <= i and listOfBubbles[j][10] >= i and listOfBubbles[j][0]:
				wallCollision = -1
				temp = [1,1,1]
				if wallCollisionQ == 1:
					# checking wall collision
					# if the value in list rez is different perform changing of direction (multiply by -1) in the respective axis while also considering the bounciness
					rez = checkWallCollision(listOfBubbles[j][2], listOfBubbles[j][3], listOfBubbles[j][4], listOfBubbles[j][5], containerObj)
					if (rez[4] != tempCollisionList[j][4] or rez[5] != tempCollisionList[j][5]) and (rez[4] == 1 or rez[5] == 1):
					    listOfBubbles[j][6] = -1 * listOfBubbles[j][6] * bounciness

					if (rez[1] != tempCollisionList[j][1] or rez[3] != tempCollisionList[j][3]) and (rez[1] == 1 or rez[3] == 1):
					    listOfBubbles[j][7] = -1 * listOfBubbles[j][7] * bounciness

					if (rez[0] != tempCollisionList[j][0] or rez[2] != tempCollisionList[j][2]) and (rez[0] == 1 or rez[2] == 1):
					    listOfBubbles[j][8] = -1 * listOfBubbles[j][8] * bounciness
					    
				    # in case the bubble hits a wall the additional forces should not be applied in that direction so we use the list temp to do that
					if (rez[4] == 1 or rez[5] == 1):
					    temp[0] = 0
					if (rez[1] == 1 or rez[3] == 1):
					    temp[1] = 0
					if (rez[0] == 1 or rez[2] == 1):
					    temp[2] = 0
					    
					if envType == 2:
						if rez[3] == 1:
							# when the bubble hits the bottom it pops like a soap bubble
							popBubble(j, listOfBubbles, i)
					else:
						if rez[1] == 1:
							# when the bubble hits the top it pops like an air bubble when it gets out of the water
							popBubble(j, listOfBubbles, i)
					tempCollisionList[j] = rez					

				if(bubbleCollisionQ == 1):
				    k = 0
				    # if active/alive bubbles collide they pop or they merge, depending on the user preferences
				    while k < j:
					    if listOfBubbles[k][0]:
					        if checkCollision(listOfBubbles[j][2], listOfBubbles[j][3], listOfBubbles[j][4], listOfBubbles[j][5], listOfBubbles[k][2], listOfBubbles[k][3], listOfBubbles[k][4], listOfBubbles[k][5]):
					            if bubblePopQ == 1:
					                popBubble(j, listOfBubbles, i)
					                popBubble(k, listOfBubbles, i)
				                else:
									# for bubble merging we need a collision list for it too 
									tempCollisionList.append(rez1)
  
									mergeBubbles(k, j, i, listOfBubbles, bubbleGroup)
						k+=1
				
				if envType == 2:
					# in this case gravity acceleration is applied and added to the bubble velocity
					listOfBubbles[j][7] = listOfBubbles[j][7] - gravAcc * listOfBubbles[j][11]                    
				else:
					# adding the force caused by the difference in density between the air and the water
					# if the densityis negative, the bubble will go down so we have to e careful not to go outside of the container in this case
					# could have been avoided by changing the density range, but it gives interesting results
					if (waterDensity - bubbleDensity > 0) or (tempCollisionList[j][3] !=1):
					    listOfBubbles[j][7] = listOfBubbles[j][7] + (waterDensity - bubbleDensity) * listOfBubbles[j][2]**3 * 4.19 / 8
				# moving the bubble and keyfarming

				moveObject(listOfBubbles[j][1], listOfBubbles[j][3] , listOfBubbles[j][4] , listOfBubbles[j][5] , i)
				# calculating the possitions for the next frame
				# the additional forces are added only if there was no wall collision to avoid having them mess up the movement
				listOfBubbles[j][3] = 1 / fps  * listOfBubbles[j][6] + listOfBubbles[j][3] + force[0] * temp[0] /fps
				listOfBubbles[j][4] = 1 / fps  * listOfBubbles[j][7] + listOfBubbles[j][4] + force[1] * temp[1] /fps
				listOfBubbles[j][5] = 1 / fps  * listOfBubbles[j][8] + listOfBubbles[j][5] + force[2] * temp[2] /fps

			j+=1
		i+=1

def blockAttributes(obj):
	'''
	Blocking the attributes of the object.
	'''
	attr = ['.tx', '.ty', '.tz', '.rx', '.ry', '.rz', '.sx', '.sy', '.sz']
	for i in attr:   
		cmds.setAttr(obj+i, lock = 1)        

def StartSimulation(containerObj, emitters, noBubbles, bubbleSize, randSize, densityControl, xVelocity, yVelocity, zVelocity, startFrame, randStartFrame, lifeSpan, randLifespan, listOfForces, animationFrames, envType, gravAcc, waterDensity, wallCollision, bubbleCollision, bubblePop, bounciness):
	'''
	Fills the listOfBubbles, disperses the bubbles if possible, creates the bubbles and starts animating if the emitters and the container are valid.
	'''
	
	# checking if the container and the emitters are set and if they are valid (they were not deleted of renamed)
	ok = 1	
	for i in emitters:
		if not cmds.objExists(i[0]):
			ok = 0
		
	if containerObj[1] and cmds.objExists(containerObj[0][0]) and ok:
	    # getting the frames per second to calculate the distance for every frame in function startKeyframing
		fps = mel.eval('float $fps = `currentTimeUnitToFPS`')
		listOfBubbles = fillListOfBubbles(noBubbles, bubbleSize, randSize, densityControl, xVelocity, yVelocity, zVelocity, startFrame, randStartFrame, lifeSpan,randLifespan)
		totalVertexNo = getTotalVertexNo(emitters)
		
		if disperseBubbles(listOfBubbles, containerObj, emitters, totalVertexNo) == 1:
		    # grouping the bubbles to avoid having a messy outliner and to be able to move them toghether as a group
			bubbleGroup = cmds.group( em=True, name='Bubbles0' )
			i = 0
			
			while i < len(listOfBubbles):

				CreateBubble(listOfBubbles, i)
				cmds.parent( listOfBubbles[i][1],bubbleGroup )	
				moveObject(listOfBubbles[i][1], listOfBubbles[i][3], listOfBubbles[i][4], listOfBubbles[i][5], listOfBubbles[i][9])			
				i+=1
			startKeyframing(listOfBubbles,listOfForces, containerObj, fps, animationFrames, envType, gravAcc, waterDensity, wallCollision, bubbleCollision, bubblePop, bounciness, bubbleGroup, densityControl)            
	else:
		cmds.confirmDialog( title='Ooops...', message='Please make sure that you have created a new container and that you have added your emitter(s).', button=['OK'], defaultButton='OK')

# source from on Xiaosong Yang: https://brightspace.bournemouth.ac.uk/d2l/le/content/67409/viewContent/672063/View
def cancelProc(*pArgs):
	''' close up the popup window'''
	cmds.deleteUI("Bubbles")
# source from on Xiaosong Yang ends here

def deleteList(myList):
	'''
	Deleting all of the elements in the list.
	'''
	del myList[:]
	
def addForce(listOfForces, forceType, x, y, z, startFrame, endFrame):
	'''
	Updating the list of forces with a new entry.
	
	Parameters:
		listOfForces (list) : contains the attributes of the additional forces or None if it is empty
		forceType     (int) : 1 if the force is constant, 2 if the corce is random, 3 if the force is smooth random
		x           (float) : velocity in x direction
		y           (float) : velocity in y direction
		z           (float) : velocity in z direction
		startFrame    (int) : the first frame when the force is active
		endFrame      (int) : the last frame when the force is active
	'''
	
	listOfForces.append([forceType, x, y, z, startFrame, endFrame, 1])

def createContainer(containerObj, emitters):
	'''
	Creates a new container and empties the list of emitters.
	
	Parameters:
		containerObj (list) : list of 2 elements (the name of the container object and a boolean)
		emitters     (list) : list of list object(s) containing pairs of object and its number of vertices    
	'''
	
	del emitters[:]
	cube = cmds.polyCube(n = 'container0')
	containerObj[0] = cube
	containerObj[1] = False
	
	# locking the rotation attributes as it may raise problems for the wall-bubble collision later if they are changed from the default values
	attr = ['.rx', '.ry', '.rz']
	for i in attr:   
		cmds.setAttr(cube[0] + i, lock = 1)

def getTotalVertexNo(emitters):
	'''
	Adds the vertex number for each emitter.
	
	Parameters:
		emitters     (list) : list of list object(s) containing pairs of object and its number of vertices
		
	Returns:
		totalvertexNo (int) : the number of total verticesof the emitters
	'''
	
	totalvertexNo = 0
	for i in emitters:
		totalvertexNo = totalvertexNo + i[1]
	
	return totalvertexNo

def getVtxNumber( object ) :
	'''
	Returns the number of vertices in object.
	'''
	
	vtxWorldPosition = []    # will contain positions in space of all object vertex
	vtxIndexList = cmds.getAttr( object+".vrts", multiIndices=True )
	return len(vtxIndexList)

def addEmitter(emitters, selectionList, containerObj):
	'''
	If the user forgot to create a container, the function creates one instead and then adds the selected objects to the list of emitters,
	together with their number of vertices.
	
	Parameters
		emitters      : the list of emitters which is formed of lists of 2 elements (the emitter object, the object's number of vertices)
		selectionList : a list containing the selected objects
		containerObj  : the name of the object preset as a container or nothing if the container has not been preset
	'''
	
	if not (containerObj[0]) or not cmds.objExists(containerObj[0][0]):
		createContainer(containerObj, emitters)
		
	for i in selectionList:        
		try:
			vtxNo = getVtxNumber(i)
			emitters.append([i, vtxNo])
			containerObj[1] = True
		except:
			print("An exception occurred")        
    

# source based on Xiaosong Yang: https://brightspace.bournemouth.ac.uk/d2l/le/content/67409/viewContent/672063/View    
def bubblesSystemUI():	
	''' create the User interface for creating a container, adding emitter(s), bubble, collision and environement properties, adding extra forces
		choosing the strating frame(s) and the lifespam of the bbubbles, the number of frames to be keyframed and strating to create the animation 
		procedurally
	'''
	
	# list that holds the dictionaries
	
	# dictionaries for preset values
	# in order to get good results please use the reset vales with the corresponding containers and emitters provided in the maya scene
	# for the container, please create it from the UI and then scale it to fit into the MainContainer
	# but you can create your own containers and emitters too 
	
	#
	# default values
	#
	
	preset = {"numberBubbles" : 1, "size" : 5.0, "sizeRand" : 0.0, "density" : 0.0000, "bbVelx" : 0.0000, "bbVely" : 0.0000, "bbVelz" : 0.0000,
	"bounciness" : 1.0000, "wallCollision" : 1, "bubbleCollision" : 1, "bubbleCollisionBehaviour" : 1, "environement" : 1, "gravitationalAcc" : 9.8,
	"water" : 1.0000, "typeForce" : 1, "forceX" : 0.0000, "forceY" : 0.0000, "forceZ" : 0.0000, "forceStart" : 1, "forceEnd" : 1, "startFrame" : 1,
	"startRand" : 0, "lifespan" : 1, "lifespanRand" : 0, "keyframes" : 0}
	
	#
	# set 1 - air bubbles in water raising to the surface from the bottom
	#
	
	#preset = {"numberBubbles" : 80, "size" : 2.4, "sizeRand" : 2.3, "density" : 0.0075, "bbVelx" : -5.0000, "bbVely" : 0.0000, "bbVelz" : -7.0000,
	#"bounciness" : 0.8000, "wallCollision" : 1, "bubbleCollision" : 1, "bubbleCollisionBehaviour" : 2, "environement" : 1, "gravitationalAcc" : 9.8,
	#"water" : 1.0000, "typeForce" : 1, "forceX" : 0.0000, "forceY" : 0.0000, "forceZ" : 0.0000, "forceStart" : 1, "forceEnd" : 1, "startFrame" : 1,
	#"startRand" : 0, "lifespan" : 700, "lifespanRand" : 0, "keyframes" : 700}
	
	#
	# set 2 - air bubbles in water moving around and then raising
	#
	
	#preset = {"numberBubbles" : 80, "size" : 0.9, "sizeRand" : 0.4, "density" : 0.0075, "bbVelx" : -15.0000, "bbVely" : -30.0000, "bbVelz" : -10.0000,
	#"bounciness" : 0.5700, "wallCollision" : 1, "bubbleCollision" : 1, "bubbleCollisionBehaviour" : 2, "environement" : 1, "gravitationalAcc" : 9.8,
	#"water" : 1.0000, "typeForce" : 1, "forceX" : 0.0000, "forceY" : 0.0000, "forceZ" : 0.0000, "forceStart" : 1, "forceEnd" : 1, "startFrame" : 115,
	#"startRand" : 114, "lifespan" : 650, "lifespanRand" : 0, "keyframes" : 650}
	
	#
	# set 3 - bubbles pop
	#
	
	#preset = {"numberBubbles" : 30, "size" : 4.0, "sizeRand" : 2.6, "density" : 0.0000, "bbVelx" : 20.0000, "bbVely" : 0.0000, "bbVelz" : 17.0000,
	#"bounciness" : 0.8000, "wallCollision" : 1, "bubbleCollision" : 1, "bubbleCollisionBehaviour" : 1, "environement" : 2, "gravitationalAcc" : 9.8,
	#"water" : 1.0000, "typeForce" : 1, "forceX" : 0.0000, "forceY" : 0.0000, "forceZ" : 0.0000, "forceStart" : 1, "forceEnd" : 1, "startFrame" : 1,
	#"startRand" : 0, "lifespan" : 150, "lifespanRand" : 0, "keyframes" : 150}
	
	#
	# set 4 - soap bubbles falling slowly and merging
	#

	#preset = {"numberBubbles" : 100, "size" : 2.4, "sizeRand" : 1.2, "density" : 0.0075, "bbVelx" : 2.0000, "bbVely" : 0.0000, "bbVelz" : 5.0000,
	#"bounciness" : 0.0150, "wallCollision" : 1, "bubbleCollision" : 1, "bubbleCollisionBehaviour" : 2, "environement" : 2, "gravitationalAcc" : 0.3,
	#"water" : 1.0000, "typeForce" : 1, "forceX" : 0.0000, "forceY" : 0.0000, "forceZ" : 0.0000, "forceStart" : 1, "forceEnd" : 1, "startFrame" : 1,
	#"startRand" : 0, "lifespan" : 800, "lifespanRand" : 0, "keyframes" : 800}
	
	
	windowID = 'Bubbles'
	if cmds.window(windowID, exists=True):
		cmds.deleteUI(windowID)
	
	winWidth = 500;
	winHeight = 500;
	cmds.window(windowID, wh=(winWidth,winHeight))
	scrollLayout = cmds.scrollLayout(
	horizontalScrollBarThickness=10,
	verticalScrollBarThickness=10)
	cmds.columnLayout(adjustableColumn=True )

	containerObj = []
	emitters = []
	containerObj.append("")
	containerObj.append(False)
	cmds.text( label='' )
	cmds.text( label='Container and emitter' )
	cmds.text( label='' )
	cmds.rowColumnLayout( numberOfColumns=2,  co = [(1, 'left', 33), (2, 'both', 35)])
	cmds.button(label = "Create new container", command = lambda *args: createContainer(containerObj, emitters), w = 200)	
	cmds.button(label = "Add selected object as emitter", command = lambda *args: addEmitter(emitters, cmds.ls( selection=True , sn = True), containerObj), w = 200)
	cmds.setParent('..')
	cmds.columnLayout( adjustableColumn=True)	
	cmds.separator(style="in", width=10, height = 20)	
	cmds.text( label='Bubble properties' )
	cmds.text( label='' )
	noBubblesControl = cmds.intSliderGrp(label='Number of bubbles', minValue=1, maxValue=1000, value= preset["numberBubbles"], field=True)
	
	bubbleSizeControl = cmds.floatSliderGrp(label='Size', minValue=0.1, maxValue=40, value=preset["size"], field=True)
	randSizeControl = cmds.floatSliderGrp(label='Size Random', minValue=0, maxValue=40, value=preset["sizeRand"], field=True)
	densityControl = cmds.floatSliderGrp(label='Density (g/cm^3)', minValue=0, maxValue=2, value=preset["density"], field=True, step = 0.0001)

	cmds.rowColumnLayout( numberOfColumns=4, columnAttach=(1, 'left', 62) )
	cmds.text( label='Bubble velocity ' )
	xVelocity = cmds.floatField( minValue=-100, maxValue=100, precision=4, step=.001, value = preset["bbVelx"] )
	yVelocity = cmds.floatField( minValue=-100, maxValue=100, precision=4, step=.001, value = preset["bbVely"] )
	zVelocity = cmds.floatField( minValue=-100, maxValue=100, precision=4, step=.001, value = preset["bbVelz"] )
	cmds.setParent('..')
	cmds.separator(style="in", width=10, height = 20)
	cmds.text( label='Collision properties' )
	cmds.text( label='' )
	bouncinessControl = cmds.floatSliderGrp(label='Bounciness', minValue=0, maxValue=1, value=preset["bounciness"], field=True, step = 0.0001)
	wallCollision = cmds.radioButtonGrp( label='Allow wall collision', labelArray2=['Yes', 'No'], numberOfRadioButtons=2, sl = preset["wallCollision"] )
	
	bubbleCollision = cmds.radioButtonGrp( label='Allow bubble collision', labelArray2=['Yes', 'No'], numberOfRadioButtons=2, sl = preset["bubbleCollision"] )
	
	bubblePop = cmds.radioButtonGrp( label='Bubble collision behaviour', labelArray2=['Pop', 'Merge'], numberOfRadioButtons=2, sl = preset["bubbleCollisionBehaviour"] )
	
	cmds.columnLayout( adjustableColumn=True )
	
	cmds.separator(style="in", width=10, height = 20)
	cmds.text( label='Environement properties' )
	cmds.text( label='' )
	
	envTypeControl = cmds.radioButtonGrp( label='Environement', labelArray2=['Underwater', 'Air'], numberOfRadioButtons=2, sl = preset["environement"])
	
	gravAccControl = cmds.floatSliderGrp(label='Gravitational acceleration', minValue=0, maxValue=10, value=preset["gravitationalAcc"], field=True)
    # the values for water density correspond to the real ones
	waterDensityControl = cmds.floatSliderGrp(label='Water density (g/cm^3)', minValue=0.95, maxValue=1, value=preset["water"], field=True, step = 0.0001)
	
	cmds.separator(style="in", width=10, height = 20)
	cmds.text( label='Additional forces' )
	cmds.text( label='' )
	
	forceTypeControl = cmds.radioButtonGrp( label='Type of force', labelArray3=['Constant', 'Random', 'Smooth Random'], numberOfRadioButtons=3, sl = preset["typeForce"])
	cmds.text( label=' ' )
	cmds.rowColumnLayout( numberOfColumns=4, columnAttach=(1, 'left', 105) )
	
	listOfForces = []
	
	cmds.text( label='Values ' )
	xForce = cmds.floatField( minValue=-100, maxValue=100, precision=4, step=.001, value = preset["forceX"] )
	yForce = cmds.floatField( minValue=-100, maxValue=100, precision=4, step=.001, value = preset["forceY"] )
	zForce = cmds.floatField( minValue=-100, maxValue=100, precision=4, step=.001, value = preset["forceZ"] )
	
	cmds.setParent('..')

	startFrameForceControl = cmds.intSliderGrp(label='Start frame', minValue=1, maxValue=10000, value=preset["forceStart"], field=True)
	endFrameForceControl = cmds.intSliderGrp(label='End frame', minValue=1, maxValue=10000, value=preset["forceEnd"], field=True)	
	cmds.text( label=' ' )
	cmds.rowColumnLayout( numberOfColumns=2,  co = [(1, 'left', 33), (2, 'both', 35)])
	cmds.button(label = "Add force", w = 200, command = lambda *args: addForce(listOfForces, cmds.radioButtonGrp(forceTypeControl, query=True, select=True), cmds.floatField(xForce, query=True, value=True),  cmds.floatField(yForce, query=True, value=True),  cmds.floatField(zForce, query=True, value=True),  cmds.intSliderGrp(startFrameForceControl, query=True, value=True), cmds.intSliderGrp(endFrameForceControl, query=True, value=True)))

	cmds.button(label = "Delete additional forces",w = 200, command = lambda *args: deleteList(listOfForces))	
	cmds.setParent('..')
	cmds.separator(style="in", width=10, height = 20)
	
	startFrameControl = cmds.intSliderGrp(label='Start Frame', minValue=1, maxValue=10000, value=preset["startFrame"], field=True)
	randStartFrameControl = cmds.intSliderGrp(label='Start Random', minValue=0, maxValue=10000, value=preset["startRand"], field=True)
	
	cmds.separator(style="in", width=10, height = 20)
	
	lifespanControl = cmds.intSliderGrp(label='Lifespan', minValue=1, maxValue=10000, value=preset["lifespan"], field=True)
	randLifespanControl = cmds.intSliderGrp(label='Lifespan Random', minValue=0, maxValue=10000, value=preset["lifespanRand"], field=True)

	cmds.separator(style="in", width=10, height = 20)
	
	cmds.setParent('..')

	cmds.columnLayout( adjustableColumn=True) 
	animationFrames = cmds.intSliderGrp(label='Number of key frames', minValue=0, maxValue=10000, value=preset["keyframes"], field=True)
	cmds.text( label=' ' )
	cmds.button(label = "Start bubble animation", command = lambda *args: StartSimulation(containerObj, emitters, cmds.intSliderGrp(noBubblesControl, query=True, value=True), cmds.floatSliderGrp(bubbleSizeControl, query=True, value=True), cmds.floatSliderGrp(randSizeControl, query=True, value=True), cmds.floatSliderGrp(densityControl, query=True, value=True), cmds.floatField(xVelocity, query=True, value=True), cmds.floatField(yVelocity, query=True, value=True), cmds.floatField(zVelocity, query=True, value=True), cmds.intSliderGrp(startFrameControl, query=True, value=True),cmds.intSliderGrp(randStartFrameControl, query=True, value=True), cmds.intSliderGrp(lifespanControl, query=True, value=True),cmds.intSliderGrp(randLifespanControl, query=True, value=True), listOfForces, cmds.intSliderGrp(animationFrames, query=True, value=True), cmds.radioButtonGrp(envTypeControl, query=True, select = True), cmds.floatSliderGrp(gravAccControl, query=True, value=True), cmds.floatSliderGrp(waterDensityControl, query=True, value=True), cmds.radioButtonGrp(wallCollision, query=True,select = True), cmds.radioButtonGrp(bubbleCollision, query=True, select = True), cmds.radioButtonGrp(bubblePop, query=True, select = True), cmds.floatSliderGrp(bouncinessControl, query=True, value=True) ))

	cmds.setParent('..')

	cmds.columnLayout( adjustableColumn=True )
	cmds.separator(style="in", width=10, height = 20)


	cmds.button(label = "Finished", command = cancelProc)
	cmds.showWindow()

	
# main program, start with the function bubblesSystemUI()
if __name__ == "__main__":
	import maya.cmds as cmds
	import maya.mel as mel
	import random
	import math as math
	bubblesSystemUI()
# source based on Xiaosong Yang ends here