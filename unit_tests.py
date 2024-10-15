import unittest
from unittest.mock import patch, MagicMock
import client_monitor

class TestMonitoringTool(unittest.TestCase):

    @patch('client_monitor_gui.subprocess.getoutput')
    def test_get_wireguard_status(self, mock_getoutput):
        mock_getoutput.return_value = "wg0 connected"
        status = client_monitor.get_wireguard_status()
        self.assertIn("wg0 connected", status)

    @patch('client_monitor_gui.requests.get')
    def test_get_public_ip(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "123.123.123.123"
        mock_get.return_value = mock_response
        public_ip = client_monitor.get_public_ip()
        self.assertEqual(public_ip, "123.123.123.123")

    @patch('client_monitor_gui.subprocess.getoutput')
    def test_monitor_dns(self, mock_getoutput):
        mock_getoutput.return_value = "DNS Query: example.com"
        dns_query = client_monitor.monitor_dns()
        self.assertIn("example.com", dns_query)

    @patch('client_monitor_gui.smtplib.SMTP')
    def test_send_email_alert(self, mock_smtp):
        client_monitor.send_email_alert("Test Subject", "Test Body")
        mock_smtp_instance = mock_smtp.return_value
        mock_smtp_instance.sendmail.assert_called()

if __name__ == '__main__':
    unittest.main()