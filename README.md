Tekemäni harjoitustyö on eräänlainen keskustelufoorumi. Kuka tahansa pystyy selaamaan ja lukemaan keskusteluja, mutta 
rekisteröityneet käyttäjät pystyvät luomaan uusia keskusteluita ja ottamaan osaa muiden luomiin keskusteluihin. Jokaisesta 
keskusteluviestistä voi tykätä. Tässä minun tekemässäni keskustelufoorumissa on perimmäinen idea, että keskustelun luoja kysyy jotain, johon hän haluaa vastauksen. Esimerkiksi jos joku kysyisi "onko Marsissa elämää", muut rekisteröityneet käyttäjät voivat vastata tähän kysymykseen. Kuten jo kerrottu, näistä vastauksista (eli viesteistä) pystyy tykkäämään. Näin kysyjä voi päätellä, mikä vastauksista voisi olla paras. Jokainen rekisteröitynyt käyttäjä voi tykätä vain kerran tietystä viestistä. 

Rekisteröityneitä käyttäjiä on kolmea eri laatua: tavallinen, moderator ja admin. Tavallinen käyttäjä pystyy tekemään edellä mainitsemani asiat, eli luomaan kysymyksiä, vastaamaan muiden kysymyksiin ja tykkäämään kysymyksistä. Moderator pystyy poistamaan muiden viestejä. Admin-käyttäjällä on kaikista eniten valtuuksia. Admin pystyy tekemään kaikki edellä mainitsemani toimenpiteet. Lisäksi admin pystyy tekemään tavallisista käyttäjistä moderator-käyttäjiä ja poistamaan kenen tahansa käyttäjätilin. 

## Installation

We assume that you have installed Docker on your desktop. You can install this software by using Docker hub or manually by command: docker build . -t TietokantaHarkkatyo. After that you can run it by typing: docker run -it -p 3000:5000 TietokantaHarkkatyo. Navigate to address: 127.0.0.1:3000

The another way is to pull image from docker hub: docker pull masiro918/devopswith-docker:latest

ATTETION! The Docker container does not include database! You have to configure environment variables and database connetions yourself. The program still "runs", but not correctly because of database.


