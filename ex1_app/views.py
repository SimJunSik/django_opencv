from django.shortcuts import render
import cv2
from rest_framework import viewsets
from django.http import JsonResponse
from rest_framework.response import Response
from .models import *
from .serializers import *
# Create your views here.

def index(request) :

	data = {
		'test' : 1,
		'test2' : 2,
	}

	#return render(request, "./home.html")
	return JsonResponse(data)





def opencv(request) :

	try :
		print('카메라를 구동합니다.')
		cap = cv2.VideoCapture(0)

	except :
		print('카메라 구동 실패')
		return

	cap.set(3,480)
	cap.set(4,320)

	while True:
		ret, frame = cap.read()

		if not ret :
			print('읽기 오류')
			break

		cv2.imshow('cam', frame)
		k = cv2.waitKey(1) & 0xFF
		if k == 27 :
			break

	cap.release()
	cv2.destroyAllWindows()

	return render(request, "./home.html")


class VersionViewSet(viewsets.ModelViewSet):
	queryset = Version.objects.all()
	serializer_class = VersionSerializer

	def list(self, request, *args, **kwargs):
		"""
		result = {}
		versions = Version.objects.filter(osType='android')
		cnt = 0
		for version in versions :
			cnt += 1
			result_tmp = {}
			result_tmp['result'] = 200
			result_tmp['osType'] = version.osType
			result_tmp['version'] = version.version
			result[str(cnt)] = result_tmp
		return JsonResponse(result)
		"""
		versions = Version.objects.filter(osType='android')
		serializer = VersionSerializer(versions, many=True)
		#return JSONResponse(serializer.data)
		response_data={"success": "1"}
		return JSONResponse(response_data)

	def create(self, request, *args, **kwargs):

		print(request.data['version'])
		version = request.data['version']
		new_version = Version(version=version)
		new_version.save()

		response_data={"success": "1"}
		return JSONResponse(response_data)



class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	def list(self, request, *args, **kwargs):
		"""
		result = {}
		versions = Version.objects.filter(osType='android')
		cnt = 0
		for version in versions :
			cnt += 1
			result_tmp = {}
			result_tmp['result'] = 200
			result_tmp['osType'] = version.osType
			result_tmp['version'] = version.version
			result[str(cnt)] = result_tmp
		return JsonResponse(result)
		"""
		users = User.objects.all()
		print(users)
		serializer = UserSerializer(users, many=True)
		return JSONResponse(serializer.data)

	def create(self, request, *args, **kwargs):
		#print(request.data['user_id'])
		#user = request.data['users']
		user_id = request.data['user_id']
		user_psw = request.data['user_psw']

		users = User.objects.all()

		id_lst = []
		for user in users :
			id_lst.append(user.user_id)

		
		if user_id in id_lst :
			response_data={"success": 0}
		else :
			new_user = User(user_id = user_id, user_psw = user_psw)
			new_user.save()
			response_data={"success": 1}
		
		return JSONResponse(response_data)

#from rest_framework.viewsets import GenericViewSet
#from drf_multiple_model.mixins import MultipleModelMixin

import simplejson as json
from PIL import Image
import scipy.misc as smp
import numpy as np
import random as r
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from braces.views import CsrfExemptMixin
from django.utils.decorators import method_decorator
import zlib
import os

class GetframeViewSet(viewsets.ModelViewSet) :
	queryset = Thumbnail.objects.all()
	serializer_class = ThumbnailSerializer

	def create(self, request, *args, **kwargs):

		#print(request.data['idx'])
		thumbnail_id = int(request.data['thumbnail_id'])
		print(thumbnail_id)
		thumbnail_tmp = Thumbnail.objects.get(thumbnail_id = thumbnail_id)
		print(thumbnail_tmp.video.url)
		try :
			print('카메라를 구동합니다.')
			cap = cv2.VideoCapture('.' + thumbnail_tmp.video.url)

		except :
			print('카메라 구동 실패')
			return

		cap.set(cv2.CAP_PROP_FPS, 20)
		myFrameNumber = int(request.data['idx'])
		print("myFN =", myFrameNumber)
		frames = []
		size = 400

		# get total number of frames
		#totalFrames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
		cap.set(cv2.CAP_PROP_POS_AVI_RATIO,1)
		num_frames = cap.get(cv2.CAP_PROP_POS_FRAMES)
		fps = cap.get(cv2.CAP_PROP_FPS)
		duration = int(float(num_frames) / float(fps))
		totalFrames = duration * round(fps)

		# check for valid frame number
		if myFrameNumber >= 0 and myFrameNumber <= totalFrames:
		    # set frame position
		    cap.set(cv2.CAP_PROP_POS_FRAMES,myFrameNumber)

		if totalFrames < (myFrameNumber + 90) :
			print(totalFrames)
			print(myFrameNumber)
			print(int(totalFrames - myFrameNumber - 1)*1)
			for i in range(0,int(totalFrames - myFrameNumber - 1)*1) :
				ret, frame = cap.read()
				frame = cv2.resize(frame, (size, size))
				frames.append(frame)

		else :
			for i in range(0,90*1) :
				ret, frame = cap.read()
				frame = cv2.resize(frame, (size, size))
				frames.append(frame)

		frame_byte_list = []
		frame_byte = []
		#print(frame[:,:,:])


		#print ("0x%0.4X" % ((int(red / 255 * 31) << 11) | (int(green / 255 * 63) << 5) | (int(blue / 255 * 31))))
		"""
		for frame in frames :
			frame_byte = []
			for i in range(0,size) :
				for f in frame[i] :
					frame_byte.append(f[2])
					frame_byte.append(f[1])
					frame_byte.append(f[0])
					frame_byte.append(-1)
			frame_byte_list.append(str(frame_byte))
		"""





		"""
		for frame in frames :
			tmp = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			_, alpha = cv2.threshold(tmp, 0, 255, cv2.THRESH_BINARY)
			b, g, r = cv2.split(frame)
			rgba = [r, g, b, alpha]
			dst = cv2.merge(rgba, 4)
			#print(dst.shape)
			#cv2.imshow('a',frame)
			#cv2.waitKey(0)
			compressed_data = zlib.compress(dst)
			#print(frame)
			abc = zlib.decompress(compressed_data)
			abc = abc.hex()
			#print(len(str(abc)))
			#frame_byte_list.append(str(abc)[2:].replace('\\',''))
			frame_byte_list.append(str(abc))
		"""


	
		for frame in frames :
			"""
			tmp = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			_, alpha = cv2.threshold(tmp, 0, 255, cv2.THRESH_BINARY)
			b, g, r = cv2.split(frame)
			rgba = [r, g, b, alpha]
			dst = cv2.merge(rgba, 4)
			"""

			
			b, g, r = cv2.split(frame)
			rgba = [r, g, b]
			dst = cv2.merge(rgba, 3)
			
			encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 80]
			ret, jpeg = cv2.imencode('.jpg',dst,encode_param)

			frame_byte_list.append(str(jpeg.tobytes().hex()))



		
		print("finish")
		result = { 'frame' : frame_byte_list }
		#print(result)

		return JSONResponse(result)



class ThumbnailViewSet(viewsets.ModelViewSet) :
	queryset = Thumbnail.objects.all()
	serializer_class = ThumbnailSerializer

	def list(self, request, *args, **kwargs):
		try :
			print('카메라를 구동합니다.')
			cap = cv2.VideoCapture('./media/dog2.mp4')

		except :
			print('카메라 구동 실패')
			return

		myFrameNumber = r.randint(10,100)
		print("myFN =", myFrameNumber)
		frames = []
		size = 100

		# get total number of frames
		totalFrames = cap.get(cv2.CAP_PROP_FRAME_COUNT)

		# check for valid frame number
		if myFrameNumber >= 0 & myFrameNumber <= totalFrames:
		    # set frame position
		    cap.set(cv2.CAP_PROP_POS_FRAMES,myFrameNumber)

		for i in range(0,5) :
			print(i)
			ret, frame = cap.read()
			frame = cv2.resize(frame, (size, size))
			frames.append(frame)

		frame_byte_list = []
		frame_byte = []
		#print(frame[:,:,:])
		for frame in frames :
			frame_byte = []
			for i in range(0,size) :
				for f in frame[i] :
					frame_byte.append(f[2])
					frame_byte.append(f[1])
					frame_byte.append(f[0])
					frame_byte.append(-1)
			frame_byte_list.append(frame_byte)

		#print(frame_byte)
		#print(len(frame_byte))

		print("finish")
		result = { 'frame' : frame_byte_list }
		#print(result)

		return JSONResponse(result)

	def create(self, request, *args, **kwargs) :
		#print(request.data)
		bmp = request.data['bmp']
		user_id = request.data['user_id']
		print(user_id)

		#print(bmp)

		#new_thumbnail = Thumbnail(bytes_list = bmp)




		#jsonDec = json.decoder.JSONDecoder()
		#myPythonList = jsonDec.decode(new_thumbnail.bytes_list)
		#print(new_thumbnail.bytes_list['mBuffer'])
		"""
		for i in range(len(new_thumbnail.bytes_list['mBuffer'])) :
			if i%2==1 :
				print(new_thumbnail.bytes_list['mBuffer'][i])
		"""
		

		#print(type(new_thumbnail.bytes_list))
		#print(new_thumbnail.bytes_list['mBuffer'][0:200])
		#image_data = new_thumbnail.bytes_list
		#image = Image.frombytes('RGBA', (128,128), image_data)


		new_img = []
		cnt = 1
		for p in bmp :
			if cnt%4!=0 :
				new_img.append(p)
			cnt += 1



		"""
		img = Image.new('RGB', (50, 50))
		img.putdata(new_img)
		img.save('my.png')
		img.show()
		"""

		# Create a 1024x1024x3 array of 8 bit unsigned integers

		size = 200
		data = np.zeros( (size,size,3), dtype=np.uint8 )
		w = 0
		h = 0
		for i in range(0,len(new_img)-3,3) :
			data[w,h] = [new_img[i],new_img[i+1],new_img[i+2]]
			if w==(size-1):
				h += 1
			w = (w+1)%size


		#print(data)

		#data[512,512] = [254,0,0]       # Makes the middle pixel red
		#data[512,513] = [0,0,255]       # Makes the next pixel blue

		img = smp.toimage(data)     # Create a PIL image
		img = img.rotate(270)
		img = img.transpose(Image.FLIP_LEFT_RIGHT)

		
		#img.show()
		#img.save('./media/test.png')
		img.save('./media/' + user_id + '.png')

		thumbnail_list = Thumbnail.objects.all()
		max_id = 0
		max_ssim = 0
		max_flann = 0

		for thumbnail in thumbnail_list :
			#print('.' + thumbnail.img.url)
			img_cv = cv2.imread('./media/' + user_id + '.png', cv2.IMREAD_GRAYSCALE)
			thumbnail_cv = cv2.imread('.' + thumbnail.img.url, cv2.IMREAD_GRAYSCALE)
			thumbnail_cv = cv2.resize(thumbnail_cv, (200,200))
			

			res = None
			sift = cv2.xfeatures2d.SIFT_create()
			kp1, des1 = sift.detectAndCompute(img_cv, None)
			kp2, des2 = sift.detectAndCompute(thumbnail_cv, None)

			FLANN_INDEX_KDTREE = 0
			index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
			search_params = dict(checks = 50)

			flann = cv2.FlannBasedMatcher(index_params,search_params)
			matches = flann.knnMatch(des1, des2, k = 2)

			good = []
			for m,n in matches :
			    if m.distance < 0.7*n.distance :
			        good.append(m)


			if (compare_ssim(img_cv,thumbnail_cv) >= max_ssim) and (len(good) >= max_flann) :
				max_ssim = compare_ssim(img_cv,thumbnail_cv)
				max_flann = len(good)
				max_id = thumbnail.thumbnail_id
				
			print(thumbnail.img.url + "   " + str(compare_ssim(img_cv,thumbnail_cv)))

			#res = cv2.drawMatches(img1, kp1, img2, kp2, good, res, flags=2)
			#matches = sorted(matches, key = lambda  x:x.distance)
			#Qres = cv2.drawMatches(img1, kp1, img2, kp2, matches[:30], res, flags=0)
			print("          " + str(len(good)))


		try :
			#os.remove('./media/' + user_id + '.png')
			pass
		except :
			pass

		#print(Thumbnail.objects.get(thumbnail_id = max_id).video.url)
		v = cv2.VideoCapture('.' + Thumbnail.objects.get(thumbnail_id = max_id).video.url)
		v.set(cv2.CAP_PROP_POS_AVI_RATIO,1)
		num_frames = v.get(cv2.CAP_PROP_POS_FRAMES)
		fps = v.get(cv2.CAP_PROP_FPS)
		duration = int(float(num_frames) / float(fps))
		print(fps)
		print("duration=",duration)
		total_sec = duration
		duration = duration * round(fps)


		#new_thumbnail.save()
		if max_ssim > 0.4 or max_flann >= 10 :
			response_data = {"success" : "1", "max_id" : max_id, "duration" : duration, "total_sec" : total_sec}
		else :
			response_data = {"success" : "0", "max_id" : max_id, "duration" : duration, "total_sec" : total_sec}
		return JSONResponse(response_data)




from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from .serializers import TestSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
from django.contrib.staticfiles.templatetags.staticfiles import static


class JSONResponse(HttpResponse):

    

    def __init__(self, data, **kwargs):

        content = JSONRenderer().render(data, 'application/json; indent=4')

        kwargs['content_type'] = 'application/json'

        super(JSONResponse, self).__init__(content, **kwargs)



def video_get_frame(request) :

	try :
		print('카메라를 구동합니다.')
		cap = cv2.VideoCapture('./media/dog2.mp4')

	except :
		print('카메라 구동 실패')
		return

	myFrameNumber = 20

	# get total number of frames
	totalFrames = cap.get(cv2.CAP_PROP_FRAME_COUNT)

	# check for valid frame number
	if myFrameNumber >= 0 & myFrameNumber <= totalFrames:
	    # set frame position
	    cap.set(cv2.CAP_PROP_POS_FRAMES,myFrameNumber)

	ret, frame = cap.read()
	frame = cv2.resize(frame, (200, 200))
	#print(frame)
	#cv2.imshow("Video", frame)
	#cv2.waitKey()

	frame_list = []
	result = {}
	"""
	for i in range(0,10) :
	    ret, frame = cap.read()
	    frame = cv2.resize(frame, (200, 200))
	    result['frame' + str(i)] = frame
	    #frame_list.append(frame)
	    
	    cv2.imshow("Video", frame)
	    if cv2.waitKey(20) & 0xFF == ord('q'):
	        break
	"""

	result = { 'frame' : frame }


	return JSONResponse(result)




from skimage.measure import compare_ssim

def thumbnail_compare(request) :

	thumbnail_list = Thumbnail.objects.all()

	for thumbnail in thumbnail_list :

		print(compare_ssim(img1,thumbnail))




	result = { 'success' : '1'}

	return JSONResponse(result)










@api_view(['GET','POST'])

def test_list(request, format=None):

    

    if request.method == 'GET':

        packages = TestModel.objects.all()

        serializer = TestSerializer(packages, many=True)

        return JSONResponse(serializer.data)


@csrf_exempt 
def version_list(request, format=None):

    if request.method == 'GET':
    	packages = Version.objects.all()
    	serializer = VersionSerializer(packages, many=True)
    	return JSONResponse(serializer.data)

    if request.method=='POST':
    	print(request.POST)
    	"""
    	image = request.FILES['photo']
    	title1 =''
    	new_image = Photo(file=image,description=title1)
    	new_image.save()
    	"""

    	response_data={"success": "1"}
    	return JSONResponse(response_data)





@csrf_exempt
def thumbnail_call(request) :

	if request.method == 'POST' :
		print("!!!!!")
		print(request.data['bmp'])

		response_data = {"success", "1"}
		return JSONResponse(response_data)










from django.shortcuts import render
from django.http import HttpResponse,StreamingHttpResponse
import cv2
import time
from django.views.decorators import gzip

class VideoCamera(object):
    def __init__(self):
    	self.video = cv2.VideoCapture('./media/Lou_Clip_-_Pixar_Short_Film.mp4')
    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret,image = self.video.read()
        ret,jpeg = cv2.imencode('.jpg',image)
        print(len(image.tobytes().hex()),len(jpeg.tobytes().hex()))
        return jpeg.tobytes()

def gen(camera):
	cnt = 0
	while True:
		if cnt == 900 :
			break
		cnt += 1
		frame = camera.get_frame()
		#print(frame)
		#frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		#frame = cv2.resize(frame, (200,200))
		yield(b'--frame\r\n'
			b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

#@gzip.gzip_page
def stream_test(request): 
    try:
    	response = StreamingHttpResponse(gen(VideoCamera()),content_type="multipart/x-mixed-replace;boundary=frame")
    	print(response)
    	return response
    except HttpResponseServerError as e:
        print("aborted")



class GetframeViewSet2(viewsets.ModelViewSet) :
	queryset = Thumbnail.objects.all()
	serializer_class = ThumbnailSerializer

	def create(self, request, *args, **kwargs):

		try:
			response = StreamingHttpResponse(gen(VideoCamera()),content_type="multipart/x-mixed-replace;boundary=frame")
			print(response)
			return response
		except HttpResponseServerError as e:
			print("aborted")