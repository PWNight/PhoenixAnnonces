import discord
from discord.ext.commands.bot import Bot
import asyncio
import os
import discord.utils
from discord.ext import commands
import disnake as discord
from disnake.ext import commands
from disnake.ui import Button, View

bot = commands.Bot(command_prefix= r'//', intents = discord.Intents.all())
bot.remove_command('help')
voprosmembers = []
countervopros = 0
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name=f"Напиши мне в ЛС сообщение, чтобы я опубликовал его в объявлениях."))
    print('Анонсы активированы.')
@bot.event
async def on_message(message):
    channel = bot.get_channel(956205925973229658) # ID канала с логами.
    channel2 = bot.get_channel(939578152060084335) # ID канала с логами.
    memberop = message.author
    resno = '<:phoenix_error:954067706074775622> Ваше предыдущее объявление ещё находится на проверке. Вы не можете отправить объявление, пока предыдущее не будет проверено.'
    resyes = '<:phoenix_verify:953725334770040953> Принял! Ваша публикация была отправлена на проверку. Мы оповестим вас о результатах проверки сообщением ниже.'
    if message.guild is None and not message.author.bot:
        if memberop.id in voprosmembers:
            await memberop.send(resno)
            return
        if not memberop.id in voprosmembers:
                global countervopros
                countervopros += 1
                voprosmembers.append(memberop.id)
                await memberop.send(resyes)
                annonce = discord.Embed(description=f'{message.content}', color = 0x2f3136)
                annonce.set_author(name=f"{message.author}", icon_url = message.author.display_avatar.url)
                row = Button(
                        style = discord.ButtonStyle.green,
                        label = 'Одобрить публикацию',
                        custom_id = 'acceptann',
                        emoji= '<:phoenix_verify:953725334770040953>'
                    )
                row2 = Button(
                        style = discord.ButtonStyle.danger,
                        label = 'Отклонить публикацию',
                        custom_id = 'denyann',
                        emoji= '<:phoenix_deny:953725334539358308>'
                    )
                view=View()
                view.add_item(row)
                view.add_item(row2)
                files = []
                for attachment in message.attachments:
                    try:
                        if attachment.content_type.startswith("image/"):
                            files.append(await attachment.to_file())
                    except:
                        continue
                msgtic = await channel.send(embed=annonce, view=view, files = files)
                def check(m):
                    return m.message.id == msgtic.id and m.author.guild_permissions.manage_messages == True
                try:
                   m = await bot.wait_for("button_click", check=check)
                except asyncio.TimeoutError:
                    print("Неизвестная ошибка в коде Тикетов") 
                else:
                    if m.component.custom_id == "acceptann":
                        voprosmembers.remove(memberop.id)
                        await channel2.send(embed = annonce)
                        await message.author.send(content='<:phoenix_verify:953725334770040953> Ваше объявление одобрено и было опубликовано.')
                        await msgtic.delete()
                        return
                    if m.component.custom_id == "denyann":
                        voprosmembers.remove(memberop.id)
                        await message.author.send(content=f'<:phoenix_error:954067706074775622> Текст вашей публикации не прошёл проверку. Публикация отклонена модератором {m.author}')
                        await msgtic.delete()
                        return
bot.run('OTQyMzc2Mzg3ODMzMTA2NDUy.YgjmZw.6WA7I1R4ZIBZZmXdvgpD_szowSE')