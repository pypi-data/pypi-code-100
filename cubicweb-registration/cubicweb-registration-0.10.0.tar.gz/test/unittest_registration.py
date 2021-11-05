import re
import urllib.parse
from contextlib import contextmanager

from cubicweb.crypto import encrypt, decrypt
from cubicweb.devtools.testlib import MAILBOX, CubicWebTC


class RegistrationTC(CubicWebTC):

    captcha_value = "captcha value"

    data = {
        "firstname-subject": "Toto",
        "surname-subject": "Toto",
        "email_address-subject": "toto@secondweb.fr",
        "login-subject": "toto",
        "upassword-subject": "toto",
        "upassword-subject-confirm": "toto",
        "captcha": captcha_value,
    }

    def setup_database(self):
        self.config.global_set_option("registration-cypher-seed", "dummy cypher key")
        super(RegistrationTC, self).setup_database()

    def _check_user_not_created(self):
        with self.admin_access.repo_cnx() as cnx:
            rset = cnx.execute(
                "CWUser X WHERE X login %(login)s",
                {"login": self.data["login-subject"]},
            )
            self.assertFalse(rset)

    def _check_error(
        self,
        req,
        path,
        expected_path="registration",
        expected_errors=None,
        expected_msg=None,
        expected_formvalues=None,
    ):
        path, params = self.expect_redirect_handle_request(req, path)
        self.assertEqual(path, expected_path)
        if expected_msg:
            self.assertMessageEqual(req, params, expected_msg)
        forminfo = req.session.data.get("registration")
        if forminfo is None:
            self.assertFalse(expected_errors or expected_formvalues)
        else:
            self.assertEqual(forminfo["eidmap"], {})
            self.assertEqual(forminfo["values"], expected_formvalues or {})
            error = forminfo["error"]
            self.assertEqual(error.entity, None)
            self.assertEqual(error.errors, expected_errors or {})

    def _posted_form(self, *skipkeys):
        data = self.data.copy()
        for key in skipkeys:
            data.pop(key, None)
        if "__errorurl" not in skipkeys:
            data["__errorurl"] = "registration"
        return data

    def test_registration_form(self):
        with self.admin_access.web_request() as req:
            req.form = {"firstname-subject": "Toto"}
            pageinfo = self.view("registration", req=req, rset=None)

        # check form field names
        names = pageinfo.etree.xpath(
            '//form[@id="registrationForm"]//input[@type!="hidden"]/@name'
        )
        self.assertEqual(set(names), set(self.data))

        # check form field value
        firstname = pageinfo.etree.xpath('//input[@name="firstname-subject"]/@value')
        self.assertEqual(firstname, [req.form["firstname-subject"]])

    def test_send_mail_ok(self):
        with self.new_access("anon").web_request() as req:
            req.form = self._posted_form()
            req.session.data["captcha"] = self.captcha_value
            path, params = self.expect_redirect_handle_request(
                req, "registration_sendmail"
            )
            self.assertEqual(path, "")
            self.assertMessageEqual(
                req,
                params,
                "Your registration email has been sent. "
                "Follow instructions in there to activate your account.",
            )
            # check email contains activation url...
            URL_RE = re.compile("(%s[^.]+)$" % self.config["base-url"], re.M)
            text = MAILBOX[-1].message.get_payload(decode=True)
            url = URL_RE.search(text).group(1)
            # ... and the registration key contains all data
            key = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(url)[3]))["key"]
            d = self._posted_form("upassword-subject-confirm")
            decrypred = decrypt(key, self.config["registration-cypher-seed"])
            decrypred["upassword-subject"] = decrypred["upassword-subject"].decode(
                "utf8"
            )
            self.assertDictEqual(decrypred, d)

    def test_send_mail_failure(self):
        for param, msg, val in (
            ("login-subject", "required field", None),
            ("captcha", "required field", None),
            ("captcha", "incorrect captcha value", "abc"),
        ):
            with self.admin_access.web_request() as req:
                if val is None:
                    req.form = self._posted_form(param)
                else:
                    req.form = self._posted_form()
                    req.form[param] = val
                req.session.data["captcha"] = self.captcha_value
                self._check_error(
                    req,
                    "registration_sendmail",
                    expected_formvalues=req.form,
                    expected_errors={param: msg},
                )
                self.assertEqual(req.session.data.get("captcha"), None)

    @contextmanager
    def _confirm_req(self, key=None, overriden={}):
        with self.new_access("anon").web_request() as req:
            data = self._posted_form("upassword-subject-confirm")
            data.update(overriden)
            if key is None:
                key = encrypt(data, self.config["registration-cypher-seed"])
            req.form = {"key": key}
            yield req

    def test_confirm_ok(self):
        with self._confirm_req() as req:
            path, params = self.expect_redirect_handle_request(
                req, "registration_confirm"
            )
            self.assertEqual(path, "")
            self.assertMessageEqual(
                req,
                params,
                "Congratulations, your registration is complete. "
                'You can now <a href="{}">login</a>.'.format(req.build_url("login")),
            )
        with self.admin_access.repo_cnx() as cnx:
            rset = cnx.execute(
                "Any U WHERE U login %(login)s, U firstname %(firstname)s, "
                "U surname %(surname)s, U use_email M, M address %(email_address)s",
                dict(
                    (k.replace("-subject", ""), v) for k, v in list(self.data.items())
                ),
            )
            self.assertTrue(rset)

    def test_confirm_failure_login_already_used(self):
        # try to recreate a 'admin' user.
        with self._confirm_req(overriden={"login-subject": "admin"}) as req:
            formvalues = self._posted_form(
                "upassword-subject", "upassword-subject-confirm"
            )
            formvalues["login-subject"] = "admin"
            # data = {'firstname-subject': 'Toto', 'surname-subject': 'Toto',
            #         'email_address-subject': 'toto@secondweb.fr',
            #         'login-subject': 'admin',
            #         'captcha': captcha_value}
            self._check_error(
                req,
                "registration_confirm",
                expected_formvalues=formvalues,
                expected_errors={
                    "login-subject": 'the value "admin" is already used, use another one'
                },
            )

    def test_confirm_failure_invalid_data(self):
        with self._confirm_req("dummykey") as req:
            self._check_error(
                req,
                "registration_confirm",
                "register",
                expected_msg="Invalid registration data. Please try registering again.",
            )
        self._check_user_not_created()

    def test_confirm_failure_email_already_used(self):
        with self.admin_access.web_request() as req:
            self.create_user(req, "test")
            req.execute(
                "INSERT EmailAddress X: U use_email X, X address %(email_address)s "
                'WHERE U login "test"',
                {"email_address": self.data["email_address-subject"]},
            )
            req.cnx.commit()
        with self._confirm_req() as req:
            req.form["__errorurl"] = "registration"
        self._check_user_not_created()


if __name__ == "__main__":
    import unittest

    unittest.main()
