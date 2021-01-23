import os
import asyncio
import functools
import discord
from discord.ext import commands
import youtube_dl

youtube_dl.utils.bug_reports_message = lambda: ""

queue = []

#class VoiceError(Exception):
    #pass


#class YTDLError(Exception):
	#pass
	#await ctx.send('Music nicht gefunden')


class PlayCommand(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='play')
	async def play(self, ctx, url):
		voicec = ctx.author.voice
		if voicec:
			channel = voicec.channel
			if channel:

				songname = f'songs/{ctx.guild.id}_current.mp3'
				#songname = f'songs/{ctx.guild.id}_current.opus'
				song_there = os.path.isfile(songname)
				try:
					if song_there:
						os.remove(songname)
						print('removed old song file')
				except PermissionError:
					print('Trying to delete song file, but it is being player')
					await ctx.send('Error Music playing')
					return
					

				#voice = await channel.connect()
				voice = ctx.message.guild.voice_client
				#await ctx.send('➡️ Verbunden mit dem Voicechannel!')
				ydl_opts = {
					'format': 'bestaudio/best',
					'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
					'default_search': 'auto',
					'noplaylist': True,
					'postprocessors': [{
						'key': 'FFmpegExtractAudio',
						#'preferredcodec': 'mp3',
						'preferredcodec': 'opus',
						'preferredquality': '192'
					}]
				}
				
				if voice.is_playing():
					queue.append(str(url))
					print(queue)
					await ctx.send("📥 Music wurde auf die Playlist hinzugefügt!")
				
				else:
					async def bot_play_music():
						voice = ctx.message.guild.voice_client
						
						voice.play(discord.FFmpegPCMAudio(songname), after=await queue_check())
						voice.source = discord.PCMVolumeTransformer(voice.source)
						voice.source.volume = 1.00
						if len(queue) > 0:
							await ctx.send(f"📀 Music ({queue[0]}) wird jetzt abgespielt!")
						else:
							await ctx.send(f'📀Music wird abgespielt!')
						print('Ok.')
						
					async def download_convert(name):
						
						if song_there:
							os.remove(songname)
							print("Alte Datei gelöscht.")

						with youtube_dl.YoutubeDL(ydl_opts) as ydl:
							print('Downloading audio now\n')
							await ctx.send('🔍 Suche Music auf YouTube')
							ydl.download(name)
						
						for file in os.listdir('./'):
							#if file.endswith('.mp3'):
							if file.endswith('.opus'):
								print(f'Renamed File: {file}\n')
								os.rename(file, songname)
								await ctx.send('✅ Music wurde gefunden!')
						
						await bot_play_music()


					async def queue_check():
						
						if len(queue) > 0 and len(queue) != 0:
							await download_convert(queue[0])
							queue.remove(queue[0])
						else:
							print("Queue gestoppt")


					
					
					await download_convert([url])

		else:
			await ctx.send('❌ Du bist in keinem Voice Channel')
