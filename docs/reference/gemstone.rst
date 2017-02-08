The ``gemstone`` module (main classes)
======================================

Core classes
------------

.. autoclass:: gemstone.MicroService
    :members:

    .. autoattribute:: gemstone.MicroService.name
        :annotation: = a string representing the name of the service. MUST be specified by user

    .. autoattribute:: gemstone.MicroService.host
        :annotation: = a string representing the address or host to bind. Defaults to 127.0.0.1

    .. autoattribute:: gemstone.MicroService.port
        :annotation: = an integer representing the port to bind. Defaults to 8000

    .. autoattribute:: gemstone.MicroService.endpoint
        :annotation: = an string that says the url path where the service endpoint will be located.
                    Defaults to "/api"

    .. autoattribute:: gemstone.MicroService.accessible_at
        :annotation: = a full-url that specifies where the service can be accessible. Should be defined by the
                    user when the microservice is not directly accessible because it runs behind a load balancer
                    or reverse proxy. Defaults to http://{host}:{port}{endpoint}

    .. autoattribute:: gemstone.MicroService.max_parallel_blocking_tasks
        :annotation: = an integer representing how many parallel tasks can be executed in parallel. Defaults to os.cpu_count()

    .. autoattribute:: gemstone.MicroService.validation_strategies
        :annotation: = a list of validation strategy objects that will try to extract the api token from
                    various sources in order to validate the access to the private methods. See :ref:`token_validation`
                    for more details.

    .. autoattribute:: gemstone.MicroService.extra_handlers
        :annotation: = A list of tuples of form (url_expression, tornado_handler) that will be added to the default
                Tornado application.

    .. autoattribute:: gemstone.MicroService.template_dir
        :annotation: = The path of the directory where the default Tornado application will look for templates. To
                read more about how to use templates in Tornado, see http://www.tornadoweb.org/en/stable/template.html

    .. autoattribute:: gemstone.MicroService.static_dirs
        :annotation: = A list of directory paths in which the default Tornado app will search for static files.

    .. autoattribute:: gemstone.MicroService.periodic_tasks
        :annotation: = A list of tuples of functions and an integer, that schedules the function to be executed every
                given seconds in an asynchronous manner (there might be a slight delay in the function execution,
                depending on the io loop availability).

    .. autoattribute:: gemstone.MicroService.service_registry_urls
        :annotation: = A list of strings that represent the urls where the service registries are located. Pings them
                on service startup. The service registry must expose a ping(name, host, port) method and
                a locate_service(name) method via JSON RPC.

    .. autoattribute:: gemstone.MicroService.service_registry_ping_interval
        :annotation: = The number of seconds between ``ping`` requests to the service registries.


.. autoclass:: gemstone.RemoteService
    :members:

    .. autoattribute:: gemstone.RemoteService.methods
        :annotation: = A proxy object through which methods from the remote service can be invoked. Example usage

                        ::

                           client = RemoteService(api_url)
                           result = client.methods.method_to_call(arguments)

    .. autoattribute:: gemstone.RemoteService.notifications
        :annotation: = A proxy object through which methods from the remote service can be invoked as notifications.
                       (no answer is expected). Example usage:

                        ::

                           client = RemoteService(api_url)
                           client.notifications.method_to_call(arguments)  # returns None





Decorators
----------

.. autofunction:: gemstone.public_method

.. autofunction:: gemstone.private_api_method

Request handlers
----------------

.. autoclass:: gemstone.TornadoJsonRpcHandler
    :members: