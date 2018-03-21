import discord
import asyncio
import random
import requests
import platform
from discord import Game
from discord.ext.commands import Bot

client = Bot(description="A basic Discord bot", command_prefix="bb$", pm_help = False)

#
# Fun Games and Goofy Stuff
#


#This is a magic eight ball
@client.command(name='8ball',
				description="Answers a yes/no question.",
				brief="Answers from from the beyond.",
				aliases=['eight_ball', 'eightball', '8-ball'],
				pass_context=True)
async def eight_ball(context):
	possible_responses = [
		'It is certain',
		'It is decidedly so',
		'Without a doubt',
		'Yes definitely',
		'You may rely on it',
		'As I see it, yes',
		'Most likely',
		'Outlook good',
		'Yes',
		'Signs point to yes',
		'Reply hazy try again',
		'Ask again later',
		'Better not tell you now',
		'Cannot predict now',
		'Concentrate and ask again',
		'Do not count on it',
		'My reply is no',
		'My sources say no',
		'Outlook not so good',
		'Very doubtful'
	]
	await client.say(random.choice(possible_responses) + ", " + context.message.author.mention)

#A fun guessing game
@client.command(name='guess',
				description="User guesses a number between 1 & 10.",
				brief="User guesses a number between 1 & 10.",
				pass_context=True)
async def guessing_game(context):
	await client.say('Guess a number between 1 and 10.')
	def guess_check(m):
		return m.content.isdigit()
	guess = await client.wait_for_message(timeout=5.0, author=context.message.author, check=guess_check)
	answer = random.randint(1, 10)
	if guess is None:
		fmt = 'Sorry, you took too long to make a guess. It was {}.'
		await client.say(fmt.format(answer))
		return
	if int(guess.content) == answer:
		await client.say('You are right!')
	else:
		await client.say('Sorry, the number was actually {}.'.format(answer))

#Returns the squared value of a user-provided number
@client.command(name='square',
				description="Returns the squared value of a user-provided number.",
				brief="Returns the squared value of a user-provided number.",
				aliases=['squarethis', 'squared'])
async def square(number):
	squared_value = int(number) * int(number)
	await client.say(str(number) + " squared is " + str(squared_value))

#Greets the friendly user
@client.command(name='hello',
				description="Greets the friendly user.",
				brief="Greets the friendly user.",
				pass_context=True)
async def hello(context):
    await client.say("Hello, " + context.message.author.mention + ". Did you bring me a pumpkin spice latte?")

################################################################################################

#
# Utility Commands & Events
#

#Greets new guild members when they join the server.
@client.event
async def on_member_join(member):
	server = member.server
	fmt = 'Welcome, {0.mention}, to {1.name}! Do you like my new boots?'
	await client.send_message(server, fmt.format(member, server))

#Ping command to test bot response time.
@client.command(name='ping',
 				description="Tests bot response time.",
 				brief="Tests bot response time.",
 				pass_context=True)
async def ping(context):
	await client.say(':ping_pong: Pong!')

#Returns the current value of Bitcoin
@client.command(name='bitcoin',
				description="Returns the current value of Bitcoin.",
				brief="Returns the current value of Bitcoin.",
				aliases=['btc'])
async def bitcoin():
	url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
	response = requests.get(url)
	value = response.json()['bpi']['USD']['rate']
	await client.say("The current price of Bitcoin in USD is: $" + value)

################################################################################################

@client.event
async def on_ready():
	await client.change_presence(game=Game(name="with humans"))
	print('Connected!')
	print('Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to '+str(len(client.servers))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users')
	print('--------')
	print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
	print('--------')
	print('GitHub Link: https://github.com/RiggsB/ABasicDiscordBot')
	print('--------')
	print('You are running BasicBot v1.0.0a') #Do not change this. This will really help me support you, if you need support.
	print('Created by Bad Pancake#6942')

#Logs all servers on which BasicBot is running on boot and every 20mins thereafter.
async def list_servers():
	await client.wait_until_ready()
	while not client.is_closed:
		await asyncio.sleep(3)
		print('--------')
		print ("Current servers: ")
		for server in client.servers:
			print(server.name)
		await asyncio.sleep(1197)

client.loop.create_task(list_servers())
client.run('') #Place your token inside the single quotes here.