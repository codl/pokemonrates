import mastodon
import ruamel.yaml
import tracery
from tracery.modifiers import base_english
import re
import random
import time
from functools import reduce
import logging


class Bot(mastodon.StreamListener):
    def __init__(self):
        self.logger = logging.getLogger('bot.pokemonrates')
        self.logger.info('hey')
        yaml = ruamel.yaml.YAML()

        with open('pokemon.txt') as f:
            self.pokémon = list(map(lambda p: p.strip(), f.readlines()))
            print(self.pokémon)

        with open('grammar.yml') as f:
            self.grammar = yaml.load(f)
            self.grammar['pokemon'] = self.pokémon
            self.tracery = tracery.Grammar(self.grammar)
            self.tracery.add_modifiers(base_english)

        with open('bot.yml') as f:
            self.config = yaml.load(f)

        self.mastodon = mastodon.Mastodon(
                api_base_url=self.config['instance'],
                client_id=self.config['client_key'],
                client_secret=self.config['client_secret'],
                access_token=self.config['access_token'])

        self.me = self.mastodon.account_verify_credentials()

    def save(self):
        yaml = ruamel.yaml.YAML()
        with open('bot.yml', 'w') as f:
            yaml.dump(self.config, f)

    def on_timer(self):
        self.mastodon.status_post(
                self.tracery.flatten('#origin#'), visibility='unlisted')

    def to_pokémon(self, word):
        for pokémon in self.pokémon:
            if pokémon.lower() == word.lower():
                return pokémon
        return False

    def on_mention(self, status):
        words = status['content_clean'].split()
        random.shuffle(words)
        for word in words:
            pokémon = self.to_pokémon(word)
            if pokémon:
                self.logger.info('Found pokémon: {}'.format(pokémon))
                reply = self.tracery.flatten(
                        '#[pokemon:{}]origin#'.format(pokémon))
                self.tracery.clear_state()
                return reply
        return self.tracery.flatten('#origin#')

    def on_notification(self, notification):
        if notification['type'] == 'mention':
            status = notification['status']
            clean = re.sub('<[^<>]+>', ' ', status.content, flags=re.I)
            status['content_clean'] = clean

            self.logger.info('Reacting to mention: {}'.format(clean))

            reply = self.on_mention(status)
            if reply:
                self.logger.info('Replying: {}'.format(reply))
                mentions = set(map(lambda mention: mention['acct'], status['mentions']))
                mentions.add(status['account']['acct'])
                mentions.remove(self.me['acct'])
                mentions = reduce(lambda a, b: '{}@{} '.format(a, b), mentions, "")
                self.mastodon.status_post(mentions + reply, in_reply_to_id=status['id'])

    def run(self):
        stream = self.mastodon.stream_user(self, async=True)
        self.logger.info('Connected.')
        while True:
            try:
                self.logger.info('Sending hourly status.')
                self.on_timer()
                time.sleep(60*60)
            except KeyboardInterrupt:
                self.logger.info('Quitting...')
                stream.close()
                return



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    bot = Bot()
    bot.run()
