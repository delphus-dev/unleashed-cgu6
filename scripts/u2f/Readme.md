# How to make U2F function work?
If all steps are followed correctly, the U2F application on Flipper will not return a certificate error and will function exactly as on the original. Unfortunately, for security reasons, this U2F certificate cannot be shared; each user must have their own certificate.


1. Install Python and the script dependency:

```bash
pip install cryptography
```

2. Run the `u2f_keygen.py`, it will close immediately, this is normal, after this two files will appear in the script directory: `cert.der` and `cert_key.u2f`
3. Place the `cert.der` and `cert_key.u2f` files on the SD card at u2f/assets/
