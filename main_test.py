import unittest
import requests

class TestMain(unittest.TestCase):
    """unit test for API validation"""
    
    uri = "http://localhost:80/prediction"
        

    def test_no_header(self):
        res = requests.post(self.uri)
        self.assertEquals(res.status_code,403)
        self.assertEquals(res.json(),{"error_code":"you need a token to use the api, please contact the administrator"})
        
    def test_blank_header(self):
        headers = {}
        res = requests.post(self.uri,headers=headers)
        self.assertEquals(res.status_code,403)
        self.assertEquals(res.json(),{"error_code":"you need a token to use the api, please contact the administrator"})
        
    def test_invalid_header(self):
        headers = {"dc_token":""}
        res = requests.post(self.uri,headers=headers)
        self.assertEquals(res.status_code,401)
        self.assertEquals(res.json(),{"error_code":"Invalid token"})
        
    def test_no_data(self):
        headers = {"dc_token":"NrVvPG07nmraB7hW4jUc"}
        payload = {}
        res = requests.post(self.uri, params=payload, headers=headers)
        self.assertEquals(res.status_code,406)
        self.assertEquals(res.json(),{"error_code":"No document provided"})
        
    def test_badformat_data(self):
        headers = {"dc_token":"NrVvPG07nmraB7hW4jUc"}
        payload = {"words":"uio 879 -= &$"}
        res = requests.post(self.uri, params=payload, headers=headers)
        self.assertEquals(res.status_code,417)
        self.assertEquals(res.json(),{"error_code":"the document can only contains alphanumeric and space"})
        
    def test_good_data(self):
        headers = {"dc_token":"NrVvPG07nmraB7hW4jUc"}
        payload = {"words":"8d21095e8690 b208ae1e8232 4e5019f629a9 a86f2ba617ec 1c3862c83008 f8b0c07e306c f1c9f7517642 377a21b394dc 5071d8aa3768 46c88d9303da 959b4c0a0bb7 d931e701e475 93790ade6682 448cca02dae6 4357c81e10c1 04503bc22789 a31962fbd5f3 1d4249bb404a b61f1af56200 737f89bbbca2 036087ac04f9 b136f6349cf3 c33b5c3d0449 5c4ab6d55c36 caecbc15a560 e67eb757a353 586242498a88 6d25574664d2 e0a08df8ec4c 9cdf4a63deb0 6101ed18e42f b59e343416f7 4e5019f629a9 45238a6f945e 133d46f7ed38 94cfc0229e9f c337a85b8ef9 9f11111004ec f9b20c280980 a9ee836e8303 6bf9c0cb01b4 8fc4ec925d63 c337a85b8ef9 04503bc22789 f0666bdbc8a5 5c02c2aaa67b ef4ba44cdf5f 2b3cd09a5f3f b02eb907dd1a d38820625542 d08444793824 cc9e05bc2a86 746b67da2da6 4a25312439bf fc25f79e6d18 7d9e333a86da ce1f034abb5d 5b023dd25b4b 2d00e7e4d33f 98d0d51b397c fe081ae57a8b fe286bb08719 eeb86a6a04e4 57e641d8b3b5 eb4baad85df9 610915fceac6 ed214114032c 65f888439937 7d9e333a86da c99723547aac 37ba1eb08496 585bc9de3d49 d02e0be86f53 93790ade6682 37ac79620fc6 4357c81e10c1 0f88ca127938 a31962fbd5f3 f11e7777d8b5 b61f1af56200 eb562127f33e 036087ac04f9 f86490d29db0 b136f6349cf3 cc9e05bc2a86 07e7fe209a3b 93c988b67c47 6240cd5376cf e67eb757a353 edd357b65c83 578830762b27 ea51fa83c91c 9cdf4a63deb0 b59e343416f7 04503bc22789 5c02c2aaa67b 1d4249bb404a 4ad52689d690 a024d1e04168 c337a85b8ef9 2d00e7e4d33f b9699ce57810 594fa5190917 b32153b8b30c 6d25574664d2 1015893e384a 33bfc554cf75 1bc29dc7f887 9e931fae0f23 798fe9915030 07c96d6f390e 3c1f7c78e687 d5a8566dd908 aaf38e8aa6d1 80650ef942e3 14156d1fa057 d17504d2c1e7 010bdb69ff0a 6f6729c54a07 ef4ba44cdf5f b02eb907dd1a d38820625542 7d9e333a86da 37ba1eb08496 f77ad3479ff2 73801426ea65 98d0d51b397c 43565b1afa44 05aa4caf0954 77a36cacbb45"}
        res = requests.post(self.uri, params=payload, headers=headers)
        self.assertEquals(res.status_code,200)
        self.assertEquals(res.json(),{"prediction" : "REINSTATEMENT NOTICE" , "confidence" : 0.6409})    