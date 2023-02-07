import numpy as np
import cv2
import os
import shutil
import time
from flask import Flask, make_response, render_template, request, redirect
from hudescriptor import huDescriptor
from colordescriptor import ColorDescriptor
from retrieval import retrieval
from paste.translogger import TransLogger
from waitress import serve

hu = huDescriptor()
cd = ColorDescriptor((8, 12, 3))
rt = retrieval()
cantidadARecuperar=10
puntajeMinimo=0.7

app = Flask(__name__)

@app.route('/')
def inicio():
	if os.path.exists('static/temp') == True :
		shutil.rmtree('static/temp')
		shutil.rmtree('static/tmp')
		return redirect('/home')
	else :
		return redirect('/home')

@app.route('/home')
def home():
	datasets = os.listdir('static/datasets')
	if os.path.exists('static/temp') == True and os.path.getsize('static/temp') != 0:
		image_names = os.listdir('static/temp')
		nearest = sorted(os.listdir('static/temp'),reverse=True)[0]
		target = os.listdir('static/tmp')
		return render_template("index.html", image_names=sorted(image_names, reverse=True),\
		target=(target), page_status=1, count=len(datasets), nearest=(nearest))
	else :
		return render_template("index.html", page_status=2, count=len(datasets))

@app.route('/search', methods=['POST'])
def search():

	if request.method == 'POST':
		file = request.files['image']
		reading = file.read()
		extract = np.frombuffer(reading, np.uint8)
		image = cv2.imdecode(extract, cv2.IMREAD_COLOR)

		if not(os.path.exists('static/temp')):
			os.makedirs('static/temp')
			os.makedirs('static/tmp')

		results = rt.compare(image , cantidadARecuperar)

		i = 1
		for (score, resultID) in results:
			i += 1
			score = 1 - score
			if (score > puntajeMinimo):
				result = cv2.imread("static/datasets/" + resultID)
				saveimg = cv2.imwrite("static/temp/" + str(score)+str(i) + ".jpeg", result)

		imgstr = time.strftime("%Y%m%d-%H%M%S")
		cv2.imwrite("static/tmp/"+ imgstr +".jpeg", image)

	return redirect("/home")

if __name__ == '__main__':
	serve(TransLogger(app, setup_console_handler=False), host="0.0.0.0", port=5000)





