# ultrasonic sensor test
###################################
import RPi.GPIO as GPIO
import time

import requests
from requests.structures import CaseInsensitiveDict
import datetime

makerobo_TRIG = 3  
makerobo_ECHO = 5  


bin_height = 38
time_between_scans = 5



def makerobo_setup():
	GPIO.setmode(GPIO.BOARD)      
	GPIO.setwarnings(False)       
	GPIO.setup(makerobo_TRIG, GPIO.OUT) 
	GPIO.setup(makerobo_ECHO, GPIO.IN)  


def ur_disMeasure():
	GPIO.output(makerobo_TRIG, 0)  
	time.sleep(0.000002)           
	# print("after a quick nap")

	GPIO.output(makerobo_TRIG, 1)  
	time.sleep(0.00001)            
	GPIO.output(makerobo_TRIG, 0)      
	# print("after a second nap")
  
	while GPIO.input(makerobo_ECHO) == 0: 
		us_a = 0
		# print("lost in and endless loop 1")
	us_time1 = time.time()                
	while GPIO.input(makerobo_ECHO) == 1: 
		us_a = 1
		# print("lost in and endless loop 2")
	us_time2 = time.time()               

	us_during = us_time2 - us_time1          

	return us_during * 340 / 2 * 100        



def bin_full_level(us_dis):
	per_full = round(100*((bin_height-us_dis) / bin_height), 1)
	
	
	
	if per_full < 5:
		per_full = 0
	else:
		per_full = round(per_full * 4, 1) # increasing to make the bin "full" faster due to limited bottles
	#would be used to round to certain levels
	""" 
	if per_full < 8:
		per_full = 0
	if per_full > 10:
		per_full = 20
	"""
	return per_full

           

# 资源释放函数
def destroy():
	GPIO.cleanup() # 释放资源
	
	
	
def post_result(fullness):
	url = "http://192.168.1.100:8000/api/scan/"

	headers = CaseInsensitiveDict()
	headers['Accept'] = "application/json"
	headers['Content-Type'] = "application/json"

	today_date = datetime.datetime.now()

	data = {
			"bin": 1,
			"percent_full": int(fullness),
			"scan_date": today_date,
			}
			
	resp = requests.post(url, data=data)

	print(resp.status_code)
	print(resp.content)

def makerobo_loop():
	# print("before the loop")
	while True:
		# print("in the loop")
		us_dis = ur_disMeasure()   #measured in cm
		fullness = bin_full_level(us_dis)
		print ("The bin is currently " + str(fullness) + '% full')       
		print ('')
		if fullness > 50:
			print("The bin is full. Schedule pickup")
			post_result(fullness)
			break
		time.sleep(time_between_scans)  


if __name__ == "__main__":
	makerobo_setup() 
	# print("setup is complete")
	try:
		makerobo_loop() 
	except KeyboardInterrupt: 
		destroy() 
		
