# Hesiz Desobfuscator Bot

This is a Discord bot designed to deobfuscate Lua scripts using MoonsecDeobfuscator and unluac.

## Requirements

- Python 3.11 or higher
- .NET SDK (for MoonsecDeobfuscator)
- Java Runtime Environment (for unluac.jar)

## Setup

1. Install the required Python packages:
   pip install discord.py python-dotenv

2. Configure the bot token:
   Create a .env file in the root directory and add your Discord bot token:
   DISCORD_TOKEN=your_token_here

3. Ensure external tools are present:
   - MoonsecDeobfuscator/MoonsecDeobfuscator.csproj must be buildable with dotnet.
   - unluac.jar must be present in the root directory.

## Usage

1. Start the bot:
   python main.py

2. In Discord, use the command:
   /desobf

3. Upload the .lua or .txt file you want to deobfuscate when prompted.

The bot will return the deobfuscated Lua file and/or the disassembly.
