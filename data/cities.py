"""Multi-city delivery zones dataset."""

CITIES = [
    {
        "id": 1,
        "name": "Hyderabad",
        "state": "Telangana",
        "country": "India",
        "lat": 17.385044,
        "lng": 78.486671,
        "is_active": True,
        "delivery_zones": [
            {
                "zone_id": 101,
                "name": "Jubilee Hills",
                "pincode": "500033",
                "hub_code": "HYD-JH-01"
            },
            {
                "zone_id": 102,
                "name": "Banjara Hills",
                "pincode": "500034",
                "hub_code": "HYD-BH-02"
            },
            {
                "zone_id": 103,
                "name": "Gachibowli",
                "pincode": "500032",
                "hub_code": "HYD-GB-03"
            },
            {
                "zone_id": 104,
                "name": "HITECH City",
                "pincode": "500081",
                "hub_code": "HYD-HC-04"
            },
            {
                "zone_id": 105,
                "name": "Madhapur",
                "pincode": "500081",
                "hub_code": "HYD-MP-05"
            },
            {
                "zone_id": 106,
                "name": "Kondapur",
                "pincode": "500084",
                "hub_code": "HYD-KP-06"
            },
            {
                "zone_id": 107,
                "name": "Kukatpally",
                "pincode": "500072",
                "hub_code": "HYD-KK-07"
            },
            {
                "zone_id": 108,
                "name": "Secunderabad",
                "pincode": "500003",
                "hub_code": "HYD-SC-08"
            },
            {
                "zone_id": 109,
                "name": "Begumpet",
                "pincode": "500016",
                "hub_code": "HYD-BP-09"
            },
            {
                "zone_id": 110,
                "name": "Ameerpet",
                "pincode": "500016",
                "hub_code": "HYD-AP-10"
            }
        ]
    },
    {
        "id": 2,
        "name": "Bengaluru",
        "state": "Karnataka",
        "country": "India",
        "lat": 12.971599,
        "lng": 77.594566,
        "is_active": True,
        "delivery_zones": [
            {
                "zone_id": 201,
                "name": "Indiranagar",
                "pincode": "560038",
                "hub_code": "BLR-IN-01"
            },
            {
                "zone_id": 202,
                "name": "Koramangala 5th Block",
                "pincode": "560095",
                "hub_code": "BLR-KM-02"
            },
            {
                "zone_id": 203,
                "name": "HSR Layout",
                "pincode": "560102",
                "hub_code": "BLR-HSR-03"
            },
            {
                "zone_id": 204,
                "name": "Whitefield",
                "pincode": "560066",
                "hub_code": "BLR-WF-04"
            },
            {
                "zone_id": 205,
                "name": "Electronic City",
                "pincode": "560100",
                "hub_code": "BLR-EC-05"
            },
            {
                "zone_id": 206,
                "name": "Bellandur",
                "pincode": "560103",
                "hub_code": "BLR-BL-06"
            },
            {
                "zone_id": 207,
                "name": "JP Nagar",
                "pincode": "560078",
                "hub_code": "BLR-JPN-07"
            },
            {
                "zone_id": 208,
                "name": "Jayanagar",
                "pincode": "560041",
                "hub_code": "BLR-JYN-08"
            },
            {
                "zone_id": 209,
                "name": "MG Road",
                "pincode": "560001",
                "hub_code": "BLR-MGR-09"
            },
            {
                "zone_id": 210,
                "name": "Malleshwaram",
                "pincode": "560003",
                "hub_code": "BLR-ML-10"
            }
        ]
    },
    {
        "id": 3,
        "name": "Mumbai",
        "state": "Maharashtra",
        "country": "India",
        "lat": 19.07609,
        "lng": 72.877426,
        "is_active": True,
        "delivery_zones": [
            {
                "zone_id": 301,
                "name": "Bandra West",
                "pincode": "400050",
                "hub_code": "MUM-BW-01"
            },
            {
                "zone_id": 302,
                "name": "Juhu Chowpatty",
                "pincode": "400049",
                "hub_code": "MUM-JH-02"
            },
            {
                "zone_id": 303,
                "name": "Powai Hiranandani",
                "pincode": "400076",
                "hub_code": "MUM-PW-03"
            },
            {
                "zone_id": 304,
                "name": "Andheri West",
                "pincode": "400053",
                "hub_code": "MUM-AW-04"
            },
            {
                "zone_id": 305,
                "name": "Colaba Fort",
                "pincode": "400005",
                "hub_code": "MUM-CL-05"
            },
            {
                "zone_id": 306,
                "name": "Lower Parel",
                "pincode": "400013",
                "hub_code": "MUM-LP-06"
            },
            {
                "zone_id": 307,
                "name": "Thane West",
                "pincode": "400601",
                "hub_code": "MUM-TH-07"
            },
            {
                "zone_id": 308,
                "name": "Navi Mumbai Vashi",
                "pincode": "400703",
                "hub_code": "MUM-NM-08"
            }
        ]
    },
    {
        "id": 4,
        "name": "New Delhi",
        "state": "Delhi",
        "country": "India",
        "lat": 28.613939,
        "lng": 77.209021,
        "is_active": True,
        "delivery_zones": [
            {
                "zone_id": 401,
                "name": "Connaught Place",
                "pincode": "110001",
                "hub_code": "DEL-CP-01"
            },
            {
                "zone_id": 402,
                "name": "Lajpat Nagar",
                "pincode": "110024",
                "hub_code": "DEL-LN-02"
            },
            {
                "zone_id": 403,
                "name": "Hauz Khas Village",
                "pincode": "110016",
                "hub_code": "DEL-HK-03"
            },
            {
                "zone_id": 404,
                "name": "Greater Kailash",
                "pincode": "110048",
                "hub_code": "DEL-GK-04"
            },
            {
                "zone_id": 405,
                "name": "Gurugram Cyber City",
                "pincode": "122002",
                "hub_code": "DEL-GG-05"
            },
            {
                "zone_id": 406,
                "name": "Noida Sector 18",
                "pincode": "201301",
                "hub_code": "DEL-ND-06"
            }
        ]
    },
    {
        "id": 5,
        "name": "Chennai",
        "state": "Tamil Nadu",
        "country": "India",
        "lat": 13.08268,
        "lng": 80.270718,
        "is_active": True,
        "delivery_zones": [
            {
                "zone_id": 501,
                "name": "T. Nagar",
                "pincode": "600017",
                "hub_code": "MAA-TN-01"
            },
            {
                "zone_id": 502,
                "name": "Adyar",
                "pincode": "600020",
                "hub_code": "MAA-AD-02"
            },
            {
                "zone_id": 503,
                "name": "Velachery",
                "pincode": "600042",
                "hub_code": "MAA-VL-03"
            },
            {
                "zone_id": 504,
                "name": "Anna Nagar",
                "pincode": "600040",
                "hub_code": "MAA-AN-04"
            },
            {
                "zone_id": 505,
                "name": "Mylapore",
                "pincode": "600004",
                "hub_code": "MAA-MY-05"
            }
        ]
    },
    {
        "id": 6,
        "name": "Kolkata",
        "state": "West Bengal",
        "country": "India",
        "lat": 22.572646,
        "lng": 88.363895,
        "is_active": True,
        "delivery_zones": [
            {
                "zone_id": 601,
                "name": "Park Street",
                "pincode": "700016",
                "hub_code": "CCU-PS-01"
            },
            {
                "zone_id": 602,
                "name": "Salt Lake Sector 5",
                "pincode": "700091",
                "hub_code": "CCU-SL-02"
            },
            {
                "zone_id": 603,
                "name": "Ballygunge",
                "pincode": "700019",
                "hub_code": "CCU-BG-03"
            },
            {
                "zone_id": 604,
                "name": "New Town Rajarhat",
                "pincode": "700156",
                "hub_code": "CCU-NT-04"
            }
        ]
    },
    {
        "id": 7,
        "name": "Pune",
        "state": "Maharashtra",
        "country": "India",
        "lat": 18.52043,
        "lng": 73.856744,
        "is_active": True,
        "delivery_zones": [
            {
                "zone_id": 701,
                "name": "Viman Nagar",
                "pincode": "411014",
                "hub_code": "PNQ-VN-01"
            },
            {
                "zone_id": 702,
                "name": "Koregaon Park",
                "pincode": "411001",
                "hub_code": "PNQ-KP-02"
            },
            {
                "zone_id": 703,
                "name": "Baner Road",
                "pincode": "411045",
                "hub_code": "PNQ-BN-03"
            },
            {
                "zone_id": 704,
                "name": "Kothrud",
                "pincode": "411038",
                "hub_code": "PNQ-KT-04"
            }
        ]
    },
    {
        "id": 8,
        "name": "Ahmedabad",
        "state": "Gujarat",
        "country": "India",
        "lat": 23.022505,
        "lng": 72.571362,
        "is_active": True,
        "delivery_zones": [
            {
                "zone_id": 801,
                "name": "Ellis Bridge",
                "pincode": "380006",
                "hub_code": "AMD-EB-01"
            },
            {
                "zone_id": 802,
                "name": "Bodakdev SG Highway",
                "pincode": "380054",
                "hub_code": "AMD-SG-02"
            },
            {
                "zone_id": 803,
                "name": "Navrangpura",
                "pincode": "380009",
                "hub_code": "AMD-NV-03"
            }
        ]
    }
]
