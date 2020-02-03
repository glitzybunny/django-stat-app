from django.db import models
from django.db.models import Sum

from django.core.exceptions import ObjectDoesNotExist
from datetime import date, timedelta, datetime

GENDER = (
    ('Male', 'Male'),
    ('Female', 'Female')
)

# Retrieve all Statistic objects for specified user, and date range
# Arguments:
#   uid - User id (NOT User model object, just id, like User.id). Required
#   start_date - datetime.date object. Start date of date range of Statistic objects
#   end_date - datetime.date object. End date of date range of Statistic objects


def get_UID_stat(uid, start_date=None, end_date=None):
    # Returns None if there is no User object for the uid
    if not User.is_exist(uid):
        return None

    pk_stat = Statistic.objects.filter(user_id=uid)

    if start_date:
        pk_stat = pk_stat.filter(date__gte=start_date)

        if end_date:
            pk_stat = pk_stat.filter(date__lte=end_date)

    return pk_stat


# Generates full date range by start and end date
def daterange(date1, date2):
    for n in range(int((date2 - date1).days)+1):
        yield date1 + timedelta(n)

# Retrieves Statistics data for Chart JS for specified range.
# Fills gaps in date range by 0
# Returns a tuple of labels(chart JS labels) and data(chart JS values)
# Arguments:
#    queryset - Queryset of Statistic objects
#    date_range - String of date range for fetching
#    chart - String of a chart name. It gotta match to name of Statistic field.
#            Like 'page_views', 'clicks', etc ...


def querysetToChartData(queryset, date_range, chart):
    # Converts dates from string into datetime.date object
    start = datetime.strptime(date_range[0], '%Y-%m-%d').date()
    end = datetime.strptime(date_range[1], '%Y-%m-%d').date()

    # labels and data values for Chart JS
    labels = []
    data = []

    for dt in daterange(start, end):
        labels.append(dt)
        # Decorating value for aggregation
        # _ = f"{chart} sum"
        q = queryset.filter(date=dt).aggregate(Sum(chart))[
            "{0}__sum".format(chart)] or 0
        data.append(q)

    return (labels, data)


class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    gender = models.CharField(max_length=15, choices=GENDER)
    ip_address = models.GenericIPAddressField()

    @property
    def fullname(self):
        fullname = '{0} {1}'.format(self.first_name, self.last_name)
        return fullname

    @classmethod
    def is_exist(cls, uid):
        try:
            obj = cls.objects.get(pk=uid)
            return obj
        except ObjectDoesNotExist:
            return False

    def __str__(self):
        return '{0}: {1}'.format(self.ip_address, self.fullname)

    # Calls get_UID_stat function (check above) for this user id
    def get_stat(self, start_date=None, end_date=None):
        return get_UID_stat(self.id, start_date, end_date)

    # Counts total amount of clicks for the user
    @property
    def total_clicks(self):
        total_clicks = Statistic.objects.filter(
            user_id=self.pk).aggregate(Sum('clicks'))
        return total_clicks['clicks__sum']

    # Counts amount of views for the user
    @property
    def total_page_views(self):
        total_views = Statistic.objects.filter(
            user_id=self.pk).aggregate(Sum('page_views'))
        return total_views['page_views__sum']


# Counts total amount of clicks for specified users
# Takes User QuerySet as an argument
def get_total_clicks(users):
    total_clicks = 0

    for user in users:
        total_clicks += user.get_total_clicks()

    return total_clicks


# Counts total amount of page views for specified users
# Takes User QuerySet as an argument
def get_total_page_views(users):
    total_views = 0

    for user in users:
        total_views += user.get_total_page_views()

    return total_views


class Statistic(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    page_views = models.IntegerField(default=0)
    clicks = models.IntegerField(default=0)

    def __str__(self):
        return 'UID: {0}|c: {1} |v:{2}'.format(self.user_id, self.clicks, self.page_views)

    # Calls get_UID_stat function (check above) for this user id
    def get_stat(self, start_date=None, end_date=None):
        return get_UID_stat(self.user_id, start_date, end_date)
