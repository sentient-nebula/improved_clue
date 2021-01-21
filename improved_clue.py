#twitter bot

from random import randint
import tweepy

def read_file(path):
	# specific to the data for this project
	# each file has a header (e.g., 'Names')
	# and all entries on new lines, i.e., separated by a '\n' character
	
	with open(path) as f:
		data = f.read()
		
	out_list = data.split('\n')[1:-1]
	# the first entry is the name of the column
	# the last entry is the empty string indicating EOF
	
	return out_list


def get_random_entry(from_list):
	# need the -1 the way randint and indexing work
	return from_list[randint(0,len(from_list) -1)]

def generate_clue():

	name  = get_random_entry(read_file('names.txt'))
	place = get_random_entry(read_file('places.txt'))
	item  = get_random_entry(read_file('items.txt'))
	
	clue = "It was %s %s with the %s."%(name,place,item)
	return clue
	
def log_in_to_twitter():

	# read credentials
	with open('twitter_credentials.txt') as f:
		read_data = f.read()
	
	credentials = {line.split(':')[0]:line.split(':')[1] for line in read_data.split('\n')}

	# create API instance
	auth = tweepy.OAuthHandler(credentials['API_key'], credentials['API_secret_key'])
	auth.set_access_token(credentials['access_token'],credentials['access_token_secret'])
	api = tweepy.API(auth)
	
	# log in
	try:
		api.verify_credentials()
		print("Authentication OK")
		return api
	except:
		print('Twitter error. Error during authentication.')
		raise NameError('Twitter error. Error during authentication.')
	


if __name__ == '__main__':

	clue = generate_clue()
	print(clue)
	
	api = log_in_to_twitter()
	
	try:
		api.update_status(clue)
		print('It is done.')
	except:
		print('Twitter error. Error during post.')
		raise NameError('Twitter error. Error during post.')

