import os

from dotenv import load_dotenv
from steam.webauth import WebAuth
from steam.client import SteamClient
from steam.enums import EResult, ELeaderboardDataRequest
from loguru import logger

load_dotenv()

USERNAME = os.environ["STEAM_USERNAME"]
PASSWORD = os.environ["STEAM_PASSWORD"]

APP_ID = 2737300

client = SteamClient()


@client.on("error")
def handle_error(result):
    logger.info("Logon result: %s", repr(result))


@client.on("connected")
def handle_connected():
    logger.info("Connected to %s", client.current_server_addr)


@client.on("reconnect")
def handle_reconnect(delay):
    logger.info("Reconnect in %ds...", delay)


@client.on("disconnected")
def handle_disconnect():
    logger.info("Disconnected.")


@client.on("logged_on")
def handle_after_logon():
    logger.info("Logged on as: %s", client.user.name)


def get_leaderboard(steam_client: SteamClient, leaderboard_name: str):
    leaderboard = steam_client.get_leaderboard(APP_ID, leaderboard_name)
    if leaderboard.id == 0:
        logger.error("Leaderboard not found!")
        return

    logger.info(leaderboard)

    for entry in leaderboard.get_entries(
        start=0, end=10, data_request=ELeaderboardDataRequest.Global
    ):
        logger.info(entry)


def setup_client(client: SteamClient):
    # TODO figure out how to setup client without user interaction
    # or maybe just use a client without 2FA, need to buy the game probs lol

    result = client.login(username=USERNAME, password=PASSWORD)

    while result in (
        EResult.AccountLoginDeniedNeedTwoFactor,
        EResult.TwoFactorCodeMismatch,
    ):
        webauth = WebAuth()
        code = os.popen("steamguard code").read().strip()
        webauth.login(username=USERNAME, password=PASSWORD, code=code)

        result = client.login(username=USERNAME, access_token=webauth.refresh_token)
    while result in (EResult.AccountLogonDenied, EResult.InvalidLoginAuthCode):
        raise RuntimeError("Failed to login, email code auth not implemented")


if __name__ == "__main__":
    try:
        setup_client(client)
        get_leaderboard(client, "ultra_chicago")
        client.run_forever()
    except KeyboardInterrupt:
        if client.connected:
            logger.info("Logout")
            client.logout()
