INSERT INTO "users" (username, useremail, password, token) 
VALUES
    ('Hermann', 'hermannnzeudeu@gmail.com', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f','aa287fce-0063-11ee-a7ce-f4b7e2bfc4e5'),
    ('Henn', 'henn@gmail.com', 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79','2a6722b9-0ad7-11ee-8a73-f4b7e2dc904a');

INSERT INTO "allow_to" (temp_hum, volt_int, smoke, token)
VALUES
    ('False', 'True', 'True','aa287fce-0063-11ee-a7ce-f4b7e2bfc4e5'),
    ('True', 'False', 'True','2a6722b9-0ad7-11ee-8a73-f4b7e2dc904a');