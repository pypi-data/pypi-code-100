import logging

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.test import Client, TestCase
from django.urls import reverse

from cms.contacts.tests import ContactUnitTest

from cms.contexts.tests import ContextUnitTest

from cms.pages.models import PageContact
from cms.pages.tests import PageUnitTest


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class PageContactAPIUnitTest(TestCase):

    def setUp(self):
        pass

    def test_page_contact(self):
        """
        Page Contact API
        """
        req = Client()
        user2 = ContextUnitTest.create_user(username='staff',
                                            is_staff=True)

        ebu = ContextUnitTest.create_editorialboard_user()
        user = ebu.user
        webpath = ebu.webpath
        site = webpath.site

        page = PageUnitTest.create_page()
        page.webpath = webpath
        page.save()

        # page contacts list
        url = reverse('unicms_api:editorial-board-site-webpath-page-contacts',
                      kwargs={'site_id': site.pk,
                              'webpath_id': webpath.pk,
                              'page_id': page.pk})

        # accessible to staff users only
        res = req.get(url)
        assert res.status_code == 403
        # site is not managed by user2
        req.force_login(user2)
        res = req.get(url)
        assert res.status_code == 403
        # user is staff
        user.is_staff = True
        user.is_superuser = True
        user.save()
        req.force_login(user)
        res = req.get(url)
        assert isinstance(res.json(), dict)

        # POST
        contact = ContactUnitTest.create_contact()
        data = {'page': page.pk,
                'contact': contact.pk,
                'is_active': True
                }
        # user hasn't permission
        req.force_login(user2)
        res = req.post(url, data=data, follow=1,
                       content_type='application/json')
        assert res.status_code == 403
        # user has permission
        req.force_login(user)
        res = req.post(url, data=data, follow=1,
                       content_type='application/json')
        page_contact = PageContact.objects.filter(contact=contact).last()
        assert page_contact

        # GET LOGS
        url = reverse('unicms_api:editorial-board-site-webpath-page-contact-logs',
                      kwargs={'site_id': site.pk,
                              'webpath_id': webpath.pk,
                              'page_id': page.pk,
                              'pk': contact.pk})
        res = req.get(url, content_type='application/json',)
        assert isinstance(res.json(), dict)

        # redis lock set
        ct = ContentType.objects.get_for_model(page_contact)
        data = {'content_type_id': ct.pk,
                'object_id': page_contact.pk}
        res = req.post(url, data,
                       content_type='application/json', follow=1)
        assert isinstance(res.json(), dict)


        # GET, patch, put, delete
        url = reverse('unicms_api:editorial-board-site-webpath-page-contact',
                      kwargs={'site_id': site.pk,
                              'webpath_id': webpath.pk,
                              'page_id': page.pk,
                              'pk': page_contact.pk})

        # GET
        res = req.get(url, content_type='application/json',)
        assert isinstance(res.json(), dict)

        # PATCH
        data = {'is_active': False}
        # user hasn't permission
        req.force_login(user2)
        res = req.patch(url, data,
                        content_type='application/json',
                        follow=1)
        assert res.status_code == 403
        # user has permission on page
        page.created_by = user2
        page.save()
        ebu3 = ContextUnitTest.create_editorialboard_user(user=user2,
                                                          webpath=webpath,
                                                          permission=3)
        user2.refresh_from_db()
        req.force_login(user2)
        res = req.patch(url, data,
                        content_type='application/json',
                        follow=1)
        page_contact.refresh_from_db()
        assert not page_contact.is_active

        # PUT
        page.created_by = None
        page.save()
        data = {'page': page.pk,
                'contact': page_contact.pk,
                'is_active': True
        }
        # user hasn't permission
        req.force_login(user2)
        res = req.put(url, data, follow=1,
                      content_type='application/json')
        assert res.status_code == 403
        # user has permission
        req.force_login(user)
        res = req.put(url, data, follow=1,
                      content_type='application/json')
        page_contact.refresh_from_db()
        assert page_contact.is_active

        # DELETE
        # user hasn't permission
        req.force_login(user2)
        res = req.delete(url)
        assert res.status_code == 403
        # user has permission
        req.force_login(user)
        res = req.delete(url)
        try:
            page_contact.refresh_from_db()
        except ObjectDoesNotExist:
            assert True

        # form
        url = reverse('unicms_api:editorial-board-site-webpath-page-contact-form',
                      kwargs={'site_id': site.pk,
                              'webpath_id': webpath.pk,
                              'page_id': page.pk})
        res = req.get(url)
        assert isinstance(res.json(), list)
