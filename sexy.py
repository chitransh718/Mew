import asyncio
import re
import random
from telethon import TelegramClient, events
from telethon.errors import MessageIdInvalidError
from collections import deque

api_id = '29848170'
api_hash = 'e2b1cafae7b2492c625e19db5ec7f513'
session = '"1BVtsOH8Bu4FVmqgUEOPlLr_eCNE1LLZG6HYP-byyEwqkhlgqEBSnKD-E5R4mxJolZHfOx-X0Lpgjr3ApU_a0E-q2kaz7wUErqCWCVJxU4ZsMYasvF63OJEn553RXpFIi0SMnmJS1XHCQthYKksRnNba_Of3eOzUEyM95ftNoqTurHv_Ft-M0_tgmmM7x9ZYKf6EfFGEwjbsIlmf7rjcDv6gsOHt9vlQiRWiGc48tXAT02QHAuYMOy-e6nSOPB40p4l3BO6GufwiSnOkCtVdkIbQq9zukLHPLHq18iNlpUI6-Khx87E3McikCNEBVeEn_36KSurj6k9Pm67qCHfo0fAaOL1VXjzA='

# Add a flag to track if the 4th button has been clicked
clicked_4th_button = False

last_two_messages = deque(maxlen=2)

async def main():
    client = TelegramClient('your_session_file.session', api_id, api_hash)

    def check_for_shiny(messages):
        for message in messages:
            if "✨ Shiny pokemon found!" in message:
                return True
        return False
    

    @client.on(events.NewMessage(from_users=572621020))

    async def handle_message(event):
        try:
            global clicked_4th_button
            global last_two_messages

            if event.is_private:
                # Check for HP information and click buttons accordingly
                # (your previous code remains the same)

                # Update the last two messages deque
                last_two_messages.append(event.raw_text)

                # Check if "✨ Shiny pokemon found!" is in the last two messages
                shiny_found = check_for_shiny(last_two_messages)
                if shiny_found:
                    print("Shiny Pokemon found! Stopping the script.")
                    await client.disconnect()  # Disconnect the client to stop the script

        except (asyncio.TimeoutError, MessageIdInvalidError):
            pass


    @client.on(events.NewMessage(from_users=572621020))
    async def _(event):
        global clicked_4th_button 
        if event.is_private and "A wild" in event.raw_text:
            if event.is_private and any(keyword in event.raw_text for keyword in ["A wild Cyndaquill", "A wild Totodile", "A wild Ampharos", "A wild Espeon", "A wild Scizor", "A wild Heracross", "A wild Houndour", "A wild Houndoom", "A wild Blissey", "A wild Tyranitar", "A wild Lugia", "A wild Ho-Oh", "A wild Celebi","A wild Venusaur", "A wild Houndoom" , "A wild Blastoise", "A wild Porygon", "A wild Beedrill", "A wild Pidgeot", "A wild Alakazam", "A wild Slowbro", "A wild Kangaskhan", "A wild Pinsir", "A wild Gyarados", "A wild Aerodactyl", "A wild Charizard ", "A wild Mewtwo ", "A wild Gengar", "A wild Charmander", "A wild Bulbasaur", "A wild Squirtle", "A wild Magikarp", "A wild Abra", "A wild Gastly", "A wild Snorlax",  "A wild Treecko", "A wild Sceptile", "A wild Torchic", "A wild Blaziken", "A wild Mudkip", "A wild Swampert", "A wild Taillow", "A wild Gardevoir", "A wild Gallade", "A wild Slakoth", "A wild Nincada", "A wild Sableye", "A wild Mawile", "A wild Aggron", "A wild Medicham", "A wild Electrike", "A wild Manectric", "A wild Sharpedo", "A wild Camerupt", "A wild Trapinch", "A wild Altaria", "A wild Banette", "A wild Absol", "A wild Glalie", "A wild Bagon", "A wild Salamence", "A wild Beldum", "A wild Metang", "A wild Metagross", "A wild Kyogre", "A wild Groudon", "A wild Rayquaza", "A wild Deoxys", "A wild Chimchar", "A wild Piplup", "A wild Starly", "A wild Buneary", "A wild Lopunny", "A wild Gible", "A wild Gabite", "A wild Garchomp", "A wild Munchlax", "A wild Riolu", "A wild Lucario", "A wild Abomasnow", "A wild Dialga", "A wild Regigigas", "A wild Giratina", "A wild Arceus", "A wild Timburr", "A wild Gurdurr", "A wild Venipede", "A wild Sandile", "A wild Darumaka", "A wild Dwebble", "A wild Scraggy", "A wild Karrablast", "A wild Frillish", "A wild Litwick", "A wild Axew", "A wild Shelmet", "A wild Mienfoo", "A wild Druddigon", "A wild Golett", "A wild Rufflet", "A wild Braviery", "A wild Durant", "A wild Deino", "A wild Larvesta", "A wild Reshiram", "A wild Zekrom", "A wild Kyurem", "A wild Victini", "A wild Genesect", "A wild Chespin", "A wild Fennekin", "A wild Froakie", "A wild Frogadier", "A wild Greninja", "A wild Flabébé", "A wild Floette", "A wild Sylveon", "A wild Hawlucha", "A wild Goomy", "A wild Bergmite", "A wild Noibat", "A wild Noivern", "A wild Avalugg", "A wild Xerneas", "A wild Yveltal", "A wild Zygarde", "A wild Diancie", "A wild Rowlet", "A wild Litten", "A wild Popplio", "A wild Grubbin", "A wild Mudbray", "A wild Passimian", "A wild Wimpod", "A wild Golisopod", "A wild Minior", "A wild Turtonator", "A wild Jangmo-o", "A wild Hakamo-o", "A wild Tapu Koko", "A wild Tapu Lele", "A wild Tapu Fini", "A wild Cosmog", "A wild Cosmoem", "A wild Solgaleo", "A wild Lunala", "A wild Buzzwole", "A wild Pheromosa", "A wild Guzzlord", "A wild Necrozma", "A wild Magearna", "A wild Marshadow", "A wild Poipole", "A wild Stakataka", "A wild Blacephalon", "A wild Zeraora", "A wild Venusaur", "A wild Charizard", "A wild Blastoise", "A wild Beedrill", "A wild Pidgeot", "A wild Alakazam", "A wild Slowbro", "A wild Gengar", "A wild Kangaskhan", "A wild Pinsir", "A wild Gyarados", "A wild Aerodactyl", "A wild Aerodactyl", "A wild Ampharos", "A wild Steelix", "A wild Scizor", "A wild Heracross", "A wild Houndoom", "A wild Tyranitar", "A wild Sceptile", "A wild Blaziken", "A wild Swampert", "A wild Gardevoir", "A wild Sableye", "A wild Mawile", "A wild Aggron", "A wild Medicham", "A wild Manectric", "A wild Sharpedo", "A wild Camerupt", "A wild Altaria", "A wild Banette", "A wild Absol", "A wild Glalie", "A wild Salamence", "A wild Metagross", "A wild Lopunny", "A wild Garchomp", "A wild Lucario", "A wild Abomasnow", "A wild Gallade", "A wild Audino", "A wild Deino" ,"A wild Zamazenta" ,"A wild Zacian" ,"A wild Eternatus" ,"A wild Spectrier" ,"A wild Duraludon", ]):
                await asyncio.sleep(1)  
                clicked_4th_button = False  # Set the flag to True
                await event.click(0) 
            else:
                await asyncio.sleep(1)  
                await event.client.send_message(572621020, "/hunt")
                clicked_4th_button = False  # Set the flag to True

    @client.on(events.MessageEdited(from_users=572621020))
    async def _(event):
        global clicked_4th_button 
        if event.is_private and "HP" in event.raw_text:
            for button_row in event.buttons:
                for button in button_row:
                    if button.text in ['Regular', 'Charmeleon']:
                        await asyncio.sleep(1)
                        await button.click()
                        clicked_4th_button = False  # Set the flag to True
                        break  # Stop searching for buttons once either 'Repeat' or 'Nincada' is found

    @client.on(events.MessageEdited(from_users=572621020))
    async def _(event):
        global clicked_4th_button 
        if event.is_private and any(keyword in event.raw_text for keyword in ["The wild ", "escaped","ball failed and the wild", "Your entire team has fainted"," caught", "expert trainer", "fled"]):
            await asyncio.sleep(1)  
            await event.client.send_message(572621020, "/hunt")
            clicked_4th_button = False  # Set the flag to True
            
                           
    @client.on(events.MessageEdited(from_users=(572621020,)))  # Listen for messages from the specified user(s)
    async def handle_message(event):
        try:
            global clicked_4th_button  # Use the global flag
            if event.is_private and "HP" in event.raw_text:
                hp = None
                for line in event.raw_text.split("\n"):
                    if "HP" in line:
                        hp = int(line.split("HP")[1].split("/")[0].strip())
                        print(f"HP value: {hp}")
                        break

                if hp and hp > 50:
                    await asyncio.sleep(1)
                    await event.click(random.randint(0, 3))
                elif hp and hp <= 50 and not clicked_4th_button:  # Check if the 4th button hasn't been clicked yet
                    await asyncio.sleep(1)
                    await event.click(4)
                    await asyncio.sleep(1) 
                    await event.click(0) 
                    clicked_4th_button = True  # Set the flag to True

        except (asyncio.TimeoutError, MessageIdInvalidError):
            pass
            
    @client.on(events.NewMessage(from_users=(572621020,)))  # Listen for messages from the specified user(s)
    async def handle_message(event):
        try:
            global clicked_4th_button  # Use the global flag
            if event.is_private and "HP" in event.raw_text:
                hp = None
                for line in event.raw_text.split("\n"):
                    if "HP" in line:
                        hp = int(line.split("HP")[1].split("/")[0].strip())
                        print(f"HP value: {hp}")
                        break

                if hp and hp > 50:
                    await asyncio.sleep(1)
                    await event.click(random.randint(0, 3))
                elif hp and hp <= 50 and not clicked_4th_button:  # Check if the 4th button hasn't been clicked yet
                    await asyncio.sleep(1)
                    await event.click(4)
                    await asyncio.sleep(1) 
                    await event.click(2) 
                    clicked_4th_button = True  # Set the flag to True

        except (asyncio.TimeoutError, MessageIdInvalidError):
            pass


    await client.start()
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
