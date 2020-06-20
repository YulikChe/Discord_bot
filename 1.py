import discord
from data import data
import datetime
import asyncio
from discord.ext import commands
import re
import random

TOKEN = 'TOKEN'

bot = commands.Bot(command_prefix='/') #инициализируем бота с префиксом '/'

#жалоба
@bot.command(pass_context=True)
async def compl(ctx, member: discord.Member, *args):
    reason = ""
    for i in args:
        reason += i + " "

    await ctx.channel.purge(limit=1)
    await ctx.send("Жалоба отправлена на оброботку!")
    print("Милорд! " + str(ctx.author) + "подал жалобу на " + str(member) + " по причине " + reason + "!")

    answer = input()
    if answer == "Y":
        await ctx.send("Жалоба отправленна!")
        with open("compls.txt", "r+") as f:
            text = f.read()

            pattern = str(member) + " had compl"
            rec2 = re.findall(pattern, text)
            person_compl = len(rec2) + 1
            if person_compl < 3:
                await member.send("Здрасте, на вас подали жалобу на Yulik_cheServ с таким текстом: " + reason + "! Поетому вы получаете предупреждение! Ещё " + str(3-person_compl) + " предупреждения и бан!")

                f.write(str(member) + " had compl\n")
            if person_compl == 3:
                await member.send("Здрасте, на вас подали жалобу на Yulik_cheServ с таким текстом: " + reason + "! Это третие предупреждение и вы получаете бан! Спасибо за понимание!")

                f.write(str(member) + " had ban\n")

                await ctx.send("Баним!")
                await member.ban(reason="3 предупреждения")
                emb = discord.Embed(title='Забанен! :thumbsup:', colour=discord.Color.red())
                emb.set_author(name=member.name, icon_url=member.avatar_url)
                emb.set_footer(text="Причина бана: получил 3 предупреждения", icon_url=bot.user.avatar_url)

                await ctx.send(emb)

    if answer == "N":
        await ctx.send("Жалоба не принята!")

#Connected
@bot.event
async def on_ready():
    print("BOT connected")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('/Info'))


#выдача роли
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(712302372830838834)
    role = discord.utils.get(member.guild.roles, id=708666321910628402)

    await member.add_roles(role)
    await channel.send("Приветсвую тебя " + member.name + " с присоединением к нашему серверу! Не забудь прочитать правила!")

#если чел ушёл
@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(691916930864644096)
    await channel.send(str(member) + " покинул чат")

#нажатие
#@bot.event
#async def on_typing(ctx, member, time):
#    role = discord.utils.get(member.guild.roles, id=716670048303054891)
#    if int(time.hour) == 23:
#        await member.add_roles(role)
#        await ctx.send(f"{member.mention}Ну и че не спишь? И да это пасхалка! Ты уже получил свою роль!")

#golosovalka
@bot.event
async def on_raw_reaction_remove(payLoad):
    with open('ID_GOLOSOVALKI', "r+") as f:
        message_id_need_for_golos = f.read()

    channel = bot.get_channel(payLoad.channel_id)
    message = await channel.fetch_message(payLoad.message_id)
    member = discord.utils.get(message.guild.members, id=payLoad.user_id)
    emoji = str(payLoad.emoji.name)
    emoji2 = ""
    if emoji == "👍":
        emoji2 = "+"
    if emoji == "👎":
        emoji2 = "-"

    if message.id == int(message_id_need_for_golos):
        with open("GOLOSA_GOLOSOVALKI", "r+") as f:
            gg = f.read()
        gg2 = gg.split(str(member) + " had golos " + str(emoji2))
        gg3 = ''
        for i in gg2:
            gg3 = f"{str(gg3)}{str(i)}"
        with open("GOLOSA_GOLOSOVALKI", "w") as f:
            f.write(gg3)


#ssp and golosovalka
@bot.event
async def on_raw_reaction_add(payLoad): #0 - stone, 1 - scissors, 2 - paper
    with open('ID_GOLOSOVALKI', "r+") as f:
        message_id_need_for_golos = f.read()

    p_bet = 3
    comp_bet = random.randint(0, 2)
    channel = bot.get_channel(payLoad.channel_id)
    message = await channel.fetch_message(payLoad.message_id)
    member = discord.utils.get(message.guild.members, id=payLoad.user_id)
    emoji = str(payLoad.emoji.name)
    #для голосовалки
    if str(message.id) == message_id_need_for_golos:
        pattern = str(member) + " had golos"
        if emoji == "👍" or emoji == "👎":
            with open('GOLOSA_GOLOSOVALKI', "r+") as gg1:
                ggg = gg1.read()
                rec2 = re.findall(pattern, ggg)
                golosa_member = len(rec2)
                if golosa_member < 1:
                    if emoji == "👍":
                        gg1.write(f"{member} had golos +")
                    if emoji == "👎":
                        gg1.write(f"{member} had golos -")
                else:
                    await message.remove_reaction(payLoad.emoji, member)
        else:
            await message.remove_reaction(payLoad.emoji, member)


    if str(message.author) == "TESTBOT#1119":
        if emoji == "stone":
            p_bet = 0
        elif emoji == "scissors":
            p_bet = 1
        elif emoji == "paper":
            p_bet = 2

        if comp_bet == 0:#если у бота камень
            if p_bet == 0:
                await channel.send(f"{member.mention}Моя ставка: камень. Твоя ставка: камень. Это ничья!")
            elif p_bet == 1:
                await channel.send(f"{member.mention}Моя ставка: камень. Твоя ставка: ножници. Я выиграл!")
            elif p_bet == 2:
                await channel.send(f"{member.mention}Моя ставка: камень. Твоя ставка: бумага. Ты выиграл!")

        elif comp_bet == 1:#если у бота ножници
            if p_bet == 0:
                await channel.send(f"{member.mention}Моя ставка: ножницы. Твоя ставка: камень. Ты выиграл!")
            elif p_bet == 1:
                await channel.send(f"{member.mention}Моя ставка: ножницы. Твоя ставка: ножници. Это ничья!")
            elif p_bet == 2:
                await channel.send(f"{member.mention}Моя ставка: ножницы. Твоя ставка: бумага. Я выиграл!")

        elif comp_bet == 2:#если у бота бумага
            if p_bet == 0:
                await channel.send(f"{member.mention}Моя ставка: бумага. Твоя ставка: камень. Я выиграл!")
            elif p_bet == 1:
                await channel.send(f"{member.mention}Моя ставка: бумага. Твоя ставка: ножници. Ты выиграл!")
            elif p_bet == 2:
                await channel.send(f"{member.mention}Моя ставка: бумага. Твоя ставка: бумага. Это ничья!")


#про мой видос
@commands.has_permissions(administrator=True)
@bot.command(pass_context=True)
async def YT(ctx, url):
    await ctx.channel.purge(limit=1)
    channel = bot.get_channel(716319427506733127)
    await channel.send("На канале моего создателя(Yulik_che) вышёл видос! " + str(url) + " Не забудь посмотреть!:thumbsup:")


#say
@bot.command(pass_context=True) #разрешаем передавать агрументы
async def say(ctx, *args): #создаем асинхронную фунцию бота
    say = ""
    for i in args:
        say += i + " "
    await ctx.send(say) #отправляем обратно аргумент

#ban
@bot.command(pass_context=True)
async def ban(ctx, member: discord.Member, *args):
    arg2 = ""
    for i in args:
        arg2 += i + " "

    await ctx.send("Запрос на бан " + str(member) + " по причине " + arg2 + " отправлен!")
    print("Милорд! Народ хочет бана " + str(member) + " по причине " + arg2 + "!")
    print("Согласны?")
    answer = input()
    if answer == "Y":
        await ctx.send("Баним!")
        await member.ban(reason=arg2)
        emb = discord.Embed(title='Забанен! :thumbsup:', colour=discord.Color.red())
        emb.set_author(name=member.name, icon_url=member.avatar_url)
        emb.set_footer(text="Причина бана: " + arg2, icon_url=bot.user.avatar_url)

        await ctx.send(embed=emb)
    if answer == "N":
        await ctx.send("Не баним!")

        emb = discord.Embed(title='Не забанен!', colour=discord.Color.green())

        emb.set_author(name=member.name, icon_url=member.avatar_url)
        emb.set_footer(text="Указаная причина для бана: " + arg2, icon_url=bot.user.avatar_url)

        await ctx.send(embed=emb)

#unban
@commands.has_permissions(administrator=True)
@bot.command(pass_context=True)
async def unban(ctx, userr):
    banned_users = await ctx.guild.bans()
    for ban_entry in banned_users:
        user = ban_entry.user
        if userr == str(user):
            await ctx.guild.unban(user)
            emb = discord.Embed(title='Разбанен! :thumbsup:', colour=discord.Color.green())

            emb.set_author(name=user.name, icon_url=user.avatar_url)
            await ctx.send(embed=emb)


#clear
@commands.has_permissions(administrator=True)
@bot.command(pass_context=True)
async def clear(ctx, amount=1000000000000000000000000000):
    await ctx.channel.purge(limit=amount)

#kick
@bot.command(pass_context=True)
async def kick(ctx, member: discord.Member, *args):
    arg2 = ""
    for i in args:
        arg2 += i + " "

    await ctx.send("Запрос на кик " + str(member) + " по причине " + arg2 + " отправлен!")
    print("Милорд! Народ хочет кика " + str(member) + " по причине " + arg2 + "!")
    print("Согласны?")
    answer = input()
    if answer == "Y":
        await ctx.send("Кикаем!")
        await member.kick(reason=arg2)
        emb = discord.Embed(title='Кикнут! :thumbsup:', colour=discord.Color.red())
        emb.set_author(name=member.name, icon_url=member.avatar_url)
        emb.set_footer(text="Причина кика: " + arg2, icon_url=bot.user.avatar_url)

        await ctx.send(embed=emb)
    if answer == "N":
        await ctx.send("Не кикаем!")

        emb = discord.Embed(title='Не кикнут!', colour=discord.Color.green())

        emb.set_author(name=member.name, icon_url=member.avatar_url)
        emb.set_footer(text="Указаная причина для кика: " + arg2, icon_url=bot.user.avatar_url)

        await ctx.send(embed=emb)

#Info
@bot.command(pass_context=True)
async def Info(ctx):
    await ctx.send("Я бот Yulik_che! Мой префикс /, Я могу вот что:"
                   "\n1. /say (что-то) повторю то что вы здесь напишете"
                   "\n2. /ban (кто) (за что) отправлю запрос на бан"
                   "\n3. /Haha отправлю случайный анекдот из архива"
                   "\n4. /Add_haha (анекдот) отправляю запрос на добавление анекдота"
                   "\n5. /kick (кого) (за что) отправляю запрос на кик"
                   "\n6. /compl (кого)(за что) отправлю жалобу")

#Haha
@bot.command(pass_context=True)
async def Haha(ctx):
    await ctx.send(data["anekdots"][random.randint(0, len(data["anekdots"]) - 1)])


#голосовалка
@commands.has_permissions(administrator=True)
@bot.command(pass_context=True)
async def goloso(ctx, hour, minute, *args):
    await ctx.channel.purge(limit=1)
    text = ""
    for i in args:
        text += i + " "

    emb = discord.Embed(title=text, colour=discord.Color.gold())
    emb.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
    emb.set_footer(text="👍 - да, 👎 - нет\n"
                        "Голосование до " + hour + ":" + minute)
    await ctx.send(embed=emb)
    with open("ID_GOLOSOVALKI", "w") as f:
        f.write(str(ctx.channel.last_message_id))

    with open("GOLOSA_GOLOSOVALKI", "w") as f:
        pass

    #time = datetime.time(hour=int(hour), minute=int(minute))

    #while not bot.is_closed:
    #    print("test")
    #    if datetime.datetime.now().time().hour == time.hour:
    #        await ctx.send("test")
    #        break


#добавить анекдот
@bot.command(pass_context=True)
async def Add_haha(ctx, *args):
    await ctx.send("Запрос отправлен!")
    an = ""
    for i in args:
        an += i + " "
    print("Милорд народ хочет добавить анекдот:" + an + "Добавлять?")
    answer = input()
    if answer == "Y":
        data["anekdots"].append(an)
        await ctx.send("Добавленно! :thumbsup:")
    if answer == "N":
        await ctx.send("Не добавлено!")

#Kамень ножницы бумага
@bot.command(pass_context=True)
async def ssp(ctx):
    await ctx.send("Ок! Ставь ставку!")


#@commands.has_permissions(administrator=True)
#@bot.command(pass_context=True)
#async def rainbow(ctx):
#    colors = [124252, 5020550, 250154, 139, 1783434, 2552555, 255215, 25569, 2525112, 191255, 3413934]
#    server = ctx.guild
#    role = discord.utils.get(server.roles, name='Любитель посхалочек🕶️')
#    while True:
#        for i in colors:
#            await role.edit(color=discord.Colour(i))
#            await asyncio.sleep(0.1)

@commands.has_permissions(administrator=True)
@bot.command(pass_context=True)
async def PMaf(ctx, *args):
    members = args
    members2 = []
    for i in members:
        members2.append(discord.utils.get(ctx.message.guild.members, name=i))
    member_len = len(members)
    roles = []
    maf = False     #мафия есть ли
    dma = False     #дон есть ли
    kom = False     #комисар есть ли
    doc = False     #док есть ли

    await MafAlgo(member_len, roles, maf, dma, kom, doc, 1)

    for i in range(0, member_len):
        await members2[i].send("Твоя роль: " + roles[i])

async def MafAlgo(member_len, roles, maf, dma, kom, doc, couter):
    if couter <= member_len+1:
        if couter <= member_len:
            rand = random.randint(1, member_len)
            if rand == 1:
                if maf == False:
                    roles.append("мафия")
                    maf2 = True
                    await MafAlgo(member_len, roles, maf2, dma, kom, doc, couter + 1)
                else:
                    await MafAlgo(member_len, roles, maf, dma, kom, doc, couter)
            elif rand == 2:
                if dma == False:
                    roles.append("донмафия")
                    dma2 = True
                    await MafAlgo(member_len, roles, maf, dma2, kom, doc, couter + 1)
                else:
                    await MafAlgo(member_len, roles, maf, dma, kom, doc, couter)
            elif rand == 3:
                if kom == False:
                    roles.append("комисар")
                    kom2 = True
                    await MafAlgo(member_len, roles, maf, dma, kom2, doc, couter + 1)
                else:
                    await MafAlgo(member_len, roles, maf, dma, kom, doc, couter)
            elif rand == 4:
                if doc == False:
                    roles.append("док")
                    doc2 = True
                    await MafAlgo(member_len, roles, maf, dma, kom, doc2, couter + 1)
                else:
                    await MafAlgo(member_len, roles, maf, dma, kom, doc, couter)
            else:
                roles.append("мирный")
                await MafAlgo(member_len, roles, maf, dma, kom, doc, couter + 1)
        else:
            await sglagivanie_bagov_maf(member_len, roles, maf, dma, kom, doc)

async def sglagivanie_bagov_maf(len, roles, maf, dma, kom, doc):
    if maf == False:
        rand = random.randint(0, len-1)
        if roles[rand] == "мирный":
            roles[rand] = "мафия"
        else:
            await sglagivanie_bagov_maf(len, roles, maf, dma, kom, doc)
    if dma == False:
        rand = random.randint(0, len - 1)
        if roles[rand] == "мирный":
            roles[rand] = "донмафия"
        else:
            await sglagivanie_bagov_maf(len, roles, maf, dma, kom, doc)
    if kom == False:
        rand = random.randint(0, len - 1)
        if roles[rand] == "мирный":
            roles[rand] = "комисар"
        else:
            await sglagivanie_bagov_maf(len, roles, maf, dma, kom, doc)
    if doc == False:
        rand = random.randint(0, len-1)
        if roles[rand] == "мирный":
            roles[rand] = "док"
        else:
            await sglagivanie_bagov_maf(len, roles, maf, dma, kom, doc)

@commands.has_permissions(administrator=True)
@bot.command(pass_context=True)
async def PMaf2(ctx, *args):
    members = args
    members2 = []
    for i in members:
        members2.append(discord.utils.get(ctx.message.guild.members, name=i))
    member_len = len(members)
    roles = []
    maf = False     #мафия есть ли
    dma = False     #дон есть ли
    doc = False     #doc есть ли

    await MafAlgo2(member_len, roles, maf, dma, doc, 1)

    for i in range(0, member_len):
        await members2[i].send("Твоя роль: " + roles[i])

async def MafAlgo2(member_len, roles, maf, dma, doc, couter):
    if couter <= member_len+1:
        if couter <= member_len:
            rand = random.randint(1, member_len)
            if rand == 1:
                if maf == False:
                    roles.append("мафия")
                    maf2 = True
                    await MafAlgo2(member_len, roles, maf2, dma, doc, couter + 1)
                else:
                    await MafAlgo2(member_len, roles, maf, dma, doc, couter)
            elif rand == 2:
                if dma == False:
                    roles.append("донмафия")
                    dma2 = True
                    await MafAlgo2(member_len, roles, maf, dma2, doc, couter + 1)
                else:
                    await MafAlgo2(member_len, roles, maf, dma, doc, couter)
            elif rand == 3:
                if doc == False:
                    roles.append("доктор")
                    doc2 = True
                    await MafAlgo2(member_len, roles, maf, dma, doc2, couter + 1)
                else:
                    await MafAlgo2(member_len, roles, maf, dma, doc, couter)
            else:
                roles.append("мирный")
                await MafAlgo2(member_len, roles, maf, dma, doc, couter + 1)
        else:
            await sglagivanie_bagov_maf2(member_len, roles, maf, dma, doc)

async def sglagivanie_bagov_maf2(len, roles, maf, dma, doc):
    if maf == False:
        rand = random.randint(0, len-1)
        if roles[rand] == "мирный":
            roles[rand] = "мафия"
        else:
            await sglagivanie_bagov_maf2(len, roles, maf, dma, doc)
    if dma == False:
        rand = random.randint(0, len - 1)
        if roles[rand] == "мирный":
            roles[rand] = "донмафия"
        else:
            await sglagivanie_bagov_maf2(len, roles, maf, dma, doc)
    if doc == False:
        rand = random.randint(0, len - 1)
        if roles[rand] == "мирный":
            roles[rand] = "докор"
        else:
            await sglagivanie_bagov_maf2(len, roles, maf, dma, doc)

bot.run(TOKEN)