# Used in conjunction with https://github.com/m3wolf/professor_oak (Professor Oak Lab Management System). Script to run on a Raspberry Pi that will send a HTTPrequest to the main inventory server to mark a certain container_id as empty and hopefully, if it's not too complicated to program, output a success message to a GPIO LCD display. Questions? Comments? email michael.plews@gmail.com

import datetime, requests, json, LOCALSETTINGS as localsettings

#variables
debug = 'OFF'
barcode_digit_length = 6

base_url = localsettings.base_url
username = localsettings.username
password = localsettings.password

def login():
	auth = requests.auth.HTTPBasicAuth(username, password)
	return auth
 
def do_command(input):
	if input == 'EXIT':
		exit() 
	
def check_if_empty(id_number):
	#stubbed for development
	return None

def mark_as_empty(id_number):
	url = base_url + str(id_number)
	payload = {
		'is_empty': True,
		}
	auth = login()

	r = requests.patch(url, json=payload, auth=auth)
	
	if str(r.status_code) == '200':
		if debug == 'ON':
			print (r.text)	
		return 'success (200)'
	elif str(r.status_code) == '404':
		if debug == 'ON':
			print (r.text)	
		return 'not found (404)'
	elif str(r.status_code) == '403':
		if debug == 'ON':
			print (r.text)	
		return 'not authorized (403)'
	elif str(r.status_code) == '400':
		if debug == 'ON':
			print (r.text)
		return 'bad request (400)'
	else:
		if debug == 'ON':
			print (r.text)	
		return 'unknown error (' + str(r.status_code) +')'
		
def write_to_log(message_string, status_code):
	log_file = open("./emptied_chemicals.log", 'a')
	log_file.write(str(datetime.date.today()) + ' ' + datetime.datetime.now().time().strftime("%H:%M:%S") + '\t' + message_string + '\t' + status_code +'\n')
	log_file.close
	
while True:
	barcode = str(input('input:'))
	do_command(barcode)
	try:
		int_barcode = int(barcode) #checks the input is an integer to avoid foul play
	except ValueError:
		print ('Value not an integer. No information was passed to the server.')
		write_to_log('error: Value not an integer. No information was passed to the server.','')
	else:
		status_return = mark_as_empty(barcode)
		write_to_log(str(barcode).zfill(barcode_digit_length), status_return)
		print ('ID#' + str(barcode).zfill(barcode_digit_length) + '\t' + status_return)
