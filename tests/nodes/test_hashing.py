from src.cryptography_primitives import hashing

# Test suite for hashing.py
class TestHashing:
    def test_sha256(self):
        sha256 = hashing.SHA2()
        text = "Hello World"
        hashed_text = (sha256.sha2(key1=text, algorithm="SHA256"),)
        assert hashed_text[0][0] == "a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e"

    def test_blake2b(self):
        blake2b = hashing.BLAKE2()
        text = "Hello World"
        hashed_text = blake2b.blake2(key1=text, algorithm="BLAKE2b", digest_size=64)
        assert (
            hashed_text[0]
            == "4386a08a265111c9896f56456e2cb61a64239115c4784cf438e36cc851221972da3fb0115f73cd02486254001f878ab1fd126aac69844ef1c1ca152379d0a9bd"
        )

    def test_sha3_256(self):
        sha3_256 = hashing.SHA3()
        text = "Hello World"
        hashed_text = (sha3_256.sha3(key1=text, algorithm="SHA3_256"),)
        assert hashed_text[0][0] == "e167f68d6563d75bb25f3aa49c29ef612d41352dc00606de7cbd630bb2665f51"

    def test_sha1(self):
        sha1 = hashing.SHA1()
        text = "Hello World"
        hashed_text = (sha1.sha1(key1=text, algorithm=None),)
        assert hashed_text[0][0] == "0a4d55a8d778e5022fab701977c5d840bbc486d0"

    def test_md5(self):
        md5 = hashing.MD5()
        text = "Hello World"
        hashed_text = (md5.md5(key1=text, algorithm=None),)
        assert hashed_text[0][0] == "b10a8db164e0754105b7a99be72e3fe5"

    def test_sm3(self):
        sm3 = hashing.SM3()
        text = "Hello World"
        hashed_text = (sm3.sm3(key1=text, algorithm=None),)
        assert hashed_text[0][0] == "77015816143ee627f4fa410b6dad2bdb9fcbdf1e061a452a686b8711a484c5d7"

    def test_shake128(self):
        shake128 = hashing.SHAKE()
        text = "Hello World"
        hashed_text = shake128.shake(
            key1=text,
            algorithm="SHAKE128",
            output_length=32,
            digest_size=64,
            squeeze_bytes=16,
            squeeze_times=2,
        )
        assert (
            hashed_text[0][0]
            == "7f9c2ba4e88f827d616045507605853ed73b8093f6efbc88eb1a6eacfa66ef263cb1eea988004b93103cfb0aeefd2a686e01fa4a58e8a3639ca8a1e3f9ae57e2"
        )
