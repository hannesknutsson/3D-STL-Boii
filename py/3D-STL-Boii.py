import StlToGif
import shutil
import discord
import sys
import random
import urllib
import asyncio
import aiohttp
import os
import logging
import hashlib

TOKEN = sys.argv[1]
client = discord.Client()

@client.event
async def on_message(message):

	#Don't respond to bots
	if message.author == client.user:
		return

	#Don't respond if there are no attachments
	if not message.attachments:
		return

	for attachment in message.attachments:

		#We don't even try rendering non STL files
		if attachment.filename.lower().endswith(".stl"):

			#Make sure there is a gif cache directory
			gif_cache_dir = "gif_cache"
			try:
				os.mkdir(gif_cache_dir)
			except:
				pass

			#Begin working
			notification_message = await message.channel.send("Work work...")
			try:
				gif = await get_gif(attachment, gif_cache_dir)
				#Finish the job
				print("Attempting to send: " + gif)
				await message.channel.send(file=discord.File(gif, attachment.filename + ".gif"))
			except:
				#Sad noises to user
				await message.channel.send("Something went wrong while processing your file :(")
				logging.exception("message")

#Gets a gif from the specified attachment, will never render the same attachment twice
async def get_gif(attachment, gif_cache_dir):
	
	#Working dir for this attachment
	working_dir = str(attachment.id)

	try:
		os.mkdir(working_dir)

		#Download that attachment baby
		stl_file_location = working_dir + os.sep + attachment.filename
		await async_download_file(attachment.url, stl_file_location)

		#Calculate hash
		file_hash = str(await hash_file(stl_file_location))

		print("File hash:", file_hash)

		#Have we already done this?
		cached_gif = await get_gif_from_cache(file_hash, gif_cache_dir)

		if cached_gif != None:
			#There was a cached gif!
			print("THERE IS NO CACHED GIF", cached_gif)
			return cached_gif
		else:
			#We have to render it once again..
			output_location = gif_cache_dir + os.sep + file_hash + ".gif"
			render_stl_model(stl_file_location, working_dir, output_location)
			return output_location
	finally:
		try:
			shutil.rmtree(working_dir)
		except:
			pass

#Hashes a fule, duh
async def hash_file(file_to_hash):

	BLOCK_SIZE = 65536
	file_hash = hashlib.sha256()

	with open(file_to_hash, 'rb') as file_handle:
		chunk = 0
		while chunk != b'':
			chunk = file_handle.read(BLOCK_SIZE)
			file_hash.update(chunk)

	hash_result = file_hash.hexdigest()

	return hash_result

#Retrieves a cached gif
async def get_gif_from_cache(stl_hash, gif_cache_dir):
	for cached_gif in os.listdir(gif_cache_dir):
		if cached_gif == stl_hash + ".gif":
			return gif_cache_dir + os.sep + cached_gif

#Renders a gif and returns the location of the gif
def render_stl_model(input_location, working_dir, output_location):
		
	#Render tweaks
	number_of_frames = 150
	time_to_rotate = 8

	#Calculate render specific parameters
	time_per_frame = time_to_rotate / number_of_frames
	frames_location = working_dir + os.sep + "frames" + os.sep
	render_filename = working_dir + os.sep + "render.gif"

	#Get attachment specific render parameters
	render_args = get_render_args(input_location, render_filename, time_per_frame, number_of_frames, frames_location)

	#Do the thing
	StlToGif.main(render_args)

	#Move it where it should go
	print(render_filename)
	print(output_location)
	shutil.move(render_filename, output_location)

#Compiles appropriate arguments for the gif rendering script
def get_render_args(input_file, output_file, time_per_frame, number_of_frames, frames_location):
	newArgs = []
	newArgs.append("-i")
	newArgs.append(input_file)
	newArgs.append("-o")
	newArgs.append(output_file)
	newArgs.append("--elevation")
	newArgs.append("45")
	newArgs.append("--duration")
	newArgs.append(str(time_per_frame))
	newArgs.append("--nframes")
	newArgs.append(str(number_of_frames))
	newArgs.append("--path")
	newArgs.append(frames_location)
	return newArgs

#Just some function to retrieve the attachment
async def async_download_file(url, destinationFile):
	async with aiohttp.ClientSession() as session:
		async with session.get(url) as response:
			if response.status == 200:
				data = await response.read()
				file = open(destinationFile, 'wb')
				file.write(data)
				file.close()

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('----------------------------------')

client.run(TOKEN)