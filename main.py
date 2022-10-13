import pyCardDeck
import os
import discord
from dotenv import load_dotenv

suits = {'R':'Rams',
		 'T': 'Tomes',
		 'M': 'Masks',
		 'C': 'Crows'}

suits_lvl = [[1, 5, 9, 13],
			 [4, 8, 12],
			 [3, 7, 11],
			 [2, 6, 10]]

def malifaux_fate_deck():
	deck = []
	#suits = ['Rams', 'Tomes', 'Masks', 'Crows']
	for s in suits.values():
		for i in range(1, 14):
			deck.append("%d of %s" % (i, s))
	deck.append("Red Joker")
	deck.append("Black Joker")
	return deck

def malifaux_twist_deck(code_list):
	code = code_list[0].upper()
	#print(type(code))
	tw_deck_list = list()
	tw_deck = dict()
	count = 0
	for s in code:
		tw_deck[suits[s]] = suits_lvl[count]
		count += 1
	print(tw_deck)
	count = 0
	for i in tw_deck.keys():
		for j in suits_lvl[count]:
			tw_deck_list.append("%d of %s" % (j, i))
		count += 1
	print(tw_deck_list)
	return tw_deck_list


load_dotenv()
#users_dict = dict()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client(intents=discord.Intents.default())
print(TOKEN)

f_deck = pyCardDeck.Deck(cards=malifaux_fate_deck(), name="Fate Deck")
f_deck.shuffle()
tw_decs = dict()
tw_hands = dict()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
	#global f_deck
	if message.content.startswith('$'):
		command, *other = message.content.split()
		print(command)
		print(other)
		if command == "$draw":
			if other:
				for i in range(int(other[0])):
					card = f_deck.draw()
					f_deck.discard(card)
					await message.channel.send(f"Card drew: {card}")
					#print(f_deck.discarded, f_deck.cards_left)
					if f_deck.cards_left == 1:
						await message.channel.send("Deck's empty, reshuffle")
					#	f_deck.shuffle_back()
					#	f_deck.shuffle()
			else:
				card = f_deck.draw()
				f_deck.discard(card)
				await message.channel.send(f"Card drew: {card}")
				if f_deck.cards_left == 1:
					await message.channel.send("Deck's empty, reshuffle")
		if command == "$discard":
			await message.channel.send(f"Discard pile: {f_deck._discard_pile}")
		if command == "$shuffle":
			f_deck.shuffle_back()
			f_deck.shuffle()
			await message.channel.send("Fate Deck has been shuffled")
		if command.find("$twd_") > -1:
			#print("HERE")
			if command.find("create") > -1:
				#print("HERE1")
				tw_decs[message.author.name] = pyCardDeck.Deck(cards=malifaux_twist_deck(other), name="Twist Deck")
				tw_decs[message.author.name].shuffle()
				tw_hands[message.author.name] = pyCardDeck.Deck()
				await message.channel.send(f"{message.author.name} creates Twist Deck")
			if command.find("draw") > -1:
				#print("HERE2")
				if other:
					for i in range(int(other[0])):
						tw_card = tw_decs[message.author.name].draw()
						tw_hands[message.author.name].add_single(tw_card)
						#tw_decs[message.author.name].discard(tw_card)
						await message.channel.send(f"Card drew: {tw_card}")
						#print(f_deck.discarded, f_deck.cards_left)
						if tw_decs[message.author.name].cards_left == 1:
							await message.channel.send("Deck's empty, reshuffle")
							#	f_deck.shuffle_back()
							#	f_deck.shuffle()
				else:
					tw_card = tw_decs[message.author.name].draw()
					#tw_decs[message.author.name].discard(tw_card)
					await message.channel.send(f"Card drew: {tw_card}")
					if tw_decs[message.author.name].cards_left == 1:
						await message.channel.send("TWdeck's empty, reshuffle")
			if command.find("hand") > -1:
				await message.channel.send(f"{message.author.name}'s hand:{tw_hands[message.author.name]._cards}")
			if command.find("card_use") > -1:
				tw_card = tw_hands[message.author.name]._cards[int(other[0]) - 1]
				await message.channel.send(f"{message.author.name} uses TD card: {tw_card}")
				tw_hands[message.author.name].discard(tw_card)
				tw_decs[message.author.name].discard(tw_card)
			if command.find("discard") > -1:
				await message.channel.send(f"{message.author.name}'s TD discard: {tw_hands[message.author.name]._discard_pile}")
				#tw_card = tw_decs[message.author.name].draw()
				#tw_hands[message.author.name] =
				#tw_decs[message.author.name].discard(tw_card)

client.run(TOKEN)