from hudescriptor import huDescriptor
from colordescriptor import ColorDescriptor
import glob
import cv2
import os

hu = huDescriptor()
cd = ColorDescriptor((8, 12, 3))

huOutput = open("conf/huFeatures.csv", "w")
colorOutput = open("conf/colorFeatures.csv", "w")

for imagePath in glob.glob("static/datasets/*"):
    imageID = os.path.basename(imagePath)
    image = cv2.imread(imagePath)

    hufeatures = hu.huMoments(image)
    colorFeatures = cd.describe(image)

    hufeatures = [str(abs(float(f))) for f in hufeatures]
    colorFeatures = [str(float(cf)) for cf in colorFeatures]
    
    huOutput.write("%s,%s\n" % (imageID, ",".join(hufeatures)))
    colorOutput.write("%s,%s\n" % (imageID, ",".join(colorFeatures)))

huOutput.close()
colorOutput.close()

print("Configuracion realizada")
