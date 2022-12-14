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
client = discord.Client(intents=discord.Intents.all())
#print(TOKEN)

tw_decs = dict()
tw_hands = dict()
f_decks = dict()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
	#global f_deck
	if message.content.startswith('$'):
		command, *other = message.content.split()
		#print(command)
		#print(other)
		if command == "$create":
			f_decks[message.guild] = pyCardDeck.Deck(cards=malifaux_fate_deck(), name=f"{message.guild} Fate Deck")
			f_decks[message.guild].shuffle()
			await message.channel.send(f"**{message.author.name}** creates Fate Deck at `{message.guild}` guild")
		if command == "$draw":
			if not other:
				other.append(1)
			for i in range(int(other[0])):
				card = f_decks[message.guild].draw()
				f_decks[message.guild].discard(card)
				await message.channel.send(f"**{message.author.name}** drew `{card}` from Fate Deck")
				#print(f_deck.discarded, f_deck.cards_left)
				if f_decks[message.guild].cards_left == 1:
					await message.channel.send("Fate Deck is empty")
					await message.channel.send("Fate Deck has been shuffled")
		if command == "$discard":
			await message.channel.send(f"Fate Deck's discard pile: `{f_decks[message.guild]._discard_pile}`")
		if command == "$shuffle":
			f_decks[message.guild].shuffle_back()
			f_decks[message.guild].shuffle()
			await message.channel.send("Fate Deck has been shuffled")
		if command.find("$twd_") > -1:
			#print("HERE")
			if command.find("create") > -1:
				#print("HERE1")
				tw_decs[message.author.name] = pyCardDeck.Deck(cards=malifaux_twist_deck(other), name=f"{message.author.name}'s Twist Deck")
				tw_decs[message.author.name].shuffle()
				tw_hands[message.author.name] = list()
				await message.channel.send(f"**{message.author.name}** creates Twist Deck")
			if command.find("draw") > -1:
				#print("HERE2")
				if not other:
					other.append(1)
				for i in range(int(other[0])):
					tw_card = tw_decs[message.author.name].draw()
					tw_hands[message.author.name].append(str(tw_card))
					#tw_decs[message.author.name].discard(tw_card)
					await message.channel.send(f"**{message.author.name}** drew `{tw_card}` from Twist Deck")
					await message.channel.send(f"**{message.author.name}** 's hand:`{tw_hands[message.author.name]}`")
					#print(f_deck.discarded, f_deck.cards_left)
					if tw_decs[message.author.name].cards_left == 1:
						await message.channel.send(f"**{message.author.name}** 's Twist Deck is empty")
						await message.channel.send(f"**{message.author.name}** 's Twist Deck has been shuffled")
			if command.find("hand") > -1:
				await message.channel.send(f"**{message.author.name}** 's hand:`{tw_hands[message.author.name]}`")
					#(f"{message.author.name}'s hand: {list(set(tw_hands[message.author.name]._cards) - set(tw_hands[message.author.name]._discard_pile))}")
			if command.find("card_use") > -1:
				tw_card = tw_hands[message.author.name][int(other[0]) - 1]
				tw_hands[message.author.name].pop(int(other[0]) - 1)
				tw_decs[message.author.name].discard(tw_card)
				await message.channel.send(f"**{message.author.name}** uses Twist Deck card: `{tw_card}`")
				await message.channel.send(f"**{message.author.name}** 's hand:`{tw_hands[message.author.name]}`")
			if command.find("discard_pile") > -1:
				await message.channel.send(f"**{message.author.name}** 's Twist Deck discard: `{tw_hands[message.author.name]._discard_pile}`")
				#tw_card = tw_decs[message.author.name].draw()
				#tw_hands[message.author.name] =
				#tw_decs[message.author.name].discard(tw_card)
		if command == '$help':
			await message.channel.send('''
			***Malifaux Deck Bot commands:***
			**Fate Deck commands:**
				`$create` - creates Fate Deck at current server
				`$draw X` - draw X cards from existing Fate Deck
				`$shuffle` - shuffle in discard pile and shuffle deck
				`$discard` - show discard pile

			**Twist Deck commands for Twist Deck:**
				`$twd_create ????` - create Twist Deck and Twist Hand for user, base on Deck code - 4 letters in priority order, ex.: mrct
				`$twd_draw X` - draw X cards from user's existing Twist Deck to Twist Hand, show Twist Hand
				`$twd_card_use N` - use card number N from existing Twist Hand and discard it, show Twist Hand
				`$twd_hand` - show existing 
				`$twd_discard` - show Twist Deck discard pile
				''')

client.run(TOKEN)
