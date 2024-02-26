# Import needed libraries
import cv2
import numpy as np

# Researched from https://medium.com/analytics-vidhya/building-a-lane-detection-system-f7a727c6694, and https://www.geeksforgeeks.org/find-and-draw-contours-using-opencv-python/
# Get video from camera
video = cv2.VideoCapture(0)

while True:
    # Get every frame of video
    ret, frame = video.read()
    # Breaks if the video has ended
    if frame is None:
        break
    # Duplicate the frame
    dup = frame.copy()
    # Turn the frame into grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Find Canny edges
    canny = cv2.Canny(gray, 30, 200)
    # Gets the  height and width of the frame
    height, width = canny.shape
    # Make the rectangle of the mask
    mask = np.zeros_like(gray)
    # Points of the rectangle
    point1 = (100, height - 150)
    point2 = (100, 100)
    point3 = (height - 150, 100)
    point4 = (height - 150, height - 150)
    # Array showing the coordinates of the rectangle
    rectangle = np.array([[point1, point2, point3, point4]])
    # outlines the rectangle for user use
    cv2.line(frame, point1, point2, (255, 255, 255), 3)
    cv2.line(frame, point2, point3, (255, 255, 255), 3)
    cv2.line(frame, point3, point4, (255, 255, 255), 3)
    cv2.line(frame, point4, point1, (255, 255, 255), 3)
    # Creates polygon
    mask = cv2.fillPoly(mask, rectangle, 255)
    # Adds the mask
    mask = cv2.bitwise_and(canny, mask)
    # Finding the contours
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    #Checks to make sure that there is more than 1 contour
    if len(contours) > 1:
        #Initializes empty lists
        areas = []
        contourlist = []
        lengthlist = []

        #Loops through all the contours
        for contour in contours:
            # Gets the area of the contour
            contourarea = cv2.contourArea(contour)
            sentry = 1
            #Checks to make sure the area is unique (plus or minus 10 from existing areas)
            for area in areas:
                if area-10 < contourarea < area + 10:
                    sentry = 0
                    break
            if sentry == 1:
                areas.append(contourarea)
                contourlist.append(contour)
                lengthlist.append(len(contour))
                #Draws the contour on the frame
                cv2.drawContours(frame, [contour], -1, (0, 255, 0), 3)
        #gets the amount of points for the contours
        numpoints = min(lengthlist)
        midpointlist = []

        for i in range(numpoints):
            try:
                #gets the average of the points and appends the point to the midpoint list
                averagex = int((contourlist[0][i][0][0]+contourlist[1][i][0][0])/2)
                averagey = int((contourlist[0][i][0][1] + contourlist[1][i][0][1]) / 2)
                midpointlist.append((averagex,averagey))
            except:
                pass
        if midpointlist is not None:

            midpointlist = np.array(midpointlist)
            #Draws the line connecting all the midpoints
            cv2.polylines(frame,[midpointlist],False, (0,0,0),3)

    #Shows the frame with the lines
    cv2.imshow("Lines", frame)

    # Breaks the video if chracter i is pressed
    if cv2.waitKey(15) & 0xFF == ord('i'):
        break
video.release()
cv2.destroyAllWindows()