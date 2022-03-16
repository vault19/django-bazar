=====
Bazar
=====

.. image:: https://img.shields.io/pypi/pyversions/django-bazar.svg
   :alt: PyPI - Python Version
   :target: https://pypi.org/project/django-bazar/

.. image:: https://img.shields.io/pypi/djversions/django-bazar
   :alt: PyPI - Django Version
   :target: https://pypi.org/project/django-bazar/

.. image:: https://img.shields.io/pypi/format/django-bazar
   :alt: PyPI - Format
   :target: https://pypi.org/project/django-bazar/

.. image:: https://img.shields.io/github/checks-status/vault19/django-bazar/main
   :alt: GitHub branch checks state
   :target: https://github.com/vault19/django-bazar/actions

.. image:: https://img.shields.io/github/license/vault19/django-bazar.svg
   :alt: LICENSE
   :target: https://github.com/vault19/django-bazar/blob/master/LICENSE

Bazar is a simple Django app to redistribute things (or services) online (both new and reused). Application is already used by civic association
`Vault19 o.z. <https://vault19.eu/>`_ (non-profit) for project that helps Ukrainian refugees in Orava (Slovakia):
https://pomoc.vault19.eu

Quick start
-----------

1. Install django-bazar via pip::

    pip install django-bazar

Alternatively install latest development version from Github::

    pip install https://github.com/vault19/django-bazar/archive/refs/heads/main.zip

2. Add "bazar" and "markdownify.apps.MarkdownifyConfig" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'markdownify.apps.MarkdownifyConfig',
        'bazar',
    ]

3. Include the polls URLconf in your project urls.py like this::

    path("", include("bazar.urls")),

4. Run `python manage.py migrate` to create the courses tables in DB.

5. Start the development server and visit http://127.0.0.1:8000/admin/
   to manage your courses (you'll need the Admin app enabled).

6. Visit http://127.0.0.1:8000/ to view the courses list.

Contributing
------------

All contributions are welcome! It doesnt have to be code, there are more possibilities how to get involved.

We have written extensive how to for beginners. Read more in our `documentation <https://vault19.github.io/django-bazar/html/contributing.html>`_.

Support
-------

`Vault19 o.z. <https://vault19.eu>`_ (non profit micro hackerspace) did this app to help. It is open sourced so you can help too.

We like to program and we wanted to design a clean
`Django <https://www.djangoproject.com/>`_ app and learn one or two things in the process...

If you can please Donate Money to help Ukraine fight against Russian Agressor.