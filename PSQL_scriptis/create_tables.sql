
--учетные данные пользователя
CREATE TABLE public.user(
   ID serial primary key,
   email               VARCHAR(255) ,
   password            VARCHAR(255),
   expiresIn           INTEGER,
   idToken             VARCHAR(255),
   kind                VARCHAR(255) ,
   localId             VARCHAR(255) ,
   refreshToken        VARCHAR(255)
);
CREATE INDEX  ON public.user (email);


--история авторизаций
CREATE TABLE public.auth_history(
   ID serial primary key,
   user_id			INTEGER,
   entry_date		TIMESTAMP
);
