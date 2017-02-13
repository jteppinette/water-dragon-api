"""
Asserts that the Water Dragon Identity Models endpoints are working properly.

The following tests can be executed with the following command.
    
    `coverage run --source='api' manage.py test api`

    This command will run all tests files in `api/tests/` and will generate a
    coverage report that can be seen by running `coverage -rm`.

Note:

    All testing commands need to executed from the directory containing
    `manage.py`.
"""

from rest_framework.test import APITestCase
from rest_framework import status

import json

# Custom User Model
from django.contrib.auth import get_user_model

# User Helper Models
from api.models import Organization, University

# User Profile Models
from api.models import Nationals, Administrator, Host

# Email Helper Models
from api.models import CarbonCopyAddress

# Identity Models
from api.models import Identity, Flag

# Event Models
from api.models import Event, Procedure, Invitee

def create_user(username, password):
    """
    Create a user given an username and password.
    """
    return get_user_model().objects.create_user(username=username,
                                                email=username+'@'+username+'.com',
                                                password=password)


class IdentityModelTests(APITestCase):
    """
    The following tests have been created to assert that each of the identity
    models rest endpoints perform accurately and reliably.
    """

    def setUp(self):
        """
        Apply fixture data to test case.
        """
        self.admin = create_user('josh', 'josh')
        self.admin.is_superuser = True
        self.admin.save()

        self.ks = Organization.objects.create(name='Kappa Sigma')
        self.spsu = University.objects.create(name='Southern Polytechnic State University',
                                              acronym='SPSU')
        
        self.sae = Organization.objects.create(name='Sigma Alpha Epsilon')
        self.gt = University.objects.create(name='Georgia Institute of Technology',
                                              acronym='GT')

        ks_nat_user = create_user('ks', 'ks')
        self.ks_nat = Nationals.objects.create(user=ks_nat_user,
                                               organization=self.ks,
                                               enabled=True)

        spsu_admin_user = create_user('spsu', 'spsu')
        self.spsu_admin = Administrator.objects.create(user=spsu_admin_user,
                                                       university=self.spsu,
                                                       enabled=True)

        sae_nat_user = create_user('sae', 'sae')
        self.sae_nat = Nationals.objects.create(user=sae_nat_user,
                                                organization=self.sae)

        gt_admin_user = create_user('gt', 'gt')
        self.gt_admin_user = Administrator.objects.create(user=gt_admin_user,
                                                          university=self.gt)

        ksspsu_user = create_user('ksspsu', 'ksspsu')
        self.ksspsu = Host.objects.create(user=ksspsu_user,
                                          organization=self.ks,
                                          university=self.spsu,
                                          enabled=True)

        saespsu_user = create_user('saespsu', 'saespsu')
        self.saespsu = Host.objects.create(user=saespsu_user,
                                          organization=self.sae,
                                          university=self.spsu,
                                          enabled=True)

        ksgt_user = create_user('ksgt', 'ksgt')
        self.ksgt = Host.objects.create(user=ksgt_user,
                                          organization=self.ks,
                                          university=self.gt,
                                          enabled=True)

    """
                             IDENTITY
    """
    
    def test_identity_post_by_all_profile(self):
        """
        Assert that an `Identity` can be created by all user profiles.
        """
        # `Nationals`
        self.client.login(username='ks', password='ks')
        response = self.client.post('/identities/',
                                    {'first_name': 'Josh',
                                     'last_name': 'Eppinette',
                                     'gender': 'Male',
                                     'dob': '1994-05-12'})
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        # `Administrator`
        self.client.login(username='spsu', password='spsu')
        response = self.client.post('/identities/',
                                    {'first_name': 'Joe',
                                     'last_name': 'Biden',
                                     'gender': 'Male',
                                     'dob': '1994-05-12'})
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        # `Host`
        self.client.login(username='ksspsu', password='ksspsu')
        response = self.client.post('/identities/',
                                    {'first_name': 'Bobby',
                                     'last_name': 'Brown',
                                     'gender': 'Male',
                                     'dob': '1994-05-12'})
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_identity_no_updates(self):
        """
        Assert that `Identity` models cannot be updated.
        """
        # `Host`
        self.client.login(username='ksspsu', password='ksspsu')
        response = self.client.post('/identities/',
                                    {'first_name': 'Bobby',
                                     'last_name': 'Brown',
                                     'gender': 'Male',
                                     'dob': '1994-05-12'})
        content = json.loads(response.content)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        # Test `PUT`
        response = self.client.put('/identities/' + str(content['id']) + '/',
                                   {'first_name': 'Jonathan'})

        # Test `PATCH`
        response = self.client.patch('/identities/' + str(content['id']) + '/',
                                     {'first_name': 'Jonathan'})

        self.assertEquals(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    """
                             FLAG
    """

    def test_flag_admin_has_full_access(self):
        """
        Assert that an `is_superuser` has full access to the `Flag` resource.
        """
        # Admin log in
        self.client.login(username='josh', password='josh')

        # Create `Identities`
        response = self.client.post('/identities/',
                                    {'first_name': 'Bobby',
                                     'last_name': 'Brown',
                                     'gender': 'Male',
                                     'dob': '1994-05-12'})
        bobby_brown = json.loads(response.content)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        # Create `Flag`
        response = self.client.post('/flags/', 
                                    {'identity': str(bobby_brown['id']),
                                     'violation': 'Vandalism'})
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_flag_get_queryset_per_user_profile(self):
        """
        Assert that the `get_queryset` method is filtering correctly.
        """
        # Create `Identities`

        # As `Nationals`
        self.client.login(username='ks', password='ks')

        response = self.client.post('/identities/',
                                    {'first_name': 'Bobby',
                                     'last_name': 'Brown',
                                     'gender': 'Male',
                                     'dob': '1996-09-11'})
        bobby_brown = json.loads(response.content)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post('/identities/',
                                    {'first_name': 'Josh',
                                     'last_name': 'Eppinette',
                                     'gender': 'Male',
                                     'dob': '1994-05-12'})
        josh_eppinette = json.loads(response.content)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        # As `Administrator`
        self.client.login(username='spsu', password='spsu')

        response = self.client.post('/identities/',
                                    {'first_name': 'Joe',
                                     'last_name': 'Brooks',
                                     'gender': 'Male',
                                     'dob': '1976-03-01'})
        joe_brooks = json.loads(response.content)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post('/identities/',
                                    {'first_name': 'Sam',
                                     'last_name': 'Thomas',
                                     'gender': 'Female',
                                     'dob': '1994-02-22'})
        sam_thomas = json.loads(response.content)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        # As `Host`
        self.client.login(username='ksspsu', password='ksspsu')

        response = self.client.post('/identities/',
                                    {'first_name': 'Matt',
                                     'last_name': 'Maker',
                                     'gender': 'Male',
                                     'dob': '1992-04-03'})
        matt_maker = json.loads(response.content)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post('/identities/',
                                    {'first_name': 'Niles',
                                     'last_name': 'Smith',
                                     'gender': 'Female',
                                     'dob': '1991-06-25'})
        niles_smith = json.loads(response.content)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        # Create `Identities`

        # As `Nationals`
        self.client.login(username='ks', password='ks')

        response = self.client.post('/flags/', 
                                    {'identity': str(bobby_brown['id']),
                                     'violation': 'Vandalism'})
        bb_nat_flag = json.loads(response.content)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post('/flags/', 
                                    {'identity': str(josh_eppinette['id']),
                                     'violation': 'Stealing'})
        je_nat_flag = json.loads(response.content)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post('/flags/', 
                                    {'identity': str(niles_smith['id']),
                                     'violation': 'Stealing'})
        ns_nat_flag = json.loads(response.content)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        # As `Administrator`
        self.client.login(username='spsu', password='spsu')

        response = self.client.post('/flags/', 
                                    {'identity': str(matt_maker['id']),
                                     'violation': 'Probation'})
        mm_admin_flag = json.loads(response.content)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post('/flags/', 
                                    {'identity': str(sam_thomas['id']),
                                     'violation': 'Underage Drinking'})
        st_admin_flag = json.loads(response.content)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post('/flags/', 
                                    {'identity': str(joe_brooks['id']),
                                     'violation': 'Stealing'})
        jb_admin_flag = json.loads(response.content)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        # As `Host` `ksspsu`
        self.client.login(username='ksspsu', password='ksspsu')

        response = self.client.post('/flags/', 
                                    {'identity': str(joe_brooks['id']),
                                     'violation': 'Probation'})
        jb_host_flag = json.loads(response.content)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post('/flags/', 
                                    {'identity': str(josh_eppinette['id']),
                                     'violation': 'Probation'})
        je_host_flag = json.loads(response.content)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        # Test `get_queryset`
        
        # `Nationals`
        self.client.login(username='ks', password='ks')
        response = self.client.get('/flags/')
        content = json.loads(response.content)['results']
        self.assertEquals(len(content), 3)

        # `Administrator`
        self.client.login(username='spsu', password='spsu')
        response = self.client.get('/flags/')
        content = json.loads(response.content)['results']
        self.assertEquals(len(content), 3)

        # `Host`
        self.client.login(username='ksspsu', password='ksspsu')
        response = self.client.get('/flags/')
        content = json.loads(response.content)['results']
        self.assertEquals(len(content), 8)
