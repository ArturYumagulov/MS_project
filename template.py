product_attributes = {'attributes': [{'sae': {'id': 7284,
                                              '0W20': '2',
                                              '5W30': '25',
                                              '5W40': '26',
                                              '10W40': '8'},
                                      'oil_type': {'id': 7286,
                                                   'mineral': '1',
                                                   '4100': '3',
                                                   '6100': '4',
                                                   '8100': '4'
                                                   },
                                      'type': {'id': 8229,
                                               'motor': '5872',
                                               },
                                      'API': {'id': 7288,
                                              'SN/CF': '10'},
                                      'engine_type': {'id': 7290,
                                                      '4-тактный': '2'}
                                      }
                                     ]
                      }
if __name__ == '__main__':
    print(product_attributes['attributes'][0]['engine_type'])