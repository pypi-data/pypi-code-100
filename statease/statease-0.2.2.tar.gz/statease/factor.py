class Factor:
    """Factor

The Factor class holds information about an individual Factor in
Stat-Ease 360. Instances of this class are typically created by
:func:`statease.client.SEClient.get_factor`

Attributes:
    name (str): the name of the factor

    units (str): the units of the factor

    values (tuple): the values of the factor, in run order

    low (str, **read only**): the actual low that corresponds to the *coded* low (this is usually, but not necessarily, the minimum observed value)

    high (str, **read only**): the actual high that corresponds to the *coded* high (this is usually, but not necessarily, the maximum observed value)

    coded_low (str, **read only**): the coded low value, typically -1 or 0

    coded_high (str, **read only**): the coded high value, typically 1
"""

    def __init__(self, client, name):
        self._client = client
        self._name = name

        result = self._client.send_payload({
            "method": "GET",
            "uri": "design/factor/" + self._name,
        })

        # overwrite the user entered name with the properly capitalized one
        self._name = result['payload'].get('name', self.name)
        self._units = result['payload'].get('units', '')
        self._values = tuple(result['payload'].get('values', []))
        self._coded_low = result['payload'].get('coded_low', -1)
        self._coded_high = result['payload'].get('coded_high', 1)
        self._actual_low = result['payload'].get('actual_low', -1)
        self._actual_high = result['payload'].get('actual_high', 1)
        self._is_categorical = result['payload'].get('is_categorical',None)
        self._coded_values = tuple(result['payload'].get('coded_values', []))
        if (self._is_categorical):
          # Convert inner nested lists to tuples for efficiency
          self._coded_values = tuple([ tuple(sublist) if sublist is not None else None for sublist in self._coded_values])

    def __str__(self):
        return 'name: "{}"\nunits: "{}"\ncoded low: {} <-> {}\ncoded high: {} <-> {}\nis_categorical: {}'.format(
            self._name,
            self._units,
            self._actual_low,
            self._coded_low,
            self._actual_high,
            self._coded_high,
            self._is_categorical
        )

    @property
    def name(self):
        return self._name

    @property
    def units(self):
        return self._units

    @property
    def coded_high(self):
        return self._coded_high

    @property
    def coded_low(self):
        return self._coded_low

    @property
    def low(self):
        return self._actual_low

    @property
    def high(self):
        return self._actual_high

    @property
    def actual_low(self):
        return self._actual_low

    @property
    def actual_high(self):
        return self._actual_high

    @property
    def values(self):
        """Get or set the factor values. When setting the factor values, you may use
        either a list or a dictionary. If fewer values are assigned than there are rows
        in the design, they will be filled in starting with first row. If a dictionary
        is used, it must use integers as keys, and it will fill factor values in rows
        indexed by the dictionary keys. The indices are 0-based, so the first row is
        index 0, the second index 1, and so on.

        :Example:
            >>> # sets the first 4 rows to a list of values
            >>> factor.values = [.1, .2, .3, .4]
            >>> # sets the 7th through 10th rows to specific values
            >>> factor.values = { 6: .1, 7: .2, 8: .3, 9: .4 }
            >>> # sets the 6th run to a specific value
            >>> factor.values = { 5: .8 }
        """
        return self._values

    @values.setter
    def values(self, factor_values):
        result = self.post("set", {"factor_values": factor_values })
        self._values = tuple(result['payload']['values'])
        self._coded_values = tuple(result['payload']['coded_values'])
        self._coded_high = result['payload'].get('coded_high', 1)
        self._coded_low = result['payload'].get('coded_low', -1)
        self._actual_low = result['payload'].get('actual_low', -1)
        self._actual_high = result['payload'].get('actual_high', 1)

    @property
    def coded_values(self):
        """Get the coded factor values in the current coding.

        :Example:
            >>> # get a list of the coded values
            >>> xc = factor.coded_values
        """
        return self._coded_values

    def is_categorical(self):
      """Test for categorical factor type.

        :Example:
            >>> # get a list of the coded values
            >>> #  values if the factor is categorical
            >>> x = []
            >>> if (factor.is_categorical):
            >>>   x = factor.coded_values
            >>> else: # Factor is not categorical
            >>>   x = factor.values
        """
      return self._is_categorical

    def post(self, endpoint, payload):
        return self._client.send_payload({
            "method": "POST",
            "uri": "design/factor/{}/{}".format(self._name, endpoint),
            **payload,
        })
