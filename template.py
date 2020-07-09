product_attributes = {'attributes': [{'sae': {'id': 7284,
                                         '0W20': '2',
                                         '5W30': '25',
                                         '5W40': '26',
                                         '10W40': '8'},
                                 'oil_type': {'id': 7286,
                                              'mineral': '1',
                                              'HC-syntetic': '2',
                                              'semi-syntetic': '3',
                                              'syntetic': '4'
                                 },
                                 'type': {'id': 8229,
                                          'motor': '5872',
                                 },
                                      }
                                     ]
                      }
print(product_attributes['attributes'][0]['model_name']['id'])