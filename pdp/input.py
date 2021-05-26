class PolicyDecisionPointInput(dict):
    """
    Input that is sent to the Policy Decision Point (PDP) as context to make an authz decision.
    """

    def __init__(
            self,
            schema: str = None,
            method: str = None,
            path: str = None,
            query: dict = None,
            headers: dict = None,
            source_ip: str = None,
            source_port: int = None,
            destination_ip: str = None,
            destination_port: int = None,
            **kwargs,
    ):
        """
        Initialize a PolicyDecisionPointInput object. This can be done using one of the reserved parameters listed
        below, which are structured conveniently for PDP to consume. Alternatively, the input can contain any keyword
        arguments apart from the reserved parameters, will be available as-is for the PDP to consume.

        :param schema: Request schema, example 'http'.
        :param method: Request method, example 'GET'.
        :param path: The server path that the request is made to.
        :param query: A dict representing the querystring. Keys are expected to be strings, whereas values can either be
                        strings or list of strings, for multi-value query params.
        :param headers: A dict representing request headers. Keys are expected to be strings, whereas values can either
                        be strings or list of strings, for multi-value headers.
        :param source_ip: The source IP address.
        :param source_port: The source port.
        :param destination_ip: The destination IP address.
        :param destination_port: The destination port.
        :param kwargs: Any keyword arguments apart from the reserved parameters that will be available as-is to the PDP.
        """
        super(PolicyDecisionPointInput, self).__init__(
            request={
                'schema': schema,
                'method': method,
                'path': path,

                # Multi-value queries and headers are converted to comma-separated stings for consistency.
                'query': self._normalize_multivalue_dict(query),
                'headers': self._normalize_multivalue_dict(headers),
            },

            source={
                'ipAddress': source_ip,
                'port': source_port,
            },

            destination={
                'ipAddress': destination_ip,
                'port': destination_port,
            },

            **kwargs,
        )

    @staticmethod
    def _normalize_multivalue_dict(d: dict) -> dict:
        if d is None:
            return {}

        for key, val in d.items():
            if isinstance(val, list):
                d[key] = ','.join(val)

        return d
