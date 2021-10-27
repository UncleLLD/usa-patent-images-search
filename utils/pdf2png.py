import sys
import fitz
import os
import datetime
 
def pyMuPDF_fitz(pdfPath, imagePath):
    startTime_pdf2img = datetime.datetime.now()  # 开始时间
    
    print("imagePath="+imagePath)
    pdfDoc = fitz.open(pdfPath)
    for pg in range(pdfDoc.pageCount):
        page = pdfDoc[pg]
        rotate = int(0)
        # 每个尺寸的缩放系数为1.3，这将为我们生成分辨率提高2.6的图像。
        # 此处若是不做设置，默认图片大小为：792X612, dpi=72
        zoom_x = 1.33333333 #(1.33333333-->1056x816)   (2-->1584x1224)
        zoom_y = 1.33333333
        mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
        pix = page.getPixmap(matrix=mat, alpha=False)
        
        if not os.path.exists(imagePath):#判断存放图片的文件夹是否存在
            os.makedirs(imagePath) # 若图片文件夹不存在就创建
        
        pix.writePNG(imagePath+'/'+'images_%s.png' % pg)  # 将图片写入指定的文件夹内
        
    endTime_pdf2img = datetime.datetime.now() # 结束时间
    print('pdf2img时间=',(endTime_pdf2img - startTime_pdf2img).seconds)
 
 
if __name__ == "__main__":
    pdf_paths = sys.argv[1]
    # single pdf file
    imagePath = sys.argv[2]
    pyMuPDF_fitz(pdfPath, imagePath)
    
    # pdf list file
    with open(pdf_paths) as f:
        for ln in f:
            pdf_path = ln.rstrip('\n')
            pdf_name = pdf_path.split('.')[0]
            save_path = './convert-pdf/' + pdf_name
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            pyMuPDF_fitz('./patent-pdf/'+pdf_path, save_path)