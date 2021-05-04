# vaccinekabmilega
Vaccine कब मिलेगा?

## Installation

Requires Python 2.7+ to work and a Twilio account to send SMS.

```
TWILIO_ACCOUNT_SID= TWILIO_AUTH_TOKEN= TWILIO_MESSAGING_SERVICE_SID= \
    python main.py --pincode 110001 --age 18
```

Available parameters:

- `--age` (default is 18)
- `--pincode`
- `--vaccine` (COVISHIELD or COVAXIN. The default is COVISHIELD)
- `--phone` (used for sending SMS. Must be of the format +91..........)

## Notes

Please use this script responsibly. Any misuse of the API, although it is public, will only create problems for everyone.

