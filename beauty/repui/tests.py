from datetime import date, timedelta
from RDF import Storage, Model, Statement
from django.test import TestCase
from django.conf import settings
from repui.search import process_POST_params
from repui.models import (
    add_treatment_to_trenche,
    create_availability_with_trenche,
    subject,
    get_trenche_support
    )
from repui.URIs import (
    NAME,
    PROVIDER,
    TRENCHE,
    TREATMENT,
    SUPPORTS,
    LABEL,
    TYPE,
    AVAIL,
    )
import repui.models


class process_POST_params_Test(TestCase):

    class FakeRequest:
        def __init__(self):
            self.POST = {
                u'csrfmiddlewaretoken': [u'db4187ab0c4fe8ef8859b2e9948ecaba'],
                u'location': [u'San Francisco'],
                u'treatment': [u'massage'],
                u'today': [u'on'],
                u'anotherday': [u'']
                }


    def setUp(self):
        self.fake_request = self.FakeRequest()

    def test_date(self):
        today = date.today()

        # Find today as per the request params above.
        result = process_POST_params(self.fake_request)
        self.assertEqual(result['dates'], [today])

        # Add tomorrow.
        self.fake_request.POST[u'tomorrow'] = [u'on']
        result = process_POST_params(self.fake_request)
        self.assertEqual(
            result['dates'],
            [today, today + timedelta(days=1)]
            )

        # Remove today.
        del self.fake_request.POST[u'today']
        result = process_POST_params(self.fake_request)
        self.assertEqual(
            result['dates'],
            [today + timedelta(days=1)]
            )

        # Add a specific date (in the past, as the business logic of not
        # allowing appointments in the past will not have been applied
        # yet.
        self.fake_request.POST[u'anotherday'] = [u'11/28/10']
        result = process_POST_params(self.fake_request)
        self.assertEqual(
            result['dates'],
            [today + timedelta(days=1), date(2010, 11, 28)]
            )

    def test_location(self):
        result = process_POST_params(self.fake_request)

        self.assertEqual(result['lat_long'], (1, 2))
        self.assertEqual(
            result['distance_full_text'],
            "Where I Left My Heart, CA 94132"
            )


class QueryTest(TestCase):
    """
    Tests the functionality related to the Day Part Pick Page
    """

    def setUp(self):
        self._M = repui.models.M
        repui.models.M = Model(Storage(**settings.TRIPLE_STORES['default']))

    def tearDown(self):
        repui.models.M = self._M

    def testAddTreatmentToTrenche(self):
        add_treatment_to_trenche('Banana Slug Dip', 'A')

        result = get_trenche_support()
        self.assertEqual(len(result), 1)

        result = result[0]
        self.assertEqual(str(result['treatmentname']), 'BananaSlugDip')
        self.assertEqual(str(result['trenchelabel']), 'A')

    def testCreateAvailabilityWithUnknownTrenche(self):
        result = create_availability_with_trenche("A")
        self.assert_(not result)
        self.assertEqual(list(repui.models.M.as_stream()), [])

    def testCreateAvailabilityWithTrenche(self):
        add_treatment_to_trenche('Banana Slug Dip', 'A')
        result = create_availability_with_trenche("A")
        self.assert_(Statement(result, TYPE, AVAIL) in repui.models.M)
