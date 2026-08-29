"""User accounts dataset."""

USERS = [
    {
        "id": 1,
        "name": "Demo Customer",
        "email": "customer@foodflow.local",
        "password_hash": "scrypt:32768:8:1$gUJiMLuBdmjKR1pE$248a76fdeef26d472570ddde2c76fea0439c5bd3d6d14372c0147020e32c075a2ae4e5286bb3c70a6b8198d2d90b5605e8b1fe7adaa50826ad6ec38d2f114b10",
        "role": "customer",
        "phone": "+91 98765 43210",
        "address": "Flat 402, Green Glen Layout, Bellandur, Bengaluru",
        "avatar": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80",
        "created_at": "2026-01-15"
    },
    {
        "id": 2,
        "name": "Paradise Biryani Owner",
        "email": "restaurant@foodflow.local",
        "password_hash": "scrypt:32768:8:1$pAP1HAPujMhIMq1K$8e4e1204d9ca40e5b4dd489d67c9638422bccd995da5b9fb808b39c553f43b0f3439ed226ba1427518026c0afbb702a41d247944d686bd4fa7f3d344b75fc87b",
        "role": "restaurant",
        "restaurant_id": 1,
        "phone": "+91 98123 45678",
        "address": "Road No. 36, Jubilee Hills, Hyderabad",
        "avatar": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80",
        "created_at": "2026-01-10"
    },
    {
        "id": 3,
        "name": "Ramesh Kumar (Delivery Agent)",
        "email": "delivery@foodflow.local",
        "password_hash": "scrypt:32768:8:1$XTwc1FA4y09hSbkA$fe560f583a617bc70173c6c8464b4795f61de87e0d1fb94d1e2de7dfee9acb51a0cbb998b8b43f773bf270c397096e0e656c5f91b23e9aa4ef616fa610e481ac",
        "role": "delivery",
        "phone": "+91 91234 56789",
        "vehicle": "Honda Activa (KA-01-EV-4021)",
        "address": "Indiranagar, Bengaluru",
        "avatar": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&auto=format&fit=crop&q=80",
        "created_at": "2026-02-01"
    },
    {
        "id": 4,
        "name": "System Administrator",
        "email": "admin@foodflow.local",
        "password_hash": "scrypt:32768:8:1$zu0w3evMhK7ihlCg$e983b7d3c996c45d51282752e1fd75822a247eb8003a2300c443d8fdbfd39e3927311e89363e0486afee87d18ecccd0bab9db9371afa6a10db3cf9c190cba06a",
        "role": "admin",
        "phone": "+91 99999 00000",
        "address": "FoodFlow HQ, Electronic City, Bengaluru",
        "avatar": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&auto=format&fit=crop&q=80",
        "created_at": "2026-01-01"
    }
]
