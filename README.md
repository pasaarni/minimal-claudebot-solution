# Chatbot

Pieni chatbot-sovellus, joka vastaa kysymyksiin omien projektikansioiden datan perusteella. Botti käyttää Claude-kielimallia Anthropicin API:n kautta.

## Mitä sovellus tekee

- Käyttäjä keskustelee botin kanssa selaimessa toimivassa chat-käyttöliittymässä.
- Yksi projektikansio on **aktiivinen**: sen koko sisältö ladataan botin kontekstiin, joten botti tuntee sen kokonaisuudessaan.
- Muut projektikansiot ovat botin tiedossa nimeltä ja lyhyeltä kuvaukseltaan. Kun käyttäjä viittaa johonkin niistä, botti hakee projektin sisällön työkalukutsulla ja vastaa sen perusteella.
- Jos vastausta ei löydy datasta, botin ohjeistus on kertoa se eikä keksiä vastausta.

## Miten tämä toteutettiin

Sovellus koostuu kolmesta pienestä osasta:

1. **Käyttöliittymä** on yksinkertainen HTML-sivu, joka lähettää keskusteluhistorian backendille ja näyttää vastauksen.
2. **Backend** on serverless-funktio. Se rakentaa järjestelmäkehotteen (botin rooli, säännöt, projektilista ja aktiivisen projektin sisältö), kutsuu Claude API:a ja hoitaa mahdolliset työkalukutsut.
3. **Datan lukija** käy läpi `projects/`-kansion, lukee tuetut tekstitiedostot ja palauttaa projektin sisällön yhtenä tekstinä. Se myös tuottaa projektin lyhyen kuvauksen README-tiedoston alusta.

Toimintaperiaate on kevyt agenttimalli (tool use): botti päättää itse, tarvitseeko se toisen projektin dataa, ja pyytää sen `get_project`-työkalulla. Backend suorittaa haun ja palauttaa tuloksen botille, joka muodostaa lopullisen vastauksen.

### Teknologiat

- Node.js (JavaScript, ES-moduulit)
- Anthropic SDK (`@anthropic-ai/sdk`)
- Vercel (hosting ja serverless-funktiot)
- Vanilla HTML, CSS ja JavaScript käyttöliittymässä

## Projektin rakenne

```
chatbot/
├── projects/      # tietopohjat, yksi kansio per projekti
├── lib/           # datan lukeminen
├── api/           # backend (chat-endpoint)
├── public/        # chat-käyttöliittymä
├── vercel.json    # julkaisun asetukset
└── .env.example   # esimerkki ympäristömuuttujista
```

## Käyttöönotto

1. Kloonaa repo ja asenna riippuvuudet komennolla `npm install`.
2. Kopioi `.env.example` tiedostoksi `.env` ja täytä sen arvot (API-avain ja aktiivisen projektin nimi).
3. Lisää omat projektikansiosi `projects/`-kansioon. Suositus: laita kuhunkin kansioon `README.md`, jonka alku kuvaa projektin lyhyesti.
4. Käynnistä paikallisesti komennolla `vercel dev`.

Julkaisu: tuo repo Verceliin ja lisää samat ympäristömuuttujat Vercelin asetuksiin.

## Tietoturva

- API-avainta ei koskaan tallenneta repoon eikä selainkoodiin. Se on vain palvelimen ympäristömuuttujassa.
- `.env` on `.gitignore`-tiedostossa.
- Backend validoi syötteen (viestien määrä ja pituus) ja sallii työkalulle vain olemassa olevat projektinimet, joten polkuhyökkäykset estetään.

## Jatkokehitys

- Aktiivisen projektin valinta käyttöliittymästä
- Vastausten suoratoisto (streaming)
- Pyyntömäärän rajoitus
- Hakutoiminto (avainsana tai embeddingit) suurempia tietomääriä varten

## Lisenssi

Apache License
