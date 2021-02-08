<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="http://mign.pl/adds/logoemenu.png" alt="Project logo"></a>
</p>

<h3 align="center">eMenu</h3>

<div align="center">

[![Stauts](https://img.shields.io/travis/coconutcake/eMenu3)](https://travis-ci.org/github/coconutcake/emenu3)
[![Requirements Status](https://requires.io/github/coconutcake/emenu3/requirements.svg?branch=main)](https://requires.io/github/coconutcake/emenu3/requirements/?branch=main)

</div>

---

<p align="center"> Zadanie eMenu
    <br> 
</p>

## 📝 Zawartość

- [O projekcie](#about)
- [Uruchomienie](#getting_started)
- [API](#api)




## 🧐 O projekcie <a name = "about"></a>

Podział kontenerów Dockera:
- Python 3.8 z django
- Baza Postgres dla django
- Adminer
- Upstream server nginx
- Cron jako daemon do wysylki maili o wskazanej godzinie

Aplikacja:

- Aplikacja wykonana wg metodyki TDD. 
- Krycie testami na poziomie ~90% 
- Projekt został zintegrowany z Travis CI -> https://travis-ci.org/github/coconutcake/eMenu3
- Wersje zależności requirements -> https://requires.io/github/coconutcake/emenu3/requirements/?branch=main
- Raportowanie rozwiązane za pomocą daemona uruchomionego na Cronie 
- Projekt wykorzystuje konteneryzacje docker wraz composerem do uruchomienia środowisk tj: aplikacji django na pythonie 3.8, bazy danych postgresql, aplikacji adminer, cron dla daemona oraz serwer upstream nginx
- Model usera został przebudowany w celu umozliwienia logowania za pomocą email
- Daty utworzenia i aktualizacji sa automatyczne dodawane za pomoca signals przy zapisie
- W projekcie wykorzystano bibliteke wait-for-it w celu kolejkowania uruchamianych kontenerów
- Folder ./initial miescie pliki inicjujace w tym ustawienia crona,nginxa,aplikacji django
- do wysylki powiadomien mailowych wykorzystano konto mailowe no-reply@mign.pl 

## 🚀 Uruchomienie <a name = "getting_started"></a>

Wykonaj klona jesli masz juz zainstalowanego dockera:
```
git clone https://github.com/coconutcake/emenu3.git
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

jesli uzywasz Windowsa, bedziesz musial użyć winpty:

```
winpty docker exec -it emenu sh -c "python3 app/manage.py createsuperuser"
```


Aby sworzyc token dla utworzonego usera - USER to login (email)

```
docker exec -it emenu sh -c "python3 app/manage.py drf_create_token USER" 
```

Możliwe jest równiez utworzenie tokena przez wbudowany CMS

Adresy na lokalnej maszynie:
- Django -> [http://127.0.0.1:8833](http://127.0.0.1:8833) - Wymagana akceptacja samopodpisanego certyfikatu SSL
- DjangoSSL -> [https://127.0.0.1:4433](https://127.0.0.1:4433)
- Adminer -> [http://127.0.0.1:8080](http://127.0.0.1:8080)

## 🚀 Api endpoints <a name = "api"></a>

### Ważne:
- W poniższych przykladach nalezy zamienic ADRES i TOKEN.
- Dla serwera lokalnego ADRES moze być adresem petli zwrotnej - 127.0.0.1
- pole <(pk)> w adreach to pk obiektu do ktorego sie odwołujemy

---
### DISH


###### pola:
```
{
    "name": "", (string)
    "description": "", (string)
    "price": "", (float, examle: „3.50”)
    "etc": "", (duration example: „00:00:30”)
    "created": null,
    "updated": null,
    "is_vege": (bool)
}
```


##### CREATE: https://ADRES:4433/api/menu/dish/create/

###### Przykład:
```
curl -X POST -k https://ADRES:4433/api/menu/dish/create/ -H 'Authorization: Token TOKEN' -d '{"name":"ogorkowa","description":"zupa","price":"23.0","etc":"00:00:30","is_vege":"True"}' -H 'Accept: application/json' -H 'Content-Type: application/json'
```
##### DETAIL: https://ADRES:4433/api/menu/dish/create/

###### Przykład:
```
curl -X GET -k https:/ADRES:4433/api/menu/dish/detail/<(pk)>/ -H 'Authorization: Token TOKEN' -H 'Accept: application/json' -H 'Content-Type: application/json'
```

##### PUT: https://ADRES:4433/api/menu/dish/detail/<(pk)>/

###### Przykład:
```
curl -X PUT -k https://ADRES:4433/api/menu/dish/detail/<(pk)>/ -H 'Authorization: Token TOKEN' -d '{"name":"pomidorowa","description":"zupa","price":"25.0","etc":"00:00:45","is_vege":"True"}' -H 'Accept: application/json' -H 'Content-Type: application/json'
```

##### DELETE:  https://ADRES:4433/api/menu/dish/delete/<(pk)>/

###### Przykład:
```
curl -X DELETE -k https://ADRES:4433/api/menu/menu/delete/<(pk)>/  -H 'Authorization: Token TOKEN' -H 'Accept: application/json' -H 'Content-Type: application/json'
```

---

### MENU


###### pola:
```
{
    "name": "", (string)
    "dish": [], (lista pk modelu dish, example: [1,2])
}
```

##### CREATE: https://ADRES:4433/api/menu/dish/create/

###### Przykład:
```
curl -X POST -k https://ADRES:4433/api/menu/menu/create/ -H 'Authorization: Token TOKEN' -d '{"name":"menu1","dish":[1,2]}' -H 'Accept: application/json' -H 'Content-Type: application/json'
```

##### DETAIL: https://ADRES:4433/api/menu/menu/detail/<(pk)>/
```
curl -X GET -k https://ADRES:4433/api/menu/menu/detail/<(pk)>/ -H 'Authorization: Token TOKEN' -H 'Accept: application/json' -H 'Content-Type: application/json'
```
##### PUT: https://ADRES:4433/api/menu/dish/detail/<(pk)>/

###### Przykład:
```
curl -X POST -k https://ADRES:4433/api/menu/menu/create/ -H 'Authorization: Token TOKEN' -d '{"name":"menu2","dish":[2,3]}' -H 'Accept: application/json' -H 'Content-Type: application/json'
```

##### DELETE: https://ADRES:4433/api/menu/menu/delete/<(pk)>/
```
curl -X DELETE -k https://ADRES:4433/api/menu/menu/delete/<(pk)>/  -H 'Authorization: Token TOKEN' -H 'Accept: application/json' -H 'Content-Type: application/json'
```

