import discord
from discord.ext import commands
from config import *
import asyncio
import datetime
import json
import os
from discord.ui import Button, View
intents = discord.Intents.all()
intents.message_content = True


today = datetime.datetime.now()
date_time = today.strftime("%d/%m/%Y  %H.%M.%S")
saat = today.strftime("%H %M %S")
tarih = today.strftime("%d/%m/%Y  %H.%M")

path = (r'C:\Users\Administrator\Desktop\deneme\ticket system\ticketlog')#buraya botun klaşörünün konumunu girin - entry your bot file location


class LeoTicketSil(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Ticket Sil', style=discord.ButtonStyle.red, custom_id='leo_ticket_sil:red', emoji="🔒")
    async def red(self, interaction: discord.Interaction, button: discord.ui.Button):
        log_channel = bot.get_channel(log_ch)
        channel01 = interaction.channel

        

        LeoTicketSilmeLog = discord.Embed(
            title = "__Bir Ticket Silindi__",
            description = " ● **Ticketi Silen Kişinin Adı** \n ''" + interaction.user.name +
            "''\n ● **Ticketi Silen Kişinin id'si** \n ''" + str(interaction.user.id) +
            "''\n ● **Ticket Kanal id'si** \n" + str(interaction.channel.id) +"''",
            colour = discord.Colour.red()
        )
        LeoTicketSilmeLog.set_footer(text=footer)
        await interaction.response.send_message(f"Ticket Silme Talebi Alındı `{channel01.name}` Adlı kanal **5** saniye içerisinde silinicektir")
        await log_channel.send(embed=LeoTicketSilmeLog, file=discord.File(f'ticket-{interaction.channel.id}.txt'))
        await asyncio.sleep(5) # Kanalı butona bastıktan 5 saniye sonra silmesi için ekledim kanalın direkt silinmesini istiyorsan satırı silebilirsin - 5 secs timeout for bot delete channel if you don't want timeout you can delete this line
        await channel01.delete()

class LeoTicketOlustur(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Ticket Oluştur', style=discord.ButtonStyle.green, custom_id='leo_ticket_olustur:green', emoji="🎫")
    async def green(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        admin_role = interaction.guild.get_role(admin) 
        member = interaction.user
        tcktcategory = discord.utils.get(guild.categories, name="leoticket") #Ticketin oluşturulacağı katogorinin adı - bot will create ticket in this categories

        overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        member: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        admin_role: discord.PermissionOverwrite(read_messages=True, send_messages=True),
    }

        LeoTicketMesaj = discord.Embed(
        title = "Destek Talebi",
        description = f'Bir Kullanıcı Destek Talebi Oluşturdu \n Birazdan <@&{admin}> Yetkisi Sahip Kişiler Yardım İçin Gelicekler', #yetkili rol id girin - entry yourticket support role id
        colour = discord.Colour.random()
        )
        LeoTicketMesaj.set_footer(text=footer)

        view= LeoTicketSil()
        channel4 = await interaction.guild.create_text_channel(f'ticket-{interaction.user.name}', reason=None, category=tcktcategory, news=False, overwrites=overwrites)
        await channel4.send(f'<@{interaction.user.id}> , <@&{admin}>', embed=LeoTicketMesaj, view=view) #yetkili rol id girin - entry your ticket support role id

        log_channel = bot.get_channel(log_ch)
        with open(f'ticket-{channel4.id}.txt', 'w+') as fp:
            fp.write(f'Ticket Olusturulma Zamani: {date_time} \nTicket Olusturan Kisi Adi: {interaction.user} \nTicket Olusturan Kisi id: {interaction.user.id}\n- - - - - - - - - -\n')
            fp.close()
            @bot.event
            async def on_message(message):
                if channel4.id == message.channel.id:
                    with open (f'ticket-{channel4.id}.txt', 'a+') as fp:
                        fp.write(f'{message.author} : {message.content}\n- - - - - - - - - -\n')
                        fp.close()
        def write_json(new_data, filename="ticket-info.json"):
            with open(filename, "r+") as file:
                file_data = json.load(file)
                file_data["ticket-info"].append(new_data)
                file.seek(0)
                json.dump(file_data, file, indent = 4)
        y = {f"id": channel4.id,
             "name": interaction.user.name,
             "userid": interaction.user.id,
             "create-date": date_time
            }
        write_json(y)
        LeoTicketOlusturmaLog = discord.Embed(
            title = "__Bir Ticket Oluşturuldu__",
            description = " ● **Ticketi Oluşturan Kullanıcının Adı** \n ''" + interaction.user.name +
            "''\n ● **Ticketi Oluşturan Kullanıcının id'si** \n ''" + str(interaction.user.id) +
            "''\n ● **Ticket Kanal id'si** \n " + str(interaction.channel.id) + "''",
            colour = discord.Colour.green()
        )
        LeoTicketOlusturmaLog.set_footer(text=footer)
        await log_channel.send(f'<#{channel4.id}>', embed=LeoTicketOlusturmaLog)

class LeoButtonListener(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(command_prefix=commands.when_mentioned_or('$'), intents=intents) # $ yerine prefixinizi yazabilirsiniz - you can prefix here currentprefix is $

    async def setup_hook(self) -> None:
        self.add_view(LeoTicketOlustur())
        self.add_view(LeoTicketSil())


bot = LeoButtonListener()
@bot.command(name="ticket-kur")
@commands.has_permissions(administrator = True)
async def ticket(ctx):
    LeoTicketEmbed = discord.Embed(
        title = f'{servernm} Ticket System',
        description ="Destek talebi oluşturmak için\nalt kısımdaki butona tıklayınız\nGereksiz kullananlar ceza alacaktır",
        colour = discord.Colour.green()
    )
    LeoTicketEmbed.set_footer(text=footer)
    view = LeoTicketOlustur()
    await ctx.send(embed=LeoTicketEmbed, view=view)


@bot.event 
async def on_ready():
    print(bot.user.name)
    print("Bot Açılma Saati: ", date_time)
    await bot.change_presence(activity=discord.Game(name=footer)) # Parantez içerisindeki kısım botun oynuyor kısımı - bot activity status

bot.run(token)

#LEO4BEY TARAFINDAN YAZILMIŞTIR İZİNSİZ PAYLAŞILMASI YASAKTIR
#https://www.leo4bey.com