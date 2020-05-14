import cv2
import numpy as np
import mapper
from PIL import Image
def scan(number_of_images):
    need = number_of_images
    img_list = []
    for i in range(need):
        a = input('Enter name of img file')
        image=cv2.imread(a)   #read in the image
        #image=cv2.resize(image,(1200,800)) #resizing because opencv does not work well with bigger images
        orig=image.copy()

        gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)  #RGB To Gray Scale
        cv2.imshow("Title",gray)
        cv2.waitKey(2000)

        blurred=cv2.GaussianBlur(gray,(5,5),0)  #(5,5) is the kernel size and 0 is sigma that determines the amount of blur
        cv2.imshow("Blur",blurred)
        cv2.waitKey(2000)
        edged=cv2.Canny(blurred,10,60)  #30 MinThreshold and 50 is the MaxThreshold
        cv2.imshow("Canny",edged)
        cv2.waitKey(2000)

        contours,hierarchy=cv2.findContours(edged,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)  #retrieve the contours as a list, with simple apprximation model
        contours=sorted(contours,key=cv2.contourArea,reverse=True)

        #the loop extracts the boundary contours of the page
        for c in contours:
            p=cv2.arcLength(c,True)
            approx=cv2.approxPolyDP(c,0.02*p,True)

            if len(approx)==4:        
                target=approx
                break
        approx=mapper.mapp(target) #find endpoints of the sheet

        pts=np.float32([[0,0],[120,0],[120,120],[0,120]])  #map to 800*800 target window

        op=cv2.getPerspectiveTransform(approx,pts)  #get the top or bird eye view effect
        dst=cv2.warpPerspective(orig,op,(800,800))


        cv2.imshow("Scanned",dst)
        cv2.waitKey(2000)
        dimensions = dst.shape
        saving = cv2.imwrite('/home/hemanth/Desktop/Hackathon/primary'+str(i)+'.'+'jpg',dst)
        print(dimensions)
        cv2.destroyAllWindows()
        new_name = 'primary'+str(i)+'.jpg'
        img_list.append(new_name) 
   
    imager = []
    for j in range(need-1):
        naming = '/home/hemanth/Desktop/Hackathon/primary'+str(j)+'.jpg'
        con = Image.open(naming)
        im1 = con.convert('RGB')
        imager.append(im1)
    pdf_name = '/home/hemanth/Desktop/Hackathon/seconds.pdf'
    im1.save(pdf_name,save_all=True, append_images=imager)    

                
take = int(input('Enter Number Of Images'))
scan(take)
