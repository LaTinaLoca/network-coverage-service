from django.test import TestCase
from net_coverage.utilities.conversion_lambert93_gps import lambert93_to_gps


class TestCoordinatesConversion(TestCase):
    def test_lambert93_to_gps(self):
        latitude, longitude, err_msg = lambert93_to_gps(x=102980, y=6847973)
        self.assertEqual(latitude, 48.4565745588299)
        self.assertEqual(longitude, -5.088856115301341)
        self.assertEqual(err_msg, "")

    def test_lambert93_to_gps_none(self):
        latitude, longitude, err_msg = lambert93_to_gps(x=None, y=None)
        self.assertEqual(latitude, None)
        self.assertEqual(longitude, None)
    
    def test_lambert93_to_gps_string(self):
        latitude, longitude, err_msg = lambert93_to_gps(x="ds", y=1900)
        self.assertEqual(latitude, None)
        self.assertEqual(longitude, None)
