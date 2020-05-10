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

TOKEN = sys.argv[1]
client = discord.Client()

#Just some function to retrieve the attachment
async def async_download_file(url, destinationFile):
	async with aiohttp.ClientSession() as session:
		async with session.get(url) as response:
			if response.status == 200:
				data = await response.read()
				file = open(destinationFile, 'wb')
				file.write(data)
				file.close()

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

			#Generic vars
			url = attachment.url
			render_id = str(attachment.id)
			original_filename = attachment.filename
			stl_file_location = render_id + os.sep + original_filename

			#Render tweaks
			number_of_frames = 150
			time_to_rotate = 8

			#Create attachment specific directory
			os.mkdir(render_id)

			#Retrieve model
			await async_download_file(url, stl_file_location)

			#Begin render
			notification_message = await message.channel.send("Work work work...")
			try:
				rendered_gif = render_stl_attachment(stl_file_location, render_id, number_of_frames, time_to_rotate)
				print("Attempting to send: " + rendered_gif)
				await message.channel.send(file=discord.File(rendered_gif, original_filename + ".gif"))

				#Clean up
				shutil.rmtree(render_id)
			except:
				logging.exception("message")
				#Sad noises to user
				await message.channel.send("Your file does not seem valid :(")

			#Remove the notification
			await notification_message.delete()

#Renders a gif and returns the location of the gif
def render_stl_attachment(stl_file, render_id, number_of_frames, time_to_rotate):
		
		#Calculate render specific parameters
		time_per_frame = time_to_rotate / number_of_frames
		frames_location = render_id + os.sep + "frames" + os.sep
		render_filename = render_id + os.sep + "render.gif"

		#Get attachment specific render parameters
		render_args = get_render_args(stl_file, render_filename, time_per_frame, number_of_frames, frames_location)

		#Do the thing
		StlToGif.main(render_args)
		
		return render_filename

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('----------------------------------')

client.run(TOKEN)