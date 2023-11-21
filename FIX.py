######	FIX Message Parsing Program
######	by Holly Roach
######	Thank you!
######	This program takes a text file of FIX messages as an argument in the command line. For example, run:
######	'python3 FIX.py Fix.Sample.txt'
import sys



text_file = str(sys.argv[1])				
message_array = []
with open(text_file) as f:
	for line in f.readlines():
		content = str(line)						# read each line from given text file, 
		message_array.append(content)			# and append each as a string to an array for later reference

accounts = {}									# this is where we will store the accounts and their min/max prices 

print("\nPrinting error notfications for duplicate fields. \n")	
for i in range(len(message_array)):							# look through all FIX messages
	parsed = message_array[i].split("|")					# split messages into fields 
	fields = {}												# this is where we will store each field's (key,value) pair
	for j in range(len(parsed)-1):							# look through all fields. NOTE: -1 is necessary because FIX messages end with "|"
		tag_value = parsed[j].split("=")					# split fields into (key,value) pairs
		if(fields.get(tag_value[0]) == None):				# if we have not seen this field yet, record its (key,value) pair
			fields[tag_value[0]] = [tag_value[1]]			# otherwise, print error message
		else:
			print("ERROR : Duplicate Field. Field Number = " + tag_value[0] + " in message number : " + str(i+1))	


	if(fields['35'] == ['D']):											# look through all New Order Single messages
		account_name = str(fields.get('1'))								# record the account name and that account's price min/max
		price_range = (fields.get('44'),fields.get('44'))				# NOTE: current price is both min and max until we look at more information
		if(accounts.get(account_name) == None):							# case where this is a new account name
			accounts[account_name] = price_range
		elif(accounts[account_name][0] > price_range[0]):				# case where this is a repeat account name, but new minimum price 
			new_range = (price_range[0], accounts[account_name][1])		
			accounts[account_name] = new_range
		elif(accounts[account_name][1] < price_range[1]):				# case where this is a repeat account name, but new maximum price
			new_range2 = (accounts[account_name][0], price_range[1])
			accounts[account_name] = new_range2
		else:
			pass


print("\nPrinting (lowest,highest) price range of valid New Order Single messages by Account.\n")
for name in accounts:
	print("Account:" + name + "\n" + "(Lowest price, Highest price):" + str(accounts[name]) + "\n")		#print NOS accounts and their price ranges




