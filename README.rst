Pushing Container Images from Openshift to External Registries
--------------------------------------------------------------

This repo is a wrapper around [skopeo](https://github.com/containers/skopeo)
that allows to push container images from Openshift to external container
registries.

How to use it
=============

You can manage all the dependencies using the provided Pipfile. In order to use
the image pusher simply run the following commands:

.. code-block:: console

        pipenv install --dev  # create the virtual environment
        python app.py push --src=SOURCE_REGISTRY --dst=TARGET_REGISTRY

Additionally, you can use the following optional arguments with the above
command:

* ``--user-src`` : The *username* used in the *source* registry

* ``--pass-src`` : The *password* for the *source* registry

* ``--user-dst`` : The *username* used in the *target* registry

* ``--pass-dst`` : The *password* for the *target* registry
