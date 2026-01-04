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
    @discord.app_commands.describe(archivo="El archivo .lua ofuscado")
    async def desobf(self, interaction: discord.Interaction, archivo: discord.Attachment):
        if not archivo.filename.endswith(".lua"):
            await interaction.response.send_message("Por favor, sube un archivo .lua", ephemeral=True)
            return

        await interaction.response.defer()

        # Generar nombres de archivo únicos
        temp_id = str(uuid.uuid4())
        input_path = f"temp_in_{temp_id}.lua"
        output_path = f"temp_out_{temp_id}.luac"

        try:
            # Guardar el archivo adjunto
            with open(input_path, "wb") as f:
                await archivo.save(f)

            # Ejecutar la herramienta de desobfuscación
            # Según el README: dotnet build -c Release (ya debería estar compilado o lo compilamos)
            # El comando es: ./MoonsecDeobfuscator/bin/Release/net7.0/MoonsecDeobfuscator -dev -i <in> -o <out>
            # Primero nos aseguramos de que esté compilado (esto idealmente se hace una vez)
            
            executable = "MoonsecDeobfuscator/bin/Release/net8.0/MoonsecDeobfuscator" # Ajustar según la versión de dotnet
            if not os.path.exists(executable):
                # Intentar encontrar el ejecutable
                for root, dirs, files in os.walk("MoonsecDeobfuscator/bin"):
                    if "MoonsecDeobfuscator" in files and not root.endswith("ref"):
                         executable = os.path.join(root, "MoonsecDeobfuscator")
                         break

            process = await asyncio.create_subprocess_exec(
                "dotnet", "run", "--project", "MoonsecDeobfuscator/MoonsecDeobfuscator.csproj", "--", 
                "-dev", "-i", os.path.abspath(input_path), "-o", os.path.abspath(output_path),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()

            if os.path.exists(output_path):
                await interaction.followup.send(
                    content="Desobfuscación completada (Bytecode Lua 5.1):",
                    file=discord.File(output_path, filename=f"deobf_{archivo.filename}c")
                )
            else:
                error_msg = stderr.decode() or stdout.decode() or "Error desconocido al desobfuscar."
                await interaction.followup.send(f"Error al desobfuscar: {error_msg[:1900]}")

        except Exception as e:
            await interaction.followup.send(f"Error inesperado: {str(e)}")
        finally:
            # Limpiar archivos temporales
            if os.path.exists(input_path): os.remove(input_path)
            if os.path.exists(output_path): os.remove(output_path)

async def setup(bot):
    await bot.add_cog(Deobfuscate(bot))
