import asyncio
import discord

import frosch2010_Console_Utils as fCU


async def send_edit_embed_msg(term, term_words, tabuLanguage, channel):

    embed = discord.Embed(title=tabuLanguage.tabu_card_term_prefix + term, description=tabuLanguage.tabu_edit_description, color=0x22a7f0)
    embed.add_field(name="###############################", value=term_words.replace(",", "\n"), inline=True)

    botMessage = await channel.send(embed=embed)

    await botMessage.add_reaction("✏️")
    await botMessage.add_reaction("✂️")
    await botMessage.add_reaction("🗑")
    await botMessage.add_reaction("✅")

    return botMessage



async def remove_user_from_edit_list_if_possible(user, tabuVars):

    if user.id in tabuVars.tabu_edit_delete_word_list:

        del tabuVars.tabu_edit_delete_word_list[user.id]


    if user.id in tabuVars.tabu_edit_delete_card_list:

        try:
            await tabuVars.tabu_edit_delete_card_list[user.id].delete()
        except:
            fCU.log_In_Console("Failed to delete 'edit delete card'-message.", "EDITSYS-RMU", "err")

        del tabuVars.tabu_edit_delete_card_list[user.id]


    if user.id in tabuVars.tabu_edit_messages_list:

        del tabuVars.tabu_edit_term_list[tabuVars.tabu_edit_messages_list[user.id][1].content.replace(tabuVars.tabu_edit_messages_list[user.id][1].content.split(" ")[0] + " ", "")]

        for msg in tabuVars.tabu_edit_messages_list[user.id][0]:
            try:
                await msg.delete()
            except:
                fCU.log_In_Console("Failed to delete edit message.", "EDITSYS-RMU", "err")

        del tabuVars.tabu_edit_messages_list[user.id]


    if user.id in tabuVars.tabu_edit_word_list:

        del tabuVars.tabu_edit_word_list[user.id]



async def delete_edit_msgs(reaction_msg, edit_msgs):

    for msg in edit_msgs:
        try:
            await msg.delete()
        except:
            fCU.log_In_Console("Failed to delete edit message.", "EDITSYS-DEL-MSGS", "err")

    try:
        await reaction_msg.delete()
    except:
        fCU.log_In_Console("Failed to delete edit reaction message.", "EDITSYS-DEL-MSGS", "err")