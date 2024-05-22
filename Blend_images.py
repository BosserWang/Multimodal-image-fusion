import cv2

def blend_images(infrared_path, visible_path, alpha=0.5):
    # 读取红外线图片和可见光图片
    infrared_img = cv2.imread(infrared_path)
    visible_img = cv2.imread(visible_path)

    # 融合图片
    blended_img = cv2.addWeighted(infrared_img, alpha, visible_img, 1-alpha, 0)

    # 显示融合后的图片
    # cv2.imshow('Blended Image', blended_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # 保存融合后的图片
    cv2.imwrite('process/blended_image.png', blended_img)

def Blend_main(filename):
    infrared_path = 'images/Infrared/'+filename
    visible_path = 'images/Visible/'+filename
    blend_images(infrared_path, visible_path)
