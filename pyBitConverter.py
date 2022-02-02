'''
#Ryan Plante
#pyBitConverter
#12/13/21
#This was created as the final project for Program Essentials with Python SE116.01 

#PROGRAM PROMPT: main() is called at the start and it calls the menu function to display menu options

#VARIABLE DICTIONARY:
there's no global variables, I'll describe the variables in the functions

#NOTES: 
This is a program that has a menu and allows for conversion of integer<->hexadecimal and integer<->binary hexadecimal<->binary

#----------------------------------------------------
'''

# import only system from os
from os import system, name

# import sleep to show output for some time period
from time import sleep
  
# clear the screen, only works if the program is being ran in the console
def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
  
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

# this function just clears the main screen and displays the menu
# clear only works if you're running this program in console
def menu():
	clear()
	print("========Binary Converter========")
	print("\t1: Hexadecimal to integer")
	print("\t2: Hexadecimal to binary")
	print("\t3: Integer to binary")
	print("\t4: Integer to hexadecimal")
	print("\t5: Binary to integer")
	print("\t6: Binary to hexadecimal")
	print("\t7: Settings")
	print("\t8: Exit program")

# pass timer to set_timer function so that it can access private variable from main function 
# timer: holds integer for how long to sleep the console in the main function
# returns the timer back to the main function since its not a global variable
def set_timer(timer):
	clear()
	print("========Settings========")
	print("Timer:", timer)
	# set timer to -1 to create invalid input to keep looping until its valid
	timer = -1
	while (timer == -1):
		timer = get_valid_input("Please enter in seconds how long you want results to be displayed [1-60]: ", 1, 60)
	return timer

# get_valid_input returns -1 if input is invalid and the user_choice if it is valid in range of low and high
# label: the text to display when using python's input function
# low: low number to check for valid input
# high: high number to check for valid input
# user_choice: input variable 
def get_valid_input(label, low, high):
	user_choice = int(input(label))
	# if user_choice is not in the range, return -1 for invalid input
	if (user_choice > high or user_choice < low):
		return error()
	else:
		return user_choice

# this function was created because input is checked a lot so it prints error, returns -1 and goes back to the function call
def error():
	print("ERROR! Invalid input")
	# sleep for 1 second to show error because menu clears the console
	sleep(1)
	return -1

# this function checks if input is a valid hexadecimal string 
# returns -1 if not, checked in the main function
# hexString: input hexString to be used to check
# tmp: temporary variable to check individual character
def get_hex_input():
	hexString = input("Enter a hexadecimal number to convert: 0x")
	# convert it to uppercase for easy access to string
	hexString = hexString.upper()
	for hex in hexString:
		# get the ascii value of the character to check
		tmp = ord(hex)
        # if its greater than a uppercase 'F'
		if (tmp > 0x46):
			return error()
		# if its greather than '0'
		elif (tmp < 0x30):
			return error()
		else:
			# if its any of the special characters between 9 and A
			if (tmp < 0x39 and tmp > 0x41):
				return error()
	# once function is done looping through the characters, return the correct character if its not -1
	return hexString

# this function checks if input is a valid binary string
# returns -1 if not, checked in the main function
# binString: the binary string of user input
# bit: temporary varuable to check character in string
def get_bin_input():
	binString = input("Enter a binary string to convert: ")
	for bit in binString:
		if (int(bit) > 1 or int(bit) < 0):
			return error()
	return binString


# hex_string_to_int converts a string hexString and converts to int without using much python built-in functions
# hexString: string of hex characters ie: 0xABCD
# result: final integer to store result in, returns -1 if it fails
# tmp: temporary variable to store each individual hex character during the conversion
def hex_string_to_int(hexString):
    result = 0
    # convert to uppercase for easier string manipulation
    hexString = hexString.upper()
    # loop through each character in hexstring
    for hex in hexString:
    	# get the ascii value of the character 
        tmp = ord(hex)
        # if its less than a uppercase 'G'
        if (tmp < 0x47):
        	# mask the upper bits because the lower bits is what contains the value we need
            tmp = tmp & 0xF
            # if the ascii value is > 0x40 or < 'A'
            if (ord(hex) > 0x40):
            	# add 9 to it because for example A would be ascii 0x41, masking the 4 would make it 1, adding 1 would make it 10
                tmp = tmp + 9
            # left shift the result by 4 so that you can hold the final value and combine the character that was converted
            result = result << 4
            # combine the character converted with result using bitwise or
            result = result | tmp
        # return -1 if its an invalid character
        else:
        	return -1
    return result

# int_to_hex converts a integer to a hexString
# num: number to convert
# hexString: the result, holds the string equivilent of the integer num
# tmp: temporary number to hold the remainder
def int_to_hex(num):
	# create an empty string to manipulate later in the program
	hexString = ""
	# if the number is negative return -1 for error since it'd take too much time to flip the bit for signed
	# this program assumes that the integer is unsigned
	if (num < 0):
		return -1
	while(num != 0):
		# temp variable to store remainder
		tmp = 0
		# store remainder in temp variable
		tmp = num % 16
		# if the remainder is 0-9
		if (tmp < 10):
			# convert the ascii character to '0' and add it to the result
			hexString = hexString + chr(tmp + 48)
		# 10 or greater would make it A-F
		else:
			hexString = hexString + chr(tmp + 55)
		# do integer division because floats don't work well in this sceneratio
		num = num // 16
	# it will store the string in reverse order, so now we have to reverse it
	return hexString[::-1]

# is_bit_activated takes a number and position argument to check if that indidual bit is activated by left shifting the number
# num: the number to check
# pos: the position to check
def is_bit_activated(num, pos):
	# left shift by the position in order to see if the bit is activated
    if num & (1 << pos):
        return 1
    else:
        return 0

# int_to_binary takes a integers and converts it to binary using is_bit_activated 
# num: integer to convert
# binString: stores the binary in string
def int_to_binary(num):
	# create a empty string to manipulate
    binString = ""
    # loop through each bit in the integer (int is 32 bits)
    for x in range(0,32):
    	# check if the bit is on or off and convert it to a string
        binString = binString + str(is_bit_activated(num, 31 - x))
    return binString


# bin_to_int takes a binary string and converts to integer
# result: result to return
# this function checks if the number is 1 or 0 and then multiplies base 2 
# returns -1 if its invalid
def bin_to_int(binString):
	result = 0
	# i is an iterator to accumlate the binary place
	i = 1
	# loop through each bit in the binary string
	for bit in binString:
		# convert the string to integer
	    digit = int(bit)
	    # make sure input is valid
	    if (digit > 1 or digit < 0):
	    	# if user inputs anything but 1 or 0 then its invalid
	    	return -1
	    result = result + (digit * i)
	    i = i * 2
	return result



# this is the main function and the entry point to the function
# timer is a setting variable that is used to slow down how long the result is displayed
# user_choice is just user's input to go into different screens
def main():
	timer = 3
	user_choice = -1
	# keep looping while input is invalid to keep asking for input
	while (user_choice == -1):
		# display the menu
		menu()
		# get user input
		user_choice = get_valid_input("Please enter your choice: ", 1, 8)
		# keep looping until they chose 8 to exit the program
		while (user_choice != 8):
			# store result in a string so that it can hold binString and hexString results
			if (user_choice == 1):
				hexString = get_hex_input()
				if (hexString != -1):
					print("Result: ", hex_string_to_int(hexString))
			elif (user_choice == 2):
				binString = get_hex_input()
				if (binString != -1):
					# do a nested function call to save creating a new function since its not needed
					print("Result: ", int_to_binary(hex_string_to_int(binString)))
			elif (user_choice == 3):
				num = int(input("Enter a number to convert: "))
				print("Result: ", int_to_binary(num))
			elif (user_choice == 4):
				num = int(input("Enter a number to convert: "))
				print("Result: 0x" + int_to_hex(num))
			elif (user_choice == 5):
				binString = get_bin_input()
				if (binString != -1):
					print("Result: ", bin_to_int(binString))
			elif (user_choice == 6):
				binString = get_bin_input()
				# check if input is invalid
				if (binString != -1):
					print("Result: 0x" + int_to_hex(bin_to_int(binString)))
			elif (user_choice == 7):
				# timer needs to be passed to this function since its a private variable to the main function
				timer = set_timer(timer)
			# only print this if input is valid so that it can ask for input again instantly
			if (user_choice != -1):
				print("Returning to main menu...")
				# sleep for timer's seconds to show the returning screen, otherwise it is instant
				sleep(timer)
			menu()
			user_choice = get_valid_input("Please enter your choice: ", 1, 8)
# call main loop
main()
# display goodbye
print("Goodbye! :)")