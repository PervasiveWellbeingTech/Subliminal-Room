import os

def change(cur, amount):
	os.system("brightness " + str(cur + amount))

def reset(val):
	os.system("brightness " + str(val))
	print('resetted screen brightness: {}'.format(val))
	
