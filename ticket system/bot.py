from tkinter.ttk import Style
import discord
from discord.ext import commands
from config import *
from discord.ui import Button, View
intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command(name="ticket")
@commands.has_role(954724999984459836)
async def ticket(ctx):
    embed = discord.Embed(
        title = "Sunucu Adı",
        description ="Açıklama yazısı\n Falan filan",
        colour = discord.Colour.random()
    )
    await ctx.send(embed=embed)
    button = Button(label="Ticket Oluştur", style=discord.ButtonStyle.green)
    button2 = Button(label="Ticket Sil", style=discord.ButtonStyle.red)
    async def button_callback(interaction):
        guild = interaction.guild
        admin_role = interaction.guild.get_role(954724999984459836) #Ticket yetkilisinin id'sini giriniz
        member = interaction.user

        overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        member: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        admin_role: discord.PermissionOverwrite(read_messages=True, send_messages=True),
    }
        channel = await interaction.guild.create_text_channel(f'ticket-{interaction.user.name}', reason=None, category=None, news=False, overwrites=overwrites)
        await channel.send(f'<@{interaction.user.id}> Adlı Kullanıcı Bir Destek Talebi Oluşturdu Birazdan <@&954724999984459836> Yetkisi Sahip Kişiler Yardım İçin Gelicekler')
        
    button.callback = button_callback
    button2.callback = button_callback

    view = View()
    view.add_item(button)
    await ctx.send(view=view)



#ticket komutu kullanılınca bot o kanala ticket mesajını atacak ve buton ekliyecek butona tıklayınca ticket odası açılacak
#açılan odaya bot kapatma butonu ve normal mesajın bulunduğu mesajı atıcak ve sadece ticket sahibi ile yetkili ekibin görmesi için ayarlıaycak
#kapatma butonuna basınca bot sohbeti txt olarak kaydedip log kanalına atıcak ve ticketi kapatıcak

###############################################################################

@bot.event
async def on_ready():
    print(bot.user.name)
    await bot.change_presence(activity=discord.Game(name="<3 LEO4BEY")) 

bot.run(token)

#LEO4BEY TARAFINDAN YAZILMIŞTIR İZİNSİZ PAYLAŞILMASI YASAKTIR
#SOT [ÇAKA BEYLİĞİ] Sunucusu için Yazılmıştır
