import cv2
import numpy as np

class image_recognition:
    
    def __init__(self):
        self.data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        self.matrix = np.load('utils/abc.npy')
        self.width = int(open('utils/Resolution.txt').read().split('\n')[0])
        self.height = int(open('utils/Resolution.txt').read().split('\n')[1])
        self.area = int(open('utils/Resolution.txt').read().split('\n')[2])
        self.realwidth = float(open('utils/Resolution.txt').read().split('\n')[3])
        self.realheight = float(open('utils/Resolution.txt').read().split('\n')[4])
        self.diff_low_t= int(open('utils/Resolution.txt').read().split('\n')[5])
        self.diff_high_t= int(open('utils/Resolution.txt').read().split('\n')[6])
        self.nhan = open('utils/nhan.txt').read().split('\n')
    def crop_anh(self,anh_nen,anh_phat_hien):
        crop_nen     = cv2.warpPerspective(anh_nen, self.matrix, (self.width, self.height))
        crop_phat_hien = cv2.warpPerspective(anh_phat_hien, self.matrix, (self.width, self.height))
        return crop_nen, crop_phat_hien
    
    def chay_phat_hien(self, anh_nen, anh_phat_hien,model):
        crop_nen, crop_phat_hien = self.crop_anh(anh_nen,anh_phat_hien)
        ket_qua, anh = self.phat_hien(crop_nen, crop_phat_hien,model)
        return ket_qua, anh
    
    def get_label(self):
        label = []
        file1 = open("utils/labels.txt","r")
        arr = file1.read().split('\n')
        for i in range(len(arr)):
            label.append(arr[i][2:])
        label.pop()
        with open('utils/nhan.txt', "w") as myfile:
            for i in range(len(label)):
                myfile.write(label[i] + '\n') 
                
    def phat_hien(self,anh_nen_crop, anh_phat_hien_crop,model):
        
        # Phát hiện vật thể
        target_gray = cv2.cvtColor(anh_phat_hien_crop, cv2.COLOR_BGR2GRAY)
        bg_gray = cv2.cvtColor(anh_nen_crop, cv2.COLOR_BGR2GRAY)
        diff_gray = cv2.absdiff(target_gray,bg_gray)
        diff_gray_blur = cv2.GaussianBlur(diff_gray,(5,5),0)
        ret,diff_tresh = cv2.threshold(diff_gray_blur,self.diff_low_t,self.diff_high_t,cv2.THRESH_BINARY)
        diff = cv2.GaussianBlur(diff_tresh,(5,5),0)
        contours, hierarchy = cv2.findContours(diff, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        
        # Phân loại vật thể
        ket_qua = []
        for cnt in contours:
            (x, y, w, h) = cv2.boundingRect(cnt)
            
            (a,b,c,d) = (x, y, w, h)
            area = w*h
            edge_noise=False
            if x==0:
                edge_noise=True
            if y==0:
                edge_noise=True
            if (x+w)== self.width:
                edge_noise=True
            if (y+h)== self.height:
                edge_noise=True

            if edge_noise==False:
                if area > self.area:
                    realx = (self.realwidth/self.width)*(x + (w/2))
                    realy = (self.realheight/self.height)*(y + (h/2))
                    #draw a circle at the center of object x,y,w,h
                    cv2.circle(anh_phat_hien_crop,(int((x + (w/2))),int((y + (h/2)))),5,(0,0,255),-1)
                    adjust=0.1
                    y=int(y-((h*adjust)/2))
                    if y<0:
                        y=0
                    x=int(x-((w*adjust)/2))
                    if x<0:
                        x=0
                    w=int(w*(1+adjust))
                    h=int(h*(1+adjust))
                    if y<0: y=0
                    if x<0: x=0
                    if (x+w)>self.width: w=self.width-x
                    if (y+h)>self.height: h=self.height-y
                    if w>h:
                        #ensure contour is centered
                        y=int(y-((w-h)/2))
                        if y<0: y=0
                        #make a square
                        h=w
                        if (y+h)>self.height: y=self.height-h
                    if h>w:
                        x=int(x-((h-w)/2))
                        if x<0: x=0
                        w=h
                        if (x+w)>self.width: x=self.width-w
                        
                        
                    crop_img = anh_phat_hien_crop[y:y+h, x:x+w]
                    cv2.rectangle(anh_phat_hien_crop, (a, b), (a + c, b + d), (0, 0, 255), 2)
                    image = cv2.cvtColor(crop_img, cv2.COLOR_BGR2RGB)
                    img = cv2.resize(image,(224, 224))
                    image_array = np.asarray(img)
                    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
                    self.data[0] = normalized_image_array
                    prediction = model.predict(self.data)
                    index_max = np.argmax(prediction)
                    Gia_tri_max = prediction[0][index_max]
                    if Gia_tri_max > 0.8:
                        ket_qua.append([realx,realy,index_max])
                        cv2.putText(anh_phat_hien_crop, self.nhan[index_max], (a, b-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (36,255,12), 2)
                        cv2.putText(anh_phat_hien_crop, 'cx, cy: '+ str(round(realx,2))+ ', '+str(round(realy,2)), (a-10, b+d+20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (36,255,12), 2)
                        cv2.putText(anh_phat_hien_crop, str(round(Gia_tri_max*100,2))+'%', (a+c-50, b-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (36,255,12), 2)
                    else:
                        ket_qua.append([round(realx,2),round(realy,2),len(self.nhan)-1])
                        cv2.putText(anh_phat_hien_crop, 'chua xac dinh', (a, b-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (36,255,12), 2)
                        cv2.putText(anh_phat_hien_crop, 'cx, cy: '+ str(round(realx,2))+ ', '+str(round(realy,2)), (a-10, b+d+20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (36,255,12), 2)
                        cv2.putText(anh_phat_hien_crop, str(round(Gia_tri_max*100,2))+'%' + ' index of: ' + str(index_max), (a+c-50, b-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (36,255,12), 2)

        return ket_qua, anh_phat_hien_crop