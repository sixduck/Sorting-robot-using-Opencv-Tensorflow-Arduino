x=1
y=2
z=3


# # 1s or less
# diff_low_t=35
# diff_high_t=255
# target_gray = cv2.cvtColor(anh_phat_hien_crop, cv2.COLOR_BGR2GRAY)
# self.previewImage('a', target_gray)
# bg_gray = cv2.cvtColor(anh_nen_crop, cv2.COLOR_BGR2GRAY)
# self.previewImage('a', bg_gray)
# diff_gray = cv2.absdiff(target_gray,bg_gray)
# self.previewImage('a', diff_gray)
# diff_gray_blur = cv2.GaussianBlur(diff_gray,(5,5),0)
# self.previewImage('a', diff_gray_blur)
# ret,diff_tresh = cv2.threshold(diff_gray_blur,diff_low_t,diff_high_t,cv2.THRESH_BINARY)
# self.previewImage('a', diff_tresh)
# diff = cv2.GaussianBlur(diff_tresh,(5,5),0)
# self.previewImage('a', diff)
# contours, hierarchy = cv2.findContours(diff, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)



# # 1s
# bg_low_t=255
# bg_high_t=255
# img_low_t=60
# img_high_t=255
# background_img_gray=cv2.cvtColor(anh_nen_crop, cv2.COLOR_BGR2GRAY)
# self.previewImage("1 Background Gray",background_img_gray)
# background_img_blur = cv2.GaussianBlur(background_img_gray,(5,5),0)
# self.previewImage("2 Background Blur Gray",background_img_blur)       
# ret,background_img_tresh = cv2.threshold(background_img_blur,bg_low_t,bg_high_t,cv2.THRESH_BINARY_INV)
# self.previewImage("3 Background Treshold",background_img_tresh)
# img_gray=cv2.cvtColor(anh_phat_hien_crop, cv2.COLOR_BGR2GRAY)
# self.previewImage("4 Image Gray",img_gray)
# img_blur = cv2.GaussianBlur(img_gray,(5,5),0)
# self.previewImage("5 Image Blur Gray",img_blur)
# ret,img_tresh = cv2.threshold(img_blur,img_low_t,img_high_t,cv2.THRESH_BINARY_INV)
# self.previewImage("6 Image Treshold",img_tresh)
# diff=cv2.absdiff(background_img_tresh,img_tresh)
# self.previewImage("7 Diff",diff)  
# contours, hierarchy = cv2.findContours(diff, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)           





# # 1.3s
# blur_bg = cv2.GaussianBlur(anh_nen_crop, (21, 21), 0)
# blur_target = cv2.GaussianBlur(anh_phat_hien_crop, (21, 21), 0)
# self.previewImage('anh_mo', blur_bg)
# self.previewImage('anh_phat_hien_mo', blur_target)
# gray_target = cv2.cvtColor(blur_target,cv2.COLOR_BGR2GRAY)
# gray_bg = cv2.cvtColor(blur_bg,cv2.COLOR_BGR2GRAY)
# frameDelta = cv2.absdiff(blur_bg,blur_target)
# self.previewImage('khac_biet', frameDelta) 
# gray_result = cv2.cvtColor(frameDelta, cv2.COLOR_BGR2GRAY)
# self.previewImage('den_trang', gray_result)        
# _, threshold = cv2.threshold(gray_result, 40, 255, cv2.THRESH_BINARY)
# thresh = cv2.dilate(threshold, None, iterations=2)
# self.previewImage('contour', thresh)
# contours,_ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        
        
        
        
        
        
        
        
        
# 1s or less
# diff_low_t=35
# diff_high_t=255
# target_gray = cv2.cvtColor(crop_phat_hien, cv2.COLOR_BGR2GRAY)
# previewImage('a', target_gray)
# bg_gray = cv2.cvtColor(crop_nen, cv2.COLOR_BGR2GRAY)
# previewImage('a', bg_gray)
# diff_gray = cv2.absdiff(target_gray,bg_gray)
# previewImage('a', diff_gray)
# diff_gray_blur = cv2.GaussianBlur(diff_gray,(5,5),0)
# previewImage('a', diff_gray_blur)
# ret,diff_tresh = cv2.threshold(diff_gray_blur,diff_low_t,diff_high_t,cv2.THRESH_BINARY)
# previewImage('a', diff_tresh)
# diff = cv2.GaussianBlur(diff_tresh,(5,5),0)
# previewImage('a', diff)
# contours, hierarchy = cv2.findContours(diff, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
# # contours, hierarchy = cv2.findContours(diff, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)




# 1s
# bg_low_t=255
# bg_high_t=255
# img_low_t=60
# img_high_t=255
# background_img_gray=cv2.cvtColor(crop_nen , cv2.COLOR_BGR2GRAY)
# previewImage("1 Background Gray",background_img_gray)
# background_img_blur = cv2.GaussianBlur(background_img_gray,(5,5),0)
# previewImage("2 Background Blur Gray",background_img_blur)       
# ret,background_img_tresh = cv2.threshold(background_img_blur,bg_low_t,bg_high_t,cv2.THRESH_BINARY_INV)
# previewImage("3 Background Treshold",background_img_tresh)
# img_gray=cv2.cvtColor(crop_phat_hien, cv2.COLOR_BGR2GRAY)
# previewImage("4 Image Gray",img_gray)
# img_blur = cv2.GaussianBlur(img_gray,(5,5),0)
# previewImage("5 Image Blur Gray",img_blur)
# ret,img_tresh = cv2.threshold(img_blur,img_low_t,img_high_t,cv2.THRESH_BINARY_INV)
# previewImage("6 Image Treshold",img_tresh)
# diff=cv2.absdiff(background_img_tresh,img_tresh)
# previewImage("7 Diff",diff)    
# contours, hierarchy = cv2.findContours(diff, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)




# 1.3s
# blur_bg = cv2.GaussianBlur(crop_nen, (21, 21), 0)
# blur_target = cv2.GaussianBlur(crop_phat_hien, (21, 21), 0)
# previewImage('anh_mo', blur_bg)
# previewImage('anh_phat_hien_mo', blur_target)
# gray_target = cv2.cvtColor(blur_target,cv2.COLOR_BGR2GRAY)
# gray_bg = cv2.cvtColor(blur_bg,cv2.COLOR_BGR2GRAY)
# frameDelta = cv2.absdiff(blur_bg,blur_target)
# previewImage('khac_biet', frameDelta)
# gray_result = cv2.cvtColor(frameDelta, cv2.COLOR_BGR2GRAY)
# previewImage('den_trang', gray_result)        
# _, threshold = cv2.threshold(gray_result, 40, 255, cv2.THRESH_BINARY)
# thresh = cv2.dilate(threshold, None, iterations=2)
# previewImage('contour', thresh)
# contours,_ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)