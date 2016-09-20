# Used in conjunction with https://github.com/m3wolf/professor_oak (Professor Oak Lab Management System). Script to run on a Raspberry Pi that will send a HTTPrequest to the main inventory server to mark a certain container_id as empty and hopefully, if it's not too complicated to program, output a success message to a GPIO LCD display. Questions? Comments? email michael.plews@gmail.com

import re, datetime, requests, json, LOCALSETTINGS as localsettings

#variables
debug = localsettings.DEBUG
barcode_digit_length = 6

ulon_url = localsettings.ulon_url
base_url = localsettings.base_url
username = localsettings.username
password = localsettings.password

def login():
	auth = requests.auth.HTTPBasicAuth(username, password)
	return auth
 
def do_command(input):
	if input == 'EXIT':
		exit() 

def validate(input):
	regex = re.compile(r'(UL)?\d{1,' + re.escape(str(barcode_digit_length)) + '}$', flags=re.IGNORECASE)
	if regex.match(input):
		return True
	else:
		return False

def send_notification(id_number, note_type):
	#stubbed for development
	auth = login()	
	if note_type == 'ULON':
		url = ulon_url + str(id_number)
		r = requests.get(url, auth=auth)
	return r.status_code

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
	if validate(barcode):
		if barcode[:2] == 'UL':
			status_return = send_notification(barcode[2:], note_type='ULON')
			barcode_string = str(barcode)
		else:
			status_return = mark_as_empty(barcode)
			barcode_string = str(barcode).zfill(barcode_digit_length)
		write_to_log(barcode_string, status_return)
		print ('ID#' + barcode_string + '\t' + status_return)
	else:
		print ('Input does not match validation. No information was passed to the server.')
		write_to_log('error: Input does not match validation. No information was passed to the server', '')
