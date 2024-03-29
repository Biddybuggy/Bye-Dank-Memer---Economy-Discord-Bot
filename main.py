import discord
from discord.ext import commands
import json
import random
import time
import datetime

intents = discord.Intents.all() 
bot = commands.Bot(command_prefix="b!",intents=intents)
bot.remove_command("help")

mainshop = [{"name":"Coke","price":100,"description":"Have fun :)"},{"name":"Watch","price":2500,"description":"Time"},{"name":"Laptop","price":30000,"description":"Work"},{"name":"PC","price":50000,"description":"Gaming"},
{"name":"Monitor","price":10000,"description":"See what you're doing on your computer"},{"name":"Headphones","price":7500,"description":"Listen to things on your computer"},{"name":"Mouse","price":5000,"description":"Control your computer"},{"name":"Grades","price":50000,"description":"Get an A+ in every subject"},{"name":"House","price":100000,"description":"Home"},
{"name":"Shovel", "price":5000, "description":"Dig for coins!"},{"name":"4090Ti","price":1000000,"description":"This GPU is overpriced but it's definitely worth it (not for everyone tho)"}]

wallet_lim = 1000000000
bank_lim = 100000000

wallet_lim_msg = "You already have the max amount of coins you can have in your wallet, bud."
bank_lim_msg = "You already have the max amount of coins you can have in your bank, bud."

def add(x,y):
  return x + y
def subtract(x,y):
  return x - y
def multiply(x,y):
  return x * y
def divide(x,y):
  return x / y

@bot.event
async def on_ready():
  await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.playing, name="b!help"))
  print("Bye Dank Memer online.")

@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandOnCooldown):
        # Calculate the remaining time in seconds
        remaining_time = error.retry_after
        # Convert the remaining time to a readable format
        remaining_time = time.strftime('%M:%S', time.gmtime(remaining_time))
        await ctx.reply(f'Hold your horses for {remaining_time}, bud.')

@bot.command()
async def help(ctx):
    embed=discord.Embed(title="Commands List", description="Always use the prefix b! before each command", color=0x000000)
    embed.add_field(name="Currency", value="balance, bankrob, beg, buy, chest, compare, deposit, dig, gamble, inventory, postmeme, rob, search, share, shop, snakeeyes, withdraw, work", inline=False)
    embed.add_field(name="Fun", value="attractive, crystalball, eightball, height, pickupline, quote, simprate, ship, spam, userping, waifu")
    embed.add_field(name="Miscellaneous", value="calculate, greetings, info, invite, ping, resetmydata, timenow", inline=False)
    embed.add_field(name="NSFW", value="None cause we are family friendly unlike Dank Memer", inline=False)
    embed.add_field(name="It Comes And It Goes", value="maxstat",inline=False)
    embed.add_field(name="Upcoming Commands", value="america, daily, leaderboard, monthly, sell, stream")
    embed.set_footer(text=f"Hope it helps, {ctx.author}")
    await ctx.reply(embed=embed)
    return

@bot.command()
async def invite(ctx):
  embed = discord.Embed(title="Invite Bye Dank Memer to Your Server", description="https://tinyurl.com/byedankmemerinvite", color=0x000000)
  await ctx.reply(embed=embed)

@bot.command()
async def info(ctx):
  embed=discord.Embed(title="About Us", description="Hi there! We are avid Discord users who really love Discord bots. Our personal favorite bot is Dank Memer. However, we discovered that there are numerous aspects of Dank Memer that are not family friendly. Thus, we created Bye Dank Memer, a family friendly version of Dank Memer :)", color=0x000000)
  await ctx.reply(embed=embed)

@bot.command(aliases=["bal"])
async def balance(ctx, member:discord.Member = None):
  if member == None:
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]

    embed = discord.Embed(title = f"{ctx.author.name}'s balance", color=0x000000)
    embed.add_field(name = "Wallet", value = wallet_amt)
    embed.add_field(name = "Bank", value = bank_amt)
    await ctx.reply(embed = embed)
    return

  else:
    await open_account(member)
    user = member
    users = await get_bank_data()

    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]

    embed = discord.Embed(title = f"{member}'s balance", color=0x000000)
    embed.add_field(name = "Wallet", value = wallet_amt)
    embed.add_field(name = "Bank", value = bank_amt)
    await ctx.reply(embed = embed)
    return

@bot.command()
async def resetmydata(ctx, confirmation = None):
  if confirmation == None:
    await ctx.reply("Please confirm that you want to reset your data by typing in 'confirm' after the command :)")
    return
  elif confirmation == "confirm":
    await open_account(ctx.author)

    bal = await update_bank(ctx.author)

    walletloss = -1*bal[0] + 5000
    bankloss = -1*bal[1]

    await update_bank(ctx.author, walletloss)
    await update_bank(ctx.author,bankloss,"bank")

    bal = await update_bank(ctx.author)

    embed = discord.Embed(title = "Reset Data Successful", color = 0x000000)
    embed.add_field(name = "Current Wallet Balance", value = bal[0], inline = False)
    embed.add_field(name = "Current Bank Balance", value = bal[1], inline = False)
    await ctx.reply(embed = embed)
    return
  else:
    await ctx.reply("Confirmation should be 'confirm'")
    return

@bot.command()
async def maxstat(ctx):
  await open_account(ctx.author)

  bal = await update_bank(ctx.author)

  walletgain = wallet_lim - bal[0]
  bankgain = bank_lim - bal[1]

  await update_bank(ctx.author, walletgain)
  await update_bank(ctx.author,bankgain,"bank")

  bal = await update_bank(ctx.author)

  embed = discord.Embed(title = "Reset Data (MaxStat) Successful", color = 0x000000)
  embed.add_field(name = "Current Wallet Balance", value = bal[0], inline = False)
  embed.add_field(name = "Current Bank Balance", value = bal[1], inline = False)
  await ctx.reply(embed = embed)
  return

@bot.command()
async def compare(ctx,member:discord.Member = None,member2:discord.Member=None):
  if member == None:
    await ctx.reply("Who do you want to compare?")
    return

  elif member != None and member2 == None:
    await open_account(ctx.author)
    await open_account(member)

    bal = await update_bank(ctx.author)
    bal2 = await update_bank(member)

    author_bal = bal[0] + bal[1]
    member_bal = bal2[0] + bal2[1]

    if author_bal > member_bal:
        richer_person = ctx.author
        poorer_person = member
        difference = author_bal - member_bal

    elif member_bal > author_bal:
        richer_person = member
        poorer_person = ctx.author
        difference = member_bal - author_bal

    elif member_bal == author_bal:
        embed = discord.Embed(title=f"{ctx.author} vs {member}", color=0x000000)
        embed.add_field(name = "Wallet", value="Wallet Balance",inline=False)
        embed.add_field(name=f"{ctx.author}",value=bal[0],inline=False)
        embed.add_field(name=f"{member}",value=bal2[0],inline=False)
        embed.add_field(name="Bank", value="Bank Balance",inline=False)
        embed.add_field(name=f"{ctx.author}",value=bal[1],inline=False)
        embed.add_field(name=f"{member}",value=bal2[1],inline=False)
        embed.add_field(name=f"Richer User",value="None", inline = False)
        await ctx.reply(embed=embed)
        return
        
    embed = discord.Embed(title=f"{ctx.author} vs {member}", color=0x000000)
    embed.add_field(name = "Wallet", value="Wallet Balance",inline=False)
    embed.add_field(name=f"{ctx.author}",value=bal[0],inline=False)
    embed.add_field(name=f"{member}",value=bal2[0],inline=False)
    embed.add_field(name="Bank", value="Bank Balance",inline=False)
    embed.add_field(name=f"{ctx.author}",value=bal[1],inline=False)
    embed.add_field(name=f"{member}",value=bal2[1],inline=False)
    embed.add_field(name=f"Richer User",value=f"{richer_person} \nRicher than {poorer_person} by {difference} coins", inline = False)
    await ctx.reply(embed=embed)
    return

  elif member != None and member2 != None:
    await open_account(member)
    await open_account(member2)

    bal = await update_bank(member)
    bal2 = await update_bank(member2)

    member_bal = bal[0] + bal[1]
    member2_bal = bal2[0] + bal2[1]

    if member_bal > member2_bal:
        richer_person = member
        poorer_person = member2
        difference = member_bal - member2_bal
    elif member2_bal > member_bal:
        richer_person = member2
        poorer_person = member
        difference = member2_bal - member_bal
    elif member_bal == member2_bal:
        embed = discord.Embed(title=f"{member} vs {member2}", color=0x000000)
        embed.add_field(name = "Wallet", value="Wallet Balance",inline=False)
        embed.add_field(name=f"{member}",value=bal[0],inline=False)
        embed.add_field(name=f"{member2}",value=bal2[0],inline=False)
        embed.add_field(name="Bank", value="Bank Balance",inline=False)
        embed.add_field(name=f"{member}",value=bal[1],inline=False)
        embed.add_field(name=f"{member2}",value=bal2[1],inline=False)
        embed.add_field(name=f"Richer User",value="None", inline = False)
        await ctx.reply(embed=embed)
        return
        
    embed = discord.Embed(title=f"{member} vs {member2}", color=0x000000)
    embed.add_field(name = "Wallet", value="Wallet Balance",inline=False)
    embed.add_field(name=f"{member}",value=bal[0],inline=False)
    embed.add_field(name=f"{member2}",value=bal2[0],inline=False)
    embed.add_field(name="Bank", value="Bank Balance",inline=False)
    embed.add_field(name=f"{member}",value=bal[1],inline=False)
    embed.add_field(name=f"{member2}",value=bal2[1],inline=False)
    embed.add_field(name=f"Richer User",value=f"{richer_person} \nRicher than {poorer_person} by {difference} coins", inline = False)
    await ctx.reply(embed=embed)

    return

@bot.command()
@commands.cooldown(1,3,commands.BucketType.user)
async def beg(ctx):
  await open_account(ctx.author)
  bal = await update_bank(ctx.author)

  if bal[0] == wallet_lim:
    await ctx.reply(wallet_lim_msg)
    return

  fates = ["get", "dontget"]
  people = ["Rick Astley", "Barack Obama", "Joe Biden", "Donald Trump", "Ye (Kanye West)", "Kim Kardashian"]
  userfate = random.choice(fates)

  if userfate == "get":
    earnings = random.randint(1, 101)

    if bal[0] + earnings > wallet_lim:
      actual_earning = wallet_lim - bal[0]

      embed = discord.Embed(title = random.choice(people), description = f"Oh you poor little beggar, take {actual_earning} coins", color=0x000000)
      await ctx.reply(embed = embed)

      await update_bank(ctx.author,actual_earning)

      return
    elif bal[0] + earnings < wallet_lim:
      earnings = earnings

      embed = discord.Embed(title = random.choice(people), description = f"Oh you poor little beggar, take {earnings} coins", color=0x000000)
      await ctx.reply(embed = embed)

      await update_bank(ctx.author,earnings)

      return

  elif userfate == "dontget":
    embed = discord.Embed(title = random.choice(people), description="Sorry, but you don't deserve my money", color=0x000000)
    embed.set_footer(text = "Imagine begging lol")
    await ctx.reply(embed = embed)
    return

@bot.command()
@commands.cooldown(1,20,commands.BucketType.user)
async def search(ctx,place=None):
  await open_account(ctx.author)
  bal = await update_bank(ctx.author)

  if bal[0] == wallet_lim:
    await ctx.reply(wallet_lim_msg)
    return

  if place == None:
    embed = discord.Embed(title="Places You Can Search", description = "1. Couch \n2. Crawlspace \n3. Air \n4. Street \n5. Bathroom \n6. Room", color=0x000000)
    embed.add_field(name="Format",value="b!search <place name>",inline=False)
    embed.set_footer(text="Tip: Don't include any capital letters while typing out a place's name")
    await ctx.reply(embed=embed)
    return

  else:
    if place in ("couch", "crawlspace", "air", "street", "bathroom", "room"):
      earnings = random.randint(100,3000)
      if bal[0] + earnings > wallet_lim:
        earnings = wallet_lim - bal[0]
      
      fate_number = random.randint(1,10)
      if 1 <= fate_number <= 6:
        await ctx.reply(f"You searched the {place} and found {earnings} coins!")
        await update_bank(ctx.author,earnings)
        return
      elif 7 <= fate_number <= 10:
        await ctx.reply("You sadly didn't find any coins...")
        return

    else:
      await ctx.reply("Sorry, but you can't search that place for now")
      return

@bot.command(aliases=["dep"])
async def deposit(ctx,amount = None):
  await open_account(ctx.author)
  bal = await update_bank(ctx.author)

  if amount in ("all", "max", "All", "Max"):
      amount = bal[0]

  if bal[1] == bank_lim:
    await ctx.reply(bank_lim_msg)
    return

  if amount == None:
    await ctx.reply("How much coins do you want to deposit?")
    return

  amount = int(amount)
  final_amt = amount + bal[1]

  if final_amt > bank_lim:
    possible_amt = bank_lim - bal[1]
    await ctx.reply(f"You can only deposit {possible_amt} more coins in your bank, bud.")
    return

  else:
    if amount > bal[0]:
      await ctx.reply("You don't have that much coins in your wallet")
      return
    if amount < 1:
      await ctx.reply("You can't deposit less than 1 coin")
      return

    else:
      await update_bank(ctx.author,-1*amount)
      await update_bank(ctx.author,amount,"bank")

      bal = await update_bank(ctx.author)

      embed = discord.Embed(title="Successfully Deposited Money", color=0x000000)
      embed.add_field(name="Deposited",value=amount, inline=False)
      embed.add_field(name="Current Wallet Balance",value=bal[0], inline=False)
      embed.add_field(name="Current Bank Balance",value=bal[1], inline=False)
      await ctx.reply(embed=embed)

@bot.command()
@commands.cooldown(1,20,commands.BucketType.user)
async def dig(ctx):
  await open_account(ctx.author)
  user = ctx.author
  users = await get_bank_data()

  try:
      inventory = users[str(user.id)]["inventory"]
  except:
      inventory = []

  item_list = []
  for item in inventory:
      name = item["item"]
      item_list.append(name)
      
  if "shovel" in item_list:
    bal = await update_bank(ctx.author)

    if bal[0] == wallet_lim:
      await ctx.reply(wallet_lim_msg)
      return

    else:
      fate_number = random.randint(1,10)
      if 1 <= fate_number <= 5:
        earnings = random.randint(1000,20000)
        
        if bal[0] + earnings > wallet_lim:
          actual_earnings = wallet_lim - bal[0]
          await ctx.reply(f"You found {actual_earnings} coins!")
          await update_bank(ctx.author,actual_earnings)
          return
        else:
          await ctx.reply(f"You found {earnings} coins!")
          await update_bank(ctx.author,earnings)
          return

      elif 6 <= fate_number <= 10:
        await ctx.reply("You sadly didn't find any coins...")

  else:
    await ctx.reply("You need a shovel to dig for coins, bud.")
    
@bot.command(aliases=["with"])
async def withdraw(ctx,amount = None):
  await open_account(ctx.author)
  bal = await update_bank(ctx.author)

  if amount in ("all", "max", "All", "Max"):
      amount = bal[1]

  if bal[0] == wallet_lim:
    await ctx.reply(wallet_lim_msg)
    return

  if amount == None:
    await ctx.reply("How much coins do you want to withdraw?")
    return

  amount = int(amount)
  final_amt = amount + bal[0]

  if final_amt > wallet_lim:
    possible_amt = wallet_lim - bal[0]
    await ctx.reply(f"You can only withdraw {possible_amt} more coins, bud.")
    return

  else:
    if amount > bal[1]:
      await ctx.reply("You don't have that much coins in your bank")
      return
    if amount < 1:
      await ctx.reply("You can't withdraw less than 1 coin")
      return

    else:
      await update_bank(ctx.author,amount)
      await update_bank(ctx.author,-1*amount,"bank")

      bal = await update_bank(ctx.author)

      embed = discord.Embed(title="Successfully Withdrew Money", color=0x000000)
      embed.add_field(name="Withdrawn", value=amount, inline=False)
      embed.add_field(name="Current Wallet Balance",value=bal[0], inline=False)
      embed.add_field(name="Current Bank Balance",value=bal[1], inline=False)
      await ctx.reply(embed=embed)

@bot.command()
async def share(ctx,member:discord.Member = None,amount = None):
  if member == None:
    await ctx.reply("Who do you want to share coins to???")
    return

  await open_account(ctx.author)
  await open_account(member)

  if member == ctx.author:
    await ctx.reply("You cannot share money to yourself")
    return
  elif amount == None:
    await ctx.reply("How much coins do you want to share?")
    return

  bal = await update_bank(ctx.author)
  bal2 = await update_bank(member)

  if bal2[0] == wallet_lim:
    await ctx.reply("That person already has the max amount of coins in their wallet")
    return
  if amount in ("all", "All", "max", "Max"):
    amount = bal[0]
  amount = int(amount)
  if amount > bal[0]:
    await ctx.reply("You don't have that much coins in your wallet")
    return
  if bal2[0] + amount > wallet_lim:
    possible_amt = wallet_lim - bal2[0]
    await ctx.reply(f"The max amount of coins u can share to that person is {possible_amt}")
    return
  if amount < 1:
    await ctx.reply("You can't share less than 1 coin")
    return

  await update_bank(ctx.author,-1*amount)
  await update_bank(member,amount)

  await ctx.reply(f"You shared {amount} coins to {member}.")

@bot.command()
@commands.cooldown(1,20,commands.BucketType.user)
async def postmeme(ctx):
  await open_account(ctx.author)
  bal = await update_bank(ctx.author)
  if bal[0] == wallet_lim:
    await ctx.reply(wallet_lim_msg)
    return
  else:
    fates = ["success", "failure"]
    userfate = random.choice(fates)

    if userfate == "success":
      earnings = random.randint(1000,5000)
      if bal[0] + earnings > wallet_lim:
        actual_earnings = wallet_lim - bal[0]
        await update_bank(ctx.author,actual_earnings)
        embed = discord.Embed(title=f"{ctx.author}'s meme posting session", description = f"You posted a funny meme! You earned {actual_earnings} coins for your funny efforts.", color=0x000000)
        await ctx.reply(embed=embed)
        return
        
      else:
        await update_bank(ctx.author,earnings)
        embed = discord.Embed(title=f"{ctx.author}'s meme posting session", description = f"You posted a funny meme! You earned {earnings} coins for your funny efforts.", color = 0x000000)
        await ctx.reply(embed = embed)
        return
        
    elif userfate == "failure":
        embed = discord.Embed(title = f"{ctx.author}'s meme posting session", description = "You posted a bad meme and now everybody is angry at you...", color = 0x000000)
        embed.set_footer("Try harder next time.")
        await ctx.reply(embed = embed)
        return

@bot.command()
@commands.cooldown(1,30,commands.BucketType.user)
async def rob(ctx,member:discord.Member = None):
  if member == None:
    await ctx.reply("Who do you want to rob?")
    return

  await open_account(ctx.author)
  await open_account(member)

  if member == ctx.author:
    await ctx.reply("You cannot rob yourself")
    return

  bal = await update_bank(ctx.author)

  if bal[0] < 5000:
    await ctx.reply("You need at least 5000 coins in your wallet to rob someone, mate.")
    return

  if bal[0] == wallet_lim:
    await ctx.reply(wallet_lim_msg)
    return

  bal = await update_bank(member)
  userbal = await update_bank(ctx.author)

  if bal[0] < 5000:
    await ctx.reply("The victim doesn't have at least 5000 coins in their wallet; robbing them ain't worth it.")
    return

  if bal[0] == wallet_lim:
    await ctx.reply("The victim already has the max amount of coins they can have in their wallet, bud.")
    return

  fates = ["success", "failure"]
  userfate = random.choice(fates)

  if userfate == "success":
    earnings = random.randrange(0, int(bal[0]))

    final_amt = userbal[0] + earnings

    if final_amt > wallet_lim:
      possible_amt = wallet_lim - userbal[0]

      await update_bank(ctx.author,possible_amt)
      await update_bank(member,-1*possible_amt)

      await ctx.reply(f"You robbed {possible_amt} coins from {member}")
      return

    elif final_amt < wallet_lim:
      await update_bank(ctx.author,earnings)
      await update_bank(member,-1*earnings)

      await ctx.reply(f"You robbed {earnings} coins from {member}")
      return

  elif userfate == "failure":
    loss = random.randrange(int(userbal[0]*0.1), int(userbal[0]*0.5))

    member_final_amt = bal[0] + loss

    if member_final_amt > wallet_lim:
      possible_amt = wallet_lim - bal[0]
      await update_bank(ctx.author,-1*possible_amt)
      await update_bank(member,possible_amt)

      await ctx.reply(f"You got caught by the police and had to pay {member} {possible_amt} coins. Better luck next time, bro.")
      return

    elif member_final_amt < wallet_lim:
      await update_bank(ctx.author,-1*loss)
      await update_bank(member,loss)

      await ctx.reply(f"You got caught and had to pay {member} {loss} coins. Better luck next time, bro.")
      return

@bot.command()
@commands.cooldown(1,30,commands.BucketType.user)
async def bankrob(ctx,member:discord.Member = None):
  await open_account(ctx.author)
  await open_account(member)

  if member == None:
    await ctx.reply("Who do you want to bankrob?")
    return

  elif member == ctx.author:
    await ctx.reply("You cannot bankrob yourself")
    return

  bal = await update_bank(ctx.author)

  if bal[0] < 5000:
    await ctx.reply("You need at least 5000 coins in your wallet to bankrob someone, mate.")
    return

  if bal[0] == wallet_lim:
    await ctx.reply(wallet_lim_msg)
    return

  bal = await update_bank(member)

  if bal[1] < 10000:
    await ctx.reply("The victim doesn't have at least 10000 coins in their bank; bankrobbing them ain't worth it.")
    return

  if bal[0] == wallet_lim:
    await ctx.reply(wallet_lim_msg)
    return

  fates = ["success", "failure"]
  userfate = random.choice(fates)

  if userfate == "success":
    earnings = random.randrange(5000,int(bal[1]))

    userbal = await update_bank(ctx.author)

    final_amt_author = userbal[0] + earnings

    if final_amt_author > wallet_lim:
      possible_amt = wallet_lim - userbal[0]

      await update_bank(ctx.author,possible_amt)
      await update_bank(member,-1*possible_amt,"bank")

      await ctx.reply(f"You robbed {possible_amt} coins from {member}'s bank.")
      return

    elif final_amt_author < wallet_lim:
      await update_bank(ctx.author,earnings)
      await update_bank(member,-1*earnings,"bank")

      await ctx.reply(f"You robbed {earnings} coins from {member}'s bank.")
      return

  elif userfate == "failure":
    memberbal = await update_bank(member)
    fine = 5000

    final_amt_member = memberbal[0] + fine

    if final_amt_member > wallet_lim:
      possible_amt = wallet_lim - memberbal[0]
      await update_bank(ctx.author,-1*possible_amt)
      await update_bank(member,possible_amt)

      await ctx.reply(f"You got caught by the police and had to pay a fine of {possible_amt} to {member}.")
      return
    
    elif final_amt_member < wallet_lim:
      await update_bank(ctx.author,-1*fine)
      await update_bank(member,fine)

      await ctx.reply(f"You got caught by the police and had to pay a fine of {fine} to {member}.")
      return

@bot.command()
@commands.cooldown(1,300,commands.BucketType.user)
async def chest(ctx):
  await open_account(ctx.author)
  bal = await update_bank(ctx.author)

  if bal[0] == wallet_lim:
    await ctx.reply(wallet_lim_msg)
    return
  elif bal[0] + 20000 > wallet_lim:
    await ctx.reply("You can't open a chest anymore since your wallet might burst lol")
    return
  else:
    earnings = random.randint(0,20000)
    if earnings == 0:
      await ctx.reply("Your chest is empty. Better luck next time, buddy")
      return
    else:      
      await update_bank(ctx.author,earnings)
      await ctx.reply(f"You have found {earnings} coins in your chest")
      return

@bot.command()
@commands.cooldown(1,30,commands.BucketType.user)
async def gamble(ctx,amount=None):
  await open_account(ctx.author)
  bal = await update_bank(ctx.author)

  if bal[0] == wallet_lim:
    await ctx.reply(wallet_lim_msg)
    return
  if amount == None:
    await ctx.reply("How much coins do you want to gamble?")
    return
  if amount in ("all", "All", "max", "Max"):
    amount = bal[0]

  amount = int(amount)
  final_amt_positive = amount + bal[0]
  max_earnings_under_a_thousand = 999
  
  if wallet_lim - bal[0] <= max_earnings_under_a_thousand:
    await ctx.reply("Sorry but you can't bet anything since you almost have the max amount of coins you can have in your wallet")
    return
  elif amount < 1:
    await ctx.reply("You can't bet less than 1 coin")
    return
  elif amount < 1000:
    await ctx.reply("Sorry but you can't gamble less than 1000 coins")
    return
  elif bal[0] < 1000:
    await ctx.reply("You need at least 1000 coins in your wallet to gamble")
    return
  elif amount > bal[0]:
    await ctx.reply("You don't have that much money in your wallet")
    return
  elif final_amt_positive > wallet_lim:
    await ctx.reply("You can't bet that much because if you win, you're going to have more money than you can in your wallet.")
    return
  else:
    userroll = random.randint(1,12)
    botroll = random.randint(1,12)
    earnings = amount

    if userroll > botroll:
      await update_bank(ctx.author,earnings)
      bal = await update_bank(ctx.author)
      embed=discord.Embed(title=f"{ctx.author}'s Gambling Game", description=f"You won {earnings} coins", color=0x000000)
      embed.add_field(name="Current Wallet Balance", value=f"{bal[0]} coins", inline=False)
      embed.add_field(name=f"{ctx.author}", value=f"Rolled {userroll}", inline=True)
      embed.add_field(name="Bye Dank Memer", value=f"Rolled {botroll}", inline=True)
      embed.set_footer(text="Congratulations!")
      await ctx.reply(embed=embed)
      return
    elif userroll < botroll:
      await update_bank(ctx.author,-1*earnings)
      bal = await update_bank(ctx.author)
      embed=discord.Embed(title=f"{ctx.author}'s Gambling Game", description=f"You lost {earnings} coins", color=0x000000)
      embed.add_field(name="Current Wallet Balance", value=f"{bal[0]} coins", inline=False)
      embed.add_field(name=f"{ctx.author}", value=f"Rolled {userroll}", inline=True)
      embed.add_field(name="Bye Dank Memer", value=f"Rolled {botroll}", inline=True)
      embed.set_footer(text="Better luck next time!")
      await ctx.reply(embed=embed)
      return
    elif userroll == botroll:
      embed=discord.Embed(title=f"{ctx.author}'s Gambling Game", description="It was a tie, so you didn't lose anything :)", color=0x000000)
      embed.add_field(name="Current Wallet Balance", value=f"{bal[0]} coins", inline=False)
      embed.add_field(name=f"{ctx.author}", value=f"Rolled {userroll}", inline=True)
      embed.add_field(name="Bye Dank Memer", value=f"Rolled {botroll}", inline=True)
      embed.set_footer(text="You didn't win, but the good thing is you didn't lose")
      await ctx.reply(embed=embed)
      return

@bot.command()
@commands.cooldown(1,30,commands.BucketType.user)
async def snakeeyes(ctx, amount=None):
  await open_account(ctx.author)
  bal = await update_bank(ctx.author)

  if bal[0] == wallet_lim:
    await ctx.reply(wallet_lim_msg)
    return
  if amount == None:
    await ctx.reply("How much coins do you want to bet?")
    return
  if amount in ("all", "All", "max", "Max"):
    amount = bal[0]

  amount = int(amount)
  earnings_doublese = amount*10
  final_amt_positive = bal[0] + earnings_doublese
  max_earnings_under_a_thousand = 999*10

  if wallet_lim - final_amt_positive <= max_earnings_under_a_thousand:
    await ctx.reply("Sorry but you can't bet anything since you almost have the max amount of coins you can have in your wallet")
    return
  elif final_amt_positive > wallet_lim:
    await ctx.reply("You can't bet that much because if you get double snake eyes, you're going to have more money than you can in your wallet.")
    return
  elif amount < 1:
    await ctx.reply("You can't bet less than 1 coin")
    return
  elif amount < 1000:
    await ctx.reply("Sorry but you can't gamble less than 1000 coins")
    return
  elif bal[0] < 1000:
    await ctx.reply("You need at least 1000 coins in your wallet to gamble")
    return
  elif amount > bal[0]:
    await ctx.reply("You don't have that much money in your wallet")
    return
  else:
    roll1 = random.randint(1,6)
    roll2 = random.randint(1,6)
    earnings = amount

    if roll1 == 1 and roll2 == 1:
      await update_bank(ctx.author,round(earnings*10))
      bal = await update_bank(ctx.author)
      embed=discord.Embed(title=f"{ctx.author}'s Gambling Game", description=f"2 EYES! You have won {round(earnings*10)} coins, 10x of what you have bet", color=0x000000)
      embed.add_field(name="Current Wallet Balance", value=f"{bal[0]} coins", inline=False)
      embed.add_field(name="Roll 1", value=f"Rolled {roll1}", inline=True)
      embed.add_field(name="Roll 2", value=f"Rolled {roll2}", inline=True)
      embed.set_footer(text="Congratulations!")
      await ctx.reply(embed=embed)
      return
    elif roll1 == 1 or roll2 == 1:
      await update_bank(ctx.author,round(earnings*1.5))
      bal = await update_bank(ctx.author)
      embed=discord.Embed(title=f"{ctx.author}'s Gambling Game", description=f"At least there was still an eye. You have won {round(earnings*1.5)} coins, 1.5x of what you have bet", color=0x000000)
      embed.add_field(name="Current Wallet Balance", value=f"{bal[0]} coins", inline=False)
      embed.add_field(name="Roll 1", value=f"Rolled {roll1}", inline=True)
      embed.add_field(name="Roll 2", value=f"Rolled {roll2}", inline=True)
      embed.set_footer(text="At least you won some money :)")
      await ctx.reply(embed=embed)
      return
    else:
      await update_bank(ctx.author,-1*earnings)
      bal = await update_bank(ctx.author)
      embed=discord.Embed(title=f"{ctx.author}'s Gambling Game", description=f"There wasn't an eye at all. You have lost {earnings} coins", color=0x000000)
      embed.add_field(name="Current Wallet Balance", value=f"{bal[0]} coins", inline=False)
      embed.add_field(name="Roll 1", value=f"Rolled {roll1}", inline=True)
      embed.add_field(name="Roll 2", value=f"Rolled {roll2}", inline=True)
      embed.set_footer(text="Better luck next time!")
      await ctx.reply(embed=embed)
      return

@bot.command()
@commands.cooldown(1,3,commands.BucketType.user)
async def shop(ctx):
  embed=discord.Embed(title="Shop", description="Buy and Sell Items!", color=0x000000)

  for item in mainshop:
    name = item["name"]
    price = item["price"]
    description = item["description"]
    embed.add_field(name = name, value = f"{price} | {description}")

  await ctx.reply(embed=embed)

@bot.command()
@commands.cooldown(1,3,commands.BucketType.user)
async def buy(ctx,item,amount = 1):
  await open_account(ctx.author)

  res = await buy_this(ctx.author,item,amount)

  if not res[0]:
    if res[1]==1:
      await ctx.reply("That object doesn't exist lol.")
      return
    if res[1]==2:
          await ctx.reply(f"Sorry, but you're too broke to buy {amount} {item}.")
          return

  await ctx.reply(f"You just bought {amount} {item}")

@bot.command(aliases=["inv"])
@commands.cooldown(1,3,commands.BucketType.user)
async def inventory(ctx, member = discord.Member):
  if member == None:
    await open_account(member)
    user = member
    users = await get_bank_data()

    try:
      inventory = users[str(user.id)]["inventory"]
    except:
      inventory = []

    embed = discord.Embed(title = f"{member}'s Inventory", color = 0x000000)
    for item in inventory:
      name = item["item"]
      amount = item["amount"]

      embed.add_field(name = name, value = amount)

    await ctx.reply(embed = embed)
    return

  else:
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    try:
      inventory = users[str(user.id)]["inventory"]
    except:
      inventory = []

    embed = discord.Embed(title = "Your Inventory", color = 0x000000)
    for item in inventory:
      name = item["item"]
      amount = item["amount"]

      embed.add_field(name = name, value = amount)
  
    await ctx.reply(embed = embed)
    return

async def open_account(user):
  users = await get_bank_data()

  if str(user.id) in users:
    return False
  else:
    users[str(user.id)] = {}
    users[str(user.id)]["wallet"] = 5000
    users[str(user.id)]["bank"] = 0

  with open("mainbank.json", "w") as f:
    json.dump(users,f)
  return True

async def get_bank_data():
  with open("mainbank.json", "r") as f:
    users = json.load(f)
  return users

async def update_bank(user,change = 0,mode = "wallet"):
  users = await get_bank_data()

  users[str(user.id)][mode] += change

  with open("mainbank.json", "w") as f:
    json.dump(users,f)

  bal = [users[str(user.id)]["wallet"],users[str(user.id)]["bank"]]
  return bal

async def buy_this(user,item_name,amount):
  item_name = item_name.lower()
  name_ = None
  for item in mainshop:
    name = item["name"].lower()
    if name == item_name:
      name_ = name
      price = item["price"]
      break
  
  if name_ == None:
    return [False,1]
  
  cost = price*amount

  users = await get_bank_data()

  bal = await update_bank(user)

  if bal[0]<cost:
    return [False,2]

  try:
    index = 0
    t = None
    for thing in users[str(user.id)]["inventory"]:
      n = thing["item"]
      if n == item_name:
        old_amt = thing["amount"]
        new_amt = old_amt + amount
        users[str(user.id)]["inventory"][index]["amount"] = new_amt
        t = 1
        break
      index+=1
    if t == None:
      obj = {"item":item_name , "amount" : amount}
      users[str(user.id)]["inventory"].append(obj)

  except:
    obj = {"item":item_name , "amount" : amount}
    users[str(user.id)]["inventory"] = [obj]

  with open("mainbank.json","w") as f:
    json.dump(users,f)
  
  await update_bank(user,cost*-1,"wallet")

  return [True,"Worked"]

@bot.command()
@commands.cooldown(10,60,commands.BucketType.user)
async def height(ctx,name=None):
  height = random.randint(130,200)
  if name == None:
    embed=discord.Embed(title='Height Machine', description=f'You are {height} cm tall', color=0x000000)
    await ctx.reply(embed=embed)
  else:
    embed = discord.Embed(title='Height Machine', description=f'{name} is {height} cm tall', color = 0x000000)
    await ctx.reply(embed=embed)

@bot.command()
@commands.cooldown(10,60,commands.BucketType.user)
async def greetings(ctx,language=None):
  if language == None:
    await ctx.reply("Hello!")
  else:
    if language in ("english", "English"):
      await ctx.reply("Hello!")
    elif language in ("bahasa", "Bahasa"):
      await ctx.reply("Halo!")
    elif language in ("chinese", "Chinese", "mandarin", "Mandarin"):
      await ctx.reply("你好！")
    else:
      await ctx.reply("Language currently not supported. Sorry!")

@bot.command()
@commands.cooldown(1,120,commands.BucketType.user)
async def userping(ctx,member:discord.Member=None,amt=None):
  if member == None:
    await ctx.reply("Who do you want to ping?")
  else:
    if amt == None:
      await ctx.reply(f"<@!{member.id}>")
    else:
      amt = int(amt)
      for u in range(amt):
        await ctx.reply(f"<@!{member.id}>")

@bot.command()
@commands.cooldown(10,60,commands.BucketType.user)
async def simprate(ctx,name = None):
  if name == None:
    percentage = random.randint(0,100)
    embed=discord.Embed(title="Simp Rate Machine", description=f"You are {percentage}% simp", color=0x000000)
    await ctx.reply(embed=embed)
  else:
    percentage = random.randint(0,100)
    embed=discord.Embed(title="Simp Rate Machine", description=f"{name} is {percentage}% simp", color=0x000000)
    await ctx.reply(embed=embed)
    return

@bot.command()
@commands.cooldown(10,60,commands.BucketType.user)
async def attractive(ctx,name = None):
  if name == None:
    percentage = random.randint(0,100)
    embed = discord.Embed(title="Attractive Rate Machine", description = f"You are {percentage}% attractive", color=0x000000)
    await ctx.reply(embed=embed)
  else:
    percentage = random.randint(0,100)
    embed = discord.Embed(title="Attractive Rate Machine", description = f"{name} is {percentage}% attractive", color=0x000000)
    await ctx.reply(embed=embed)

@bot.command()
@commands.cooldown(10,30,commands.BucketType.user)
async def calculate(ctx,operation=None,value1=None,value2=None):
  if operation == None:
    embed = discord.Embed(title='Calculator',description='Here is the list of operations',color=0x000000)
    embed.add_field(name='1. Addition', value='Format: b!calculate 1 <number 1> <number 2>',inline=False)
    embed.add_field(name='2. Subtraction', value='Format: b!calculate 2 <number 1> <number 2>', inline=False)
    embed.add_field(name='3. Multiplication', value='Format: b!calculate 3 <number 1> <number 2>', inline=False)
    embed.add_field(name='4. Division', value='Format: b!calculate 4 <number 1> <number 2>', inline=False)
    embed.set_footer(text=f'Hope it helps, {ctx.author}!')
    await ctx.reply(embed=embed)

  elif value1 == None:
    await ctx.reply("You should enter 2 numbers after the operation number \nType b!calculate for more info")
    return

  elif value2 == None:
    await ctx.reply("You should also enter a 2nd number \nType b!calculate for more info")
    return

  operation = int(operation)
  value1 = int(value1)
  value2 = int(value2)

  if operation == 1:
    await ctx.reply(f"{value1} + {value2} = {add(value1,value2)}")
    return
  elif operation == 2:
    await ctx.reply(f"{value1} - {value2} = {subtract(value1,value2)}")
    return
  elif operation == 3:
    await ctx.reply(f"{value1} x {value2} = {multiply(value1,value2)}")
    return
  elif operation == 4:
    if value2 == 0:
      await ctx.reply("You can't divide by 0")
      return
    else:
      await ctx.reply(f"{value1} / {value2} = {divide(value1,value2):.2f}")
      return
  else:
    await ctx.reply("Please enter a valid operation")
    return
@bot.command()
@commands.cooldown(10,60,commands.BucketType.user)
async def ship(ctx,person1=None,person2=None):
  if person1 == None:
    await ctx.reply("Who do you want to ship?")
    return
  else:
    percentage = random.randint(0,100)
    if 0 <= percentage < 10:
      description = "way too bad"
    elif 10 <= percentage < 19:
      description = "extremely bad"
    elif 20 <= percentage < 30:
      description = "very bad"
    elif 30 <= percentage < 40:
      description = "bad"
    elif 40 <= percentage < 50:
      description = "below average"
    elif 50 <= percentage < 60:
      description = "average"
    elif 60 <= percentage < 70:
      description = "above average"
    elif 70 <= percentage < 80:
      description = "good"
    elif 80 <= percentage < 90:
      description = "very good"
    elif 90 <= percentage < 100:
      description = "extremely good"
    elif percentage == 100:
      description = "PERFECT"

    if person1 in ("Myself", "myself", "Me", "me") and person2 == None:
      embed=discord.Embed(title="Ship Machine", description=f"How suitable are you and yourself for each other?", color=0x000000)
      embed.add_field(name="Ship %", value=f"{percentage} ({description})", inline=False)
      await ctx.reply(embed=embed)
      return

    elif person2 == None:
      embed=discord.Embed(title="Ship Machine", description=f"How suitable are you and {person1} for each other?", color=0x000000)
      embed.add_field(name="Ship %", value=f"{percentage} ({description})", inline=False)
      await ctx.reply(embed=embed)
      return

    else:
      embed=discord.Embed(title="Ship Machine", description=f"How suitable are {person1} and {person2} for each other?", color=0x000000)
      embed.add_field(name="Ship %", value=f"{percentage} ({description})", inline=False)
      await ctx.reply(embed=embed)
      return
  
@bot.command()
@commands.cooldown(10,60,commands.BucketType.user)
async def eightball(ctx,question=None):
  emoji = "\N{BILLIARDS}"
  if question == None:
    await ctx.reply("What do you want to ask the 8ball?")
    return
  else:
    replies = ["Yess, definitely!!!", "The answer is a big NO", "Yes?", "No?", "Perhaps", "Now's not the right time to tell you the answer"]
    reply = random.choice(replies)    
    await ctx.reply(f"{emoji} {reply}")
  
@bot.command()
@commands.cooldown(10,60,commands.BucketType.user)
async def crystalball(ctx,question=None):
  if question == None:
    await ctx.reply("What do you want to ask the crystal ball?")
    return
  else:
    await ctx.reply("Please wait for a few seconds as the crystal ball thinks...")
    time.sleep(5)
    replies = ["yess, definitely!!!", "the answer is a big NO", "yes?", "no?", "perhaps", "now's not the right time to tell you the answer"]
    reply = random.choice(replies)    
    await ctx.reply(f"The crystal ball says, {reply}")
    return

@bot.command()
@commands.cooldown(1,600,commands.BucketType.user)
async def work(ctx):
  await open_account(ctx.author)
  user = ctx.author
  users = await get_bank_data()

  try:
      inventory = users[str(user.id)]["inventory"]
  except:
      inventory = []

  item_list = []
  for item in inventory:
      name = item["item"]
      item_list.append(name)
      
  if "laptop" in item_list:
    bal = await update_bank(ctx.author)

    if bal[0] == wallet_lim:
      await ctx.reply(wallet_lim_msg)
      return

    else:
        earnings = random.randint(1000,20000)
        
        if bal[0] + earnings > wallet_lim:
          actual_earnings = wallet_lim - bal[0]
          await ctx.reply(f"Your boss gave you {actual_earnings} coins!")
          await update_bank(ctx.author,actual_earnings)
          return
        else:
          await ctx.reply(f"Your boss gave you {earnings} coins!")
          await update_bank(ctx.author,earnings)
          return

  else:
    await ctx.reply("You need a laptop to work, bud.")
  
@bot.command()
@commands.cooldown(10,60,commands.BucketType.user)
async def waifu(ctx,name = None):
  if name == None:
    percentage = random.randint(0,100)
    embed = discord.Embed(title="Waifu Rate Machine",description=f"You are {percentage}% waifu",color=0x000000)
    await ctx.reply(embed=embed)
    return
  else:
    percentage = random.randint(0,100)
    embed = discord.Embed(title="Waifu Rate Machine",description=f"{name} is {percentage}% waifu",color=0x000000)
    await ctx.reply(embed=embed)
    return

@bot.command()
@commands.cooldown(1,120,commands.BucketType.user)
async def spam(ctx,song=None):
  if song == None:
    embed = discord.Embed(title="Songs I can sing/spam", description="1. Rickroll (type in rickroll after b!spam) \n2. Jebait (type in jebait after b!spam)", color=0x000000)
  emoji1 = "\N{MANS SHOE}"
  emoji2 = "\N{STUDIO MICROPHONE}"
  emoji3 = "\N{FROG FACE}"

  if song == "rickroll":
    f = open("rickroll.txt", "r")
    for word in f:
      await ctx.send(word)
    await ctx.send(f"{emoji1} {emoji2}")

  elif song == "jebait":
    f = open("jebait.txt", "r")
    for word in f:
      await ctx.send(word)
    await ctx.send(f"{emoji3}")
    
  else:
    await ctx.reply("Sorry, I haven't memorised the lyrics to that song yet")

@bot.command()
@commands.cooldown(1,3,commands.BucketType.user)
async def quote(ctx):
  quotes = ["Never gonna give you up", "Never gonna let you down", "Never gonna run around and desert you",
  "Never gonna make you cry", "Never gonna say goodbye", "Never gonna tell a lie and hurt you", "Ducks are infinitely powerful"]
  await ctx.reply(f"{random.choice(quotes)}")

@bot.command()
@commands.cooldown(1,3,commands.BucketType.user)
async def pickupline(ctx):
  pickup_lines = ["You are the E to my mc^2", "You are my sin 90 degrees and only", "You are my tan 45 degrees and only", 
  "You are my sin^2x + cos^2x and only", "I code in Java, and you're the ;s of my code", "Our relationship is like a covalent bond; it is very strong",
  "sqrt(-1) love you to the edge of the universe and back", "Astronauts need to go to space to see the world, but I only need to look into your eyes",
  "Could you replace my x without asking y?"]
  await ctx.reply(f"{random.choice(pickup_lines)}")

@bot.command()
@commands.cooldown(1,3,commands.BucketType.user)
async def ping(ctx):
  await ctx.reply(f'Your ping is {round (bot.latency * 1000)} ms')

@bot.command()
async def timenow(ctx):
  time = datetime.datetime.now().strftime("It is %I:%M %p right now.")
  await ctx.reply(time)
  return

bot.run("token")
