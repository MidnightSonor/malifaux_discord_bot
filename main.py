import pyCardDeck
import os
import asyncio
import time
import discord
from dotenv import load_dotenv

def malifaux_fate_deck():
	deck = []
	suits = ['Rams', 'Tomes', 'Masks', 'Crows']
	for s in suits:
		for i in range(1, 14):
			deck.append("%d of %s" % (i, s))
	deck.append("Red Joker")
	deck.append("Black Joker")
	return deck

load_dotenv()
users_dict = dict()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()
print(TOKEN)

curr_deck = pyCardDeck.Deck(cards=malifaux_fate_deck(), name="Fate Deck")
curr_deck.shuffle()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
	#global curr_deck
	if message.content.startswith('$'):
		command, *other = message.content.split()
		print(command)
		print(other)
		if command == "$draw":
			if other:
				for i in range(int(other[0])):
					card = curr_deck.draw()
					curr_deck.discard(card)
					await message.channel.send(f"Card drew: {card}")
					#print(curr_deck.discarded, curr_deck.cards_left)
					if curr_deck.cards_left == 1:
						await message.channel.send("Deck's empty, reshuffle")
					#	curr_deck.shuffle_back()
					#	curr_deck.shuffle()
			else:
				curr_deck.shuffle_back()
				curr_deck.shuffle()
		if command == "$discard":
			await message.channel.send(f"Discard pile: {curr_deck._discard_pile}")
		if command == "$shuffle":
			curr_deck.shuffle_back()
			curr_deck.shuffle()
			await message.channel.send("Fate Deck has been shuffled")

client.run(TOKEN)
