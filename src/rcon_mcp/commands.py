from typing import Dict, List
from rcon.source import Client
import logging
from mcp.server.fastmcp import FastMCP
from .config import ServerConfig

logger = logging.getLogger(__name__)

# Initialize FastMCP server to interact with CS2 servers
mcp = FastMCP("CS2 MCP-Server 🚀", dependencies=["rcon"])

class RCONCommands:
    """Handler for RCON commands to the CS2 server."""
    
    def __init__(self, config: ServerConfig):
        """Initialize the RCON commands handler.
        
        Args:
            config: Server configuration containing connection details.
        """
        self.config = config

    def execute(self, command: str) -> str:
        """Execute an RCON command on the CS2 server.
        
        Args:
            command: The RCON command to execute.
            
        Returns:
            str: The server's response to the command.
            
        Raises:
            ConnectionError: If unable to connect to the RCON server.
            ValueError: If the command execution fails.
        """
        try:
            with Client(self.config.host, self.config.port, passwd=self.config.password) as client:
                response = client.run(command, '')
                return response
        except Exception as e:
            logger.error(f"Failed to execute RCON command '{command}': {e}")
            raise ConnectionError(f"Failed to execute RCON command: {e}") from e

    def status(self) -> str:
        """Get the current status of the CS2 server.
        
        Returns:
            str: The server's status information.
            
        Raises:
            ConnectionError: If unable to connect to the RCON server.
        """
        return self.execute("status")
    
    def list_workshop_maps(self) -> str:
        """List all workshop maps on the CS2 server.
        
        Returns:
            str: A list of workshop maps.
        """
        return self.execute("ds_workshop_listmaps")
    
    def host_workshop_map(self, workshop_map_id: int) -> str:
        """Hosts a workshop map by its id on the CS2 server.
        
        Returns:
            str: The server's response to the host_workshop_map command.
        """
        command = f"host_workshop_map {workshop_map_id}"
        return self.execute(command)
    
    def workshop_changelevel(self, workshop_map_name: str) -> str:
        """Changes the map to a given CS2 workshop map on the CS2 server.
        
        Returns:
            str: The server's response to the ds_worskshop_changelevel command.
        """
        command = f"ds_workshop_changelevel {workshop_map_name}"
        return self.execute(command)

    @staticmethod
    def get_available_commands() -> Dict[str, str]:
        """Get a dictionary of available RCON commands and their descriptions.
        
        Returns:
            Dict[str, str]: Dictionary mapping command names to their descriptions.
        """
        return {
            "changelevel <map_name>": "Changes the current map.",
            "mp_warmup_end": "Ends the warmup phase.",
            "mp_restartgame 1": "Restarts the game after 1 second.",
            "bot_kick": "Kicks all bots from the server.",
            "bot_add_t": "Adds a bot to the Terrorist side.",
            "bot_add_ct": "Adds a bot to the Counter-Terrorist side.",
            "bot_quota <number>": "Sets the total number of bots.",
            "mp_freezetime 15": "Sets the freeze time before rounds start (15 sec).",
            "mp_roundtime 1.92": "Sets the round duration to 1:55 minutes.",
            "mp_maxrounds 24": "Sets the maximum number of rounds (MR24).",
            "mp_halftime 1": "Enables halftime after 12 rounds.",
            "mp_buytime 20": "Sets how long players can buy weapons (20 sec).",
            "mp_startmoney 800": "Sets the starting money for players.",
            "mp_overtime_enable 1": "Enables overtime if the match is tied.",
            "mp_overtime_maxrounds 6": "Sets max rounds in overtime (MR6).",
            "mp_overtime_startmoney 12500": "Sets start money for overtime rounds.",
            "mp_defuser_allocation 2": "Gives all CTs a defuse kit.",
            "mp_limitteams 1": "Prevents unbalanced teams.",
            "mp_autoteambalance 1": "Enables automatic team balancing.",
            "mp_force_pick_time 5": "Time players have to pick a team.",
            "mp_ignore_round_win_conditions 0": "Disables forced round end.",
            "mp_death_drop_gun 1": "Allows players to drop their weapons on death.",
            "mp_t_default_grenades \"weapon_molotov;weapon_smokegrenade\"": "Sets default grenades for Ts.",
            "mp_ct_default_grenades \"weapon_incgrenade;weapon_smokegrenade\"": "Sets default grenades for CTs.",
            "sv_cheats 0": "Disables cheats (must be 1 to enable commands like noclip).",
            "rcon_password <password>": "Sets the RCON password for remote control.",
            "rcon <command>": "Runs a remote command on the server.",
            "exec <config_name>": "Executes a config file (e.g., exec server.cfg).",
            "status": "Shows server status and player information.",
            "kick <player_name or #userid>": "Kicks a player from the server.",
            "banid <time> <steamID>": "Bans a player for a certain duration.",
            "host_workshop_map <workshop_id>": "Loads a workshop map.",
            "mp_endmatch": "Ends the current match.",
            "mp_pause_match": "Pauses the match.",
            "mp_unpause_match": "Unpauses the match.",
            "sv_alltalk 0": "Disables voice chat between teams.",
            "mp_spectators_max 4": "Limits the number of spectators.",
            "mp_forcecamera 1": "Restricts dead players' view to only their team.",
            "sv_voiceenable 1": "Enables voice communication.",
            "mp_respawn_immunitytime 0": "Disables spawn protection.",
            "mp_display_kill_assists 1": "Enables assist tracking in scoreboard.",
            "mp_randomspawn 0": "Ensures standard spawn locations.",
            "sv_infinite_ammo 0": "Disables infinite ammo (1 for unlimited bullets).",
            "sv_grenade_trajectory 0": "Disables grenade trajectory lines.",
            "sv_showimpacts 0": "Disables bullet impact visualization.",
            "mp_warmuptime 60": "Sets warmup duration (60 sec).",
            "mp_suicide_penalty 0": "Removes suicide penalty.",
            "mp_teammates_are_enemies 0": "Disables friendly fire (1 = FFA mode).",
            "mp_round_restart_delay 5": "Time before the next round starts (5 sec).",
            "mp_weapon_allow_glock 1": "Enables/disables specific weapons.",
            "mp_c4timer 40": "Sets bomb timer duration (40 sec standard).",
            "mp_playercashawards 1": "Enables money rewards for player actions.",
            "mp_teamcashawards 1": "Enables team-wide money rewards.",
            "sv_matchpause_auto_5v5 1": "Enables auto-pause for 5v5 competitive.",
            "mp_friendlyfire 1": "Enables friendly fire.",
            "sv_competitive_minspec 1": "Forces minimum competitive settings."
        }

# Create RCON commands instance
rcon_commands = RCONCommands(ServerConfig.from_env())

@mcp.tool()
def rcon(command: str) -> str:
    """Execute an RCON command on the CS2 server.
    
    Args:
        command: The RCON command to execute.
        
    Returns:
        str: The server's response to the command.
        
    Raises:
        ConnectionError: If unable to connect to the RCON server.
        ValueError: If the command execution fails.
    """
    return rcon_commands.execute(command)

@mcp.tool()
def status() -> str:
    """Get the current status of the CS2 server.
    
    Returns:
        str: The server's status information.
        
    Raises:
        ConnectionError: If unable to connect to the RCON server.
    """
    return rcon_commands.status()

@mcp.tool()
def list_workshop_maps() -> str:
    """List all workshop maps on the CS2 server.
        
    Returns:
        str: A list of workshop maps.
        
    Raises:
        ConnectionError: If unable to connect to the server.
    """
    return rcon_commands.list_workshop_maps()

@mcp.tool()
def host_workshop_map(workshop_map_id: int) -> str:
    """Hosts a workshop map by its id on the CS2 server.
    
    Args:
        command: The id of the workshop map that should be hosted.
        
    Returns:
        str: The server's response to the command.
        
    Raises:
        ConnectionError: If unable to connect to the server.
        ValueError: If the command execution fails.
    """
    return rcon_commands.host_workshop_map(workshop_map_id)

@mcp.tool()
def workshop_changelevel(workshop_map_name: str) -> str:
    """Changes the map to a given CS2 workshop map on the CS2 server.
    
    Args:
        command: The workshop map name the map should change to.
        
    Returns:
        str: The server's response to the command.
        
    Raises:
        ConnectionError: If unable to connect to the server.
        ValueError: If the command execution fails.
    """
    return rcon_commands.workshop_changelevel(workshop_map_name)

# Export the MCP instance
mcp_server = mcp._mcp_server
