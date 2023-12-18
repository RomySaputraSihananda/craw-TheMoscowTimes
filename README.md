[![Twitter: romy](https://img.shields.io/twitter/follow/RomySihananda)](https://twitter.com/RomySihananda)

# craw-TheMoscowTimes

![](https://raw.githubusercontent.com/RomySaputraSihananda/RomySaputraSihananda/main/images/GBnPRZmbgAABJA8.jpeg)

Program ini dirancang untuk melakukan web scraping pada situs berita TheMoscowTimes dengan memanfaatkan </br>parameter seperti kategori (category), tanggal, dan halaman (page). </br>Tujuan utama dari program ini adalah untuk mengumpulkan informasi berita dari TheMoscowTimes sesuai </br>dengan kriteria yang diinputkan oleh pengguna.

## Requirements

- **Python >= 3.11.4**
- **pyquery >= 2.0.0**
- **pytz >= 2023.3.post1**
- **Requests >= 2.31.0**

## Installation

```sh
# Clonig Repository
git clone https://github.com/romysaputrasihananda/craw-TheMoscowTimes

# Change Directory
cd craw-TheMoscowTimes

# Install Requirement
pip install -r requirements.txt
```

## Example Usages

### By Category

```bash
python main.py --category=news --page=1 --output=data
```

### Searching

```bash
python main.py --keyword=war --page=1 --category=news --from_date=2023-01-01 --to_date=2023-12-18 --output=data
```

### Flags

| Flag        | Alias |             Description             | Example                | Default |
| :---------- | :---: | :---------------------------------: | :--------------------- | :-----: |
| --category  |  -s   | [category](Category.md) of the site | --category=news        |  news   |
| --page      |  -p   |       number page of the site       | --page=2               |    1    |
| --keyword   |  -d   |    keyword to search to the site    | --keyword=war          |  None   |
| --from_date |  -d   |       start date of the site        | --from_date=2023-01-01 |  None   |
| --to_date   |  -d   |        end date of the site         | --to_date=2023-12-18   |  None   |
| --output    |  -o   |        json file output path        | --output=data          |  data   |

## Sample Output

```json
{
  "date_now": "2023-12-18T22:52:18",
  "keyword": "war",
  "category": "news",
  "page": 1,
  "range_datetime": {
    "from": "2023-01-01",
    "to": "2023-12-18"
  },
  "data": [
    {
      "id": "20f1f3f07aeab7abee1f4d3c913a96bd",
      "title": "UN Says Both Russia and Ukraine Summarily Executing Prisoners of War",
      "lang": "en",
      "create_at": "2023-03-24T17:40:27+03:00",
      "url": "https://www.themoscowtimes.com/2023/03/24/un-says-both-russia-and-ukraine-summarily-executing-prisoners-of-war-a80611",
      "url_thumbnail": "https://static.themoscowtimes.com/image/article_1360/0f/aan-s6e5-matilda-at-work.jpg",
      "autor": "AFP",
      "desc": "The United Nations on Friday said it was \"deeply concerned\" by what it described as the summary exec...",
      "article": "The United Nations on Friday said it was \"deeply concerned\" by what it described as the summary executions of prisoners of war being carried out by both Russian and Ukrainian forces on the battlefield in Ukraine.The head of the UN Human Rights Monitoring Mission in Ukraine, Matilda Bogner, said her organization had documented killings, often on the battlefield, by both sides in recent months.\"We are deeply concerned about summary execution of up to 25 Russian prisoners of war and persons hors de combat by the Ukrainian armed forces, which we have documented,\" Bogner said at a press conference in Kyiv.\"This was often perpetrated immediately upon capture on the battlefield. While we are aware of ongoing investigations by Ukraine authorities into five cases involving 22 victims, we are not aware of any prosecution of the perpetrators,\" she added.Bogner also related the UN's \"deep\" concern over \"the summary execution of 15 Ukrainian prisoners of war shortly after being captured by Russian armed forces.\"She said the Wagner mercenary group, which claims to be leading Russia's assault on the city of Bakhmut, the longest and bloodiest battle of the war, was responsible for some 11 of those killings.Ukraine and Russia have both accused each other of mistreating prisoners of war since Russian President Vladimir Putin ordered his forces into Ukraine a year ago."
    }
    // more data
  ]
}
```

## License

This project is licensed under the [MIT License](LICENSE).
