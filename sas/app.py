from sas import db
from sas.services import WordService
from sas.settings import Settings
from sas.sources import CsvSource


class App:
    """Class with business logic."""

    def __init__(self, settings: Settings):
        """Init App instance."""
        self.settings = settings

    def initialize(self):
        """Initialize: initialize DB, load data."""
        is_db_exists = db.initialize(self.settings)
        if not is_db_exists:
            source = CsvSource(filename=self.settings.csv_words_filename)
            words = source.read_words()
            WordService().add_many(words)

    def serve(self):
        """Loop for work."""
        raise NotImplementedError


# todo: remove
# Create a few rows:
#
# charlie = User.create(username='charlie')
# huey = User(username='huey')
# huey.save()
#
# # Transactions:
# with db.atomic():
# with db.transaction():
#     ...
# except ErrorSavingData:
# # ... (transactions)
#
#
# # No need to set `is_published` or `created_date` since they
# # will just use the default values we specified.
# Tweet.create(user=charlie, message='My first tweet')
#
#
# Queries are expressive and composable:
#
# # A simple query selecting a user.
# User.get(User.username == 'charlie')
#
# # Get tweets created by one of several users.
# usernames = ['charlie', 'huey', 'mickey']
# users = User.select().where(User.username.in_(usernames))
# tweets = Tweet.select().where(Tweet.user.in_(users))
#
# # We could accomplish the same using a JOIN:
# tweets = (Tweet
#           .select()
#           .join(User)
#           .where(User.username.in_(usernames)))
#
# # How many tweets were published today?
# tweets_today = (Tweet
#                 .select()
#                 .where(
#                     (Tweet.created_date >= datetime.date.today()) &
#                     (Tweet.is_published == True))
#                 .count())
#
# # Paginate the user table and show me page 3 (users 41-60).
# User.select().order_by(User.username).paginate(3, 20)
#
# # Order users by the number of tweets they've created:
# tweet_ct = fn.Count(Tweet.id)
# users = (User
#          .select(User, tweet_ct.alias('ct'))
#          .join(Tweet, JOIN.LEFT_OUTER)
#          .group_by(User)
#          .order_by(tweet_ct.desc()))
#
# # Do an atomic update (for illustrative purposes only, imagine a simple
# # table for tracking a "count" associated with each URL). We don't want to
# # naively get the save in two separate steps since this is prone to race
# # conditions.
# Counter.update(count=Counter.count + 1).where(Counter.url == request.url)
