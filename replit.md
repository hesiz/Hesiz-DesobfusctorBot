# Moonsec Deobfuscator Discord Bot

## Overview

This is a Discord bot that provides Lua script deobfuscation services through Discord slash commands. The bot wraps the MoonsecDeobfuscator tool (a .NET application) to deobfuscate Lua scripts that have been obfuscated using MoonSec V3. Users can upload obfuscated `.lua` files via Discord, and the bot processes them using the deobfuscator and returns the deobfuscated bytecode.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Bot Framework
- **Framework**: discord.py with commands extension
- **Command Pattern**: Cog-based modular command structure
- **Command Type**: Discord slash commands (app_commands)
- **Rationale**: Cogs allow for organized, modular command loading from the `commands/` directory, making it easy to add new features without modifying core bot code

### Command Loading System
- Commands are automatically discovered and loaded from the `commands/` directory
- Each command file is a Python module containing a Cog class
- The bot syncs slash commands on startup via `setup_hook()`

### Deobfuscation Pipeline
1. User uploads a `.lua` file via Discord attachment
2. Bot validates file extension
3. File is saved temporarily with a UUID-based unique filename
4. Bot invokes the .NET MoonsecDeobfuscator tool via `dotnet run`
5. Deobfuscated output is generated and returned to user
6. Temporary files are cleaned up

### File Handling
- Temporary files use UUID naming to prevent collisions
- Input files: `temp_in_{uuid}.lua`
- Output files: `temp_out_{uuid}.luac`

## External Dependencies

### Discord API
- **Library**: discord.py
- **Authentication**: Bot token via `DISCORD_TOKEN` environment variable
- **Intents**: Default intents plus `message_content`

### MoonsecDeobfuscator
- **Type**: .NET console application (bundled in repository)
- **Runtime**: .NET 7.0/8.0
- **Invocation**: Via `dotnet run` with project path
- **Purpose**: Devirtualizes MoonSec V3 obfuscated Lua scripts to Lua 5.1 bytecode

### Environment Configuration
- **dotenv**: Used for loading environment variables from `.env` file
- **Required Variables**:
  - `DISCORD_TOKEN`: Discord bot authentication token