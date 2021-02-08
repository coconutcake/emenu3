<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="http://mign.pl/adds/logoemenu.png" alt="Project logo"></a>
</p>

<h3 align="center">eMenu</h3>

<div align="center">

[![Stauts](https://img.shields.io/travis/coconutcake/eMenu3)](https://travis-ci.org/github/coconutcake/emenu3)
[![Dependencies](https://img.shields.io/requires/github/coconutcake/eMenu3)](https://requires.io/github/coconutcake/emenu3/requirements/?branch=main)


</div>

---

<p align="center"> Zadanie eMenu
    <br> 
</p>

## 📝 Zawartość

- [O projekcie](#about)
- [Uruchomienie](#getting_started)




## 🧐 O projekcie <a name = "about"></a>

Projekt zadania opiera sie na poniższych kontenerach dockera :
- Python 3.8 z django
- Baza Postgres dla django
- Adminer
- Upstream server nginx

## 🚀 Uruchomienie <a name = "getting_started"></a>

Wykonaj klona jesli masz juz zainstalowanego dockera:
```
git clone https://github.com/coconutcake/eMenu.git
```

Po pobraniu klona, przejdz do folderu i zbuduj obrazy poleceniem:

```
docker-compose up --build
```

Aplikacja powinna być dostępna.
Aby zalogować sie na panel administracyjny należy pierw utworzyć konto superadmina.

```
docker exec -it emenu sh -c "python3 app/manage.py createsuperuser"
```

- Django -> [http://127.0.0.1:8833](http://127.0.0.1:8833) - Wymagana akceptacja samopodpisanego certyfikatu SSL
- Adminer -> [http://127.0.0.1:8080](http://127.0.0.1:8080)