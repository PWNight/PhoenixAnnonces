import discord
from discord.ext.commands.bot import Bot
import asyncio
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
    if message.guild is None and not message.author.bot:
        if memberop.id in voprosmembers:
            await memberop.send(resno)
            return
        if not memberop.id in voprosmembers:
                global countervopros
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
                for attachment in message.attachments:
                    try:
                        if attachment.content_type.startswith("image/") and len(message.attachments) == 1:
                            countervopros += 1
                            voprosmembers.append(memberop.id)
                            annonce = discord.Embed(description=f'{message.content}', color = 0x2f3136)
                            annonce.set_image(url=f'{attachment.url}')
                            annonce.set_author(name=f"{message.author}", icon_url = message.author.display_avatar.url)
                            msgtic = await channel.send(embed=annonce, view=view)
                            embyes = discord.Embed(title= f'<:phoenix_verify:953725334770040953> Объявление на проверке.', description=f'Ваше объявление отправлено на проверку модерацией.', color = 0x2f3136)
                            await memberop.send(embed = embyes)
                    except asyncio.TimeoutError:
                        print("Неизвестная ошибка в коде вопросов / Тикетов") 
                    else:
                        if len(message.attachments) > 1:
                            await message.author.send(content='<:phoenix_error:954067706074775622> Публикация автоматически отклонена. В объвлении можно отправить не более 1-го изображения.')
                            voprosmembers.remove(memberop.id)
                            return
                        if not attachment.content_type.startswith("image/"):
                            await message.author.send(content='<:phoenix_error:954067706074775622> Публикация автоматически отклонена. Вложение не является изображением.')
                            voprosmembers.remove(memberop.id)
                            return   
                if not message.attachments:
                    countervopros += 1
                    voprosmembers.append(memberop.id)
                    annonce = discord.Embed(description=f'{message.content}', color = 0x2f3136)
                    annonce.set_author(name=f"{message.author}", icon_url = message.author.display_avatar.url)
                    msgtic = await channel.send(embed=annonce, view=view)
                    embyes = discord.Embed(title= f'<:phoenix_verify:953725334770040953> Объявление на проверке.', description=f'Ваше объявление отправлено на проверку модерацией.', color = 0x2f3136)
                    await memberop.send(embed = embyes)
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
                        embyes = discord.Embed(title= f'<:phoenix_verify:953725334770040953> Объявление принято.', description=f'В результате проверки ваше __объявление было принято__ модератором `{m.author}` __и отправлено__ в <#939578152060084335>.', color = 0x2f3136)
                        embyes.set_footer(text = f'{m.author}', icon_url = f'{m.author.display_avatar.url}')
                        await message.author.send(embed = embyes)
                        await msgtic.delete()
                        return
                    if m.component.custom_id == "denyann":
                        voprosmembers.remove(memberop.id)
                        embno = discord.Embed(title= f'<:phoenix_verify:953725334770040953> Объявление отклонено.', description=f'В результате проверки ваше __объявление было отклонено__ модератором `{m.author}`.', color = 0x2f3136)
                        embno.set_footer(text = f'{m.author}', icon_url = f'{m.author.display_avatar.url}')
                        await message.author.send(embed = embno)
                        await msgtic.delete()
                        return
bot.run('OTQyMzc2Mzg3ODMzMTA2NDUy.YgjmZw.6WA7I1R4ZIBZZmXdvgpD_szowSE')