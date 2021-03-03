import pandas as pd
import cv2
import argparse
import keyboard
#Creating path to use cmd
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help="Image Path")
args = vars(ap.parse_args())
img_path = args['image']
#Reading image with opencv
img_need_to_resize = cv2.imread(img_path)
img = cv2.resize(img_need_to_resize,(500,500))
clicked = False
r = g = b = xpos = ypos = 0

#read csv
index=["color","color_name","hex","R","G","B"]
csv = pd.read_csv('colors.csv', names=index, header=None)
#print(csv)
#function to find closest color from the image to the csv
def getcolorname(R,G,B):
    min = 10000
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
        if(d<=min):
            min = d
            color_iden = csv.loc[i,"color_name"]
    return color_iden
#to get x,y pos of image
def draw_image(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b,g,r,xpos,ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b,g,r = img[y,x]
        b = int(b)
        g = int(g)
        r = int(r)

cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_image)

while(True):
    cv2.imshow("image",img)
    if (clicked):
        cv2.rectangle(img,(20,20), (500,60), (b,g,r), -1)
        text = getcolorname(r,g,b) + ' R='+ str(r) +  ' G='+ str(g) +  ' B='+ str(b)
        cv2.putText(img, text,(50,50),2,0.8,(255,255,255),2,cv2.LINE_AA)
        if(r+g+b>=600):#For very light colours we will display text in black colour
            cv2.putText(img, text,(50,50),2,0.8,(0,0,0),2,cv2.LINE_AA)
        clicked=False

    #Break the loop when user hits 'enter' key
    if cv2.waitKey(20) & keyboard.is_pressed('enter'):
        break
cv2.destroyAllWindows()