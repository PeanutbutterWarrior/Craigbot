import discord


class WebhookManager:
    _webhooks = {}
    _client = None

    async def init(self, client):
        # Save client for changing webhooks channels
        self._client = client

        for guild in client.guilds:
            guild_webhooks = [webhook for webhook in await guild.webhooks() if webhook.user.id == client.user.id]

            if len(guild_webhooks) == 0:
                for channel in guild.channels:
                    if type(channel) == discord.TextChannel:
                        used_webhook = await channel.create_webhook(name='Craighook')
                        break
                else:
                    # Guild has no text channels, cannot create a webhook for it
                    continue
            else:
                used_webhook, *spare_webhooks = guild_webhooks
                for webhook in spare_webhooks:
                    await webhook.delete()
            self._webhooks[guild.id] = used_webhook

    async def get_webhook(self, channel: discord.TextChannel):
        try:
            webhook = self._webhooks[channel.guild.id]
        except KeyError:
            raise ValueError(f'Guild {channel.guild.name}:{channel.guild.id} has no text channels, cannot create a '
                             f'webhook')
        # discord.py doesn't have a method to change webhook channels
        # Manually change the channel of a webhook by sending an api request
        # Virtually all of this is undocumented
        # If trying to debug check discord/http.py and discord/client.py
        await self._client.http.request(discord.http.Route('PATCH', '/webhooks/{webhook_id}',
                                                           webhook_id=webhook.id),
                                        json={'channel_id': str(channel.id)})
        return webhook