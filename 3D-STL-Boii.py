import StlToGif
import shutil
import discord
import sys
import random
import urllib
import asyncio
import aiohttp
import os

from concurrent.futures import ThreadPoolExecutor

TOKEN = sys.argv[1]

args = ["-i", "replacethis", "-o", "replacethis", "--elevation", "45", "--duration", "replacethis", "--nframes", "replacethis"]

client = discord.Client()

async def asyncDownloadFile(URL, destinationFile):
	async with aiohttp.ClientSession() as session:
		async with session.get(URL) as response:
			print("Starting async download call")
			if response.status == 200:
				data = await response.read()

				print("Response is 200")

				file = open(destinationFile, 'wb')
				file.write(data)
				file.close()

				print("File written")

@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if not message.attachments:
		return

	for attachment in message.attachments:

		filename = attachment.filename

		print(filename)

		if filename.lower().endswith(".stl"):
			
			response = "Looks like a .stl file! I'll attempt to render it :)"
			
			url = attachment.url
			id = str(attachment.id)

			os.mkdir(id)

			compositeFilename = id + os.sep + filename

			await asyncDownloadFile(url, compositeFilename)
			newArgs = args
			
			frames = 200
			time_to_rotate = 8
			time_per_frame = time_to_rotate / frames

			newArgs[1] = compositeFilename
			newArgs[3] = compositeFilename
			newArgs[7] = time_per_frame
			newArgs[9] = frames

			newArgs.append("--path")
			newArgs.append(id + os.sep + "frames" + os.sep)

			notification_message = await message.channel.send("Work work work...")

			try:
				StlToGif.main(newArgs)
				print("Attempting to send: " + compositeFilename + ".gif")
				await message.channel.send(file=discord.File(compositeFilename + ".gif", filename + ".gif"))
				shutil.rmtree(id)
			except:
				await message.channel.send("Your file do not seem valid :(")
			await notification_message.delete()

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')

client.run(TOKEN)