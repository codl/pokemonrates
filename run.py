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
        yaml = ruamel.yaml.YAML()

        with open('pokemon.txt') as f:
            self.pokémon = list(map(lambda p: p.strip(), f.readlines()))

        with open('grammar.yml') as f:
            self.grammar = yaml.load(f)
            self.grammar['pokemon'] = self.pokémon
            self.tracery = tracery.Grammar(self.grammar)
            self.tracery.add_modifiers(base_english)

        with open('bot.yml') as f:
            self.config = yaml.load(f)
            if 'last_timer' not in self.config:
                self.config['last_timer'] = time.time()

        self.mastodon = mastodon.Mastodon(
                api_base_url=self.config['instance'],
                client_id=self.config['client_key'],
                client_secret=self.config['client_secret'],
                access_token=self.config['access_token'])

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
        words = re.findall('\w+', status['content_clean'])
        random.shuffle(words)
        for word in words:
            pokémon = self.to_pokémon(word)
            if pokémon:
                self.logger.info('Found pokémon: {}'.format(pokémon))
                reply = self.tracery.flatten(
                        '#[pokemon:{}]origin#'.format(pokémon))
                self.tracery.clear_state()
                return reply
        ctx = self.mastodon.status_context(status)
        if not any(map(lambda status: status['account']['id'] == self.me['id'], ctx['ancestors'])):
            # if we're not already in the thread
            return self.tracery.flatten('#origin#')
        else:
            self.logger.info("We're already in this thread, not replying.")

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

                visibility = status.visibility

                self.mastodon.status_post(mentions + reply, in_reply_to_id=status['id'],
                        visibility=visibility)

    def on_update(self, update):
        pass

    def run(self):
        self.me = self.mastodon.account_verify_credentials()

        stream = None
        while True:
            if stream is None or not stream.is_alive():
                if stream is not None:
                    self.logger.warning('Stream lost, reconnecting...')
                stream = self.mastodon.stream_user(self, async=True)
                self.logger.info('Connected.')
            if time.time() > self.config['last_timer'] + 60*60:
                self.logger.info('Sending hourly status.')
                self.on_timer()
                self.config['last_timer'] = time.time()
                self.save()
            time.sleep(15)



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('bot')
    stopping = False
    while not stopping:
        try:
            bot = Bot()
            bot.run()
        except KeyboardInterrupt:
            # why doesn't this ever run?
            logger.info('Quitting...')
            stopping = True
        except Exception as e:
            bot.logger.exception('Crashed. Restarting...')
