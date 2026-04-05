import os
import datetime
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.x509 import (
    CertificateBuilder, NameAttribute, Name, random_serial_number,
    BasicConstraints, UnrecognizedExtension
)
from cryptography.x509.oid import NameOID, ObjectIdentifier
from cryptography import x509

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# FIDO U2F Transport extension OID (marks cert as U2F authenticator)
# Value: USB transport (bit 0 set) encoded as BIT STRING: 03 02 03 08
FIDO_U2F_TRANSPORT_OID = ObjectIdentifier("1.3.6.1.4.1.45724.2.1.1")
FIDO_U2F_TRANSPORT_VALUE = bytes([0x03, 0x02, 0x03, 0x08])  # USB transport

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()

    subject = issuer = Name([
        NameAttribute(NameOID.COMMON_NAME, u"Flipper Zero U2F"),
        NameAttribute(NameOID.ORGANIZATION_NAME, u"Flipper"),
        NameAttribute(NameOID.COUNTRY_NAME, u"US"),
    ])

    cert = (
        CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(public_key)
        .serial_number(random_serial_number())
        .not_valid_before(datetime.datetime.utcnow())
        .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365 * 10))
        .add_extension(BasicConstraints(ca=False, path_length=None), critical=True)
        .add_extension(
            UnrecognizedExtension(FIDO_U2F_TRANSPORT_OID, FIDO_U2F_TRANSPORT_VALUE),
            critical=False
        )
        .sign(private_key, hashes.SHA256())
    )

    cert_der = cert.public_bytes(serialization.Encoding.DER)

    # Validate DER format as Flipper firmware expects:
    # byte[0]=0x30, byte[1]=0x82, byte[2..3]=length, total=length+4
    assert cert_der[0] == 0x30, f"Bad DER tag: 0x{cert_der[0]:02x}"
    assert cert_der[1] == 0x82, (
        f"DER length prefix 0x{cert_der[1]:02x} != 0x82. Cert too small ({len(cert_der)} bytes)."
    )
    expected_len = ((cert_der[2] << 8) | cert_der[3]) + 4
    assert expected_len == len(cert_der), \
        f"DER length mismatch: expected {expected_len}, got {len(cert_der)}"

    cert_path = os.path.join(OUTPUT_DIR, "cert.der")
    with open(cert_path, "wb") as f:
        f.write(cert_der)
    print(f"[+] {cert_path} ({len(cert_der)} bytes)")
    print(f"    Header bytes: {cert_der[:4].hex()}")
    print(f"    byte[1]=0x{cert_der[1]:02x} ({'OK: 2-byte length' if cert_der[1]==0x82 else 'WARNING: not 0x82'})")

    priv_bytes = private_key.private_numbers().private_value.to_bytes(32, "big")
    priv_hex = " ".join(f"{b:02X}" for b in priv_bytes)

    key_path = os.path.join(OUTPUT_DIR, "cert_key.u2f")
    with open(key_path, "w", newline="\n") as f:
        f.write("Filetype: Flipper U2F Certificate Key File\n")
        f.write("Version: 1\n")
        f.write("Type: 2\n")
        f.write(f"Data: {priv_hex}\n")
    print(f"[+] {key_path}")

    print()
    print("Copy cert.der and cert_key.u2f to /ext/u2f/assets/ on SD card.")

if __name__ == "__main__":
    main()
