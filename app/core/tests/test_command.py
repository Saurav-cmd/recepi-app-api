"""
django test for db command of database
"""
#This will mock the behavior of the database
from unittest.mock import patch
#This will handle the error exception when trying to connect to database
from psycopg2 import OperationalError as Psycopg2Error
#Given by django it allows us to call the command
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase

#We need to use this patch if we want to mock the behavior of the database and inside small bracket is the path
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTest(SimpleTestCase):
    """Test commands"""
    def test_wait_for_db_ready(self,patched_check):
        """Test waiting for database if database is ready"""
        #This just return the value of the mock
        patched_check.return_value = True
        call_command('wait_for_db')
        #This make sure that we call the right database once if not called once it will throw an error
        patched_check.assert_called_once_with(databases=['default'])
     
    @patch('time.sleep') 
    def test_wait_for_db_delay(self,patched_sleep,patched_check):
        """Test waiting for db when getting OperationalError"""
        #What this does is define various value each time we call it in the order that we call it
        #That *2 rises the error in Psycopg2Error then *3 means we rise three operational error.
        #When database has not been started ot wake up then it throws Psycopg2 error and when database is ready to setup
        #but is not accepting any connection and test then it throws operational error
        patched_check.side_effect = [Psycopg2Error] * 2 + [OperationalError] * 3 + [True]   
        call_command('wait_for_db')
        #This is just checking if the call count is equal to 6 or not
        self.assertEqual(patched_check.call_count,6) 
        patched_check.assert_called_with(databases=['default'])

