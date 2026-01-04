import discord
from discord.ext import commands
import os
import subprocess
import asyncio
import uuid

class Deobfuscate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="desobf", description="Desobfusca un archivo Lua usando MoonsecDeobfuscator")
    @discord.app_commands.describe(archivo="El archivo .lua o .txt ofuscado")
    async def desobf(self, interaction: discord.Interaction, archivo: discord.Attachment):
        if not (archivo.filename.lower().endswith(".lua") or archivo.filename.lower().endswith(".txt")):
            await interaction.response.send_message("Por favor, sube un archivo .lua o .txt", ephemeral=True)
            return

        await interaction.response.defer()
        
        temp_id = str(uuid.uuid4())
        input_path = f"temp_in_{temp_id}.lua"
        output_path = f"temp_out_{temp_id}.luac"
        decompiled_path = f"temp_dec_{temp_id}.lua"

        try:
            with open(input_path, "wb") as f:
                await archivo.save(f)

            process = await asyncio.create_subprocess_exec(
                "dotnet", "run", "--project", "MoonsecDeobfuscator/MoonsecDeobfuscator.csproj", "--", 
                "-dev", "-i", os.path.abspath(input_path), "-o", os.path.abspath(output_path),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()

            if os.path.exists(output_path):
                disasm_path = f"temp_dis_{temp_id}.txt"
                disasm_proc = await asyncio.create_subprocess_exec(
                    "dotnet", "run", "--project", "MoonsecDeobfuscator/MoonsecDeobfuscator.csproj", "--", 
                    "-dis", "-i", os.path.abspath(input_path), "-o", os.path.abspath(disasm_path),
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                await disasm_proc.communicate()

                if os.path.exists(disasm_path):
                    with open(disasm_path, "r+", encoding="utf-8") as f:
                        content = f.read()
                        f.seek(0, 0)
                        f.write("-- hesiz desofuscator\n" + content)

                decompile_proc = await asyncio.create_subprocess_exec(
                    "java", "-jar", "unluac.jar", os.path.abspath(output_path),
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                stdout_dec, stderr_dec = await decompile_proc.communicate()

                if decompile_proc.returncode == 0:
                    with open(decompiled_path, "wb") as f:
                        f.write(b"-- hesiz desofuscator\n" + stdout_dec)
                    
                    await interaction.followup.send(
                        content="Desobfuscación y decompilación completadas:",
                        file=discord.File(decompiled_path, filename="Desobf.lua")
                    )
                else:
                    error_dec = stderr_dec.decode()
                    files_to_send = [discord.File(output_path, filename="Desobf.luac")]
                    if os.path.exists(disasm_path):
                        files_to_send.append(discord.File(disasm_path, filename="Disassembly.txt"))
                    
                    await interaction.followup.send(
                        content=f"La decompilación falló (posible bytecode protegido o corrupto).\nError: `{error_dec[:200]}`\nTe envío el bytecode y el desensamblado para análisis manual:",
                        files=files_to_send
                    )
                
                if os.path.exists(disasm_path): os.remove(disasm_path)
            else:
                error_msg = stderr.decode() or stdout.decode() or "Error desconocido al desobfuscar."
                await interaction.followup.send(f"Error al desobfuscar: {error_msg[:1900]}")

        except Exception as e:
            await interaction.followup.send(f"Error inesperado: {str(e)}")
        finally:
            for path in [input_path, output_path, decompiled_path]:
                if os.path.exists(path): os.remove(path)

async def setup(bot):
    await bot.add_cog(Deobfuscate(bot))
