# Generated by Django 3.1.5 on 2021-02-12 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bocken', '0010_auto_20210212_1606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journalentry',
            name='group',
            field=models.CharField(choices=[('baska', 'Baskå'), ('td', 'TD'), ('proppen', 'Proppen'), ('kv', 'KV'), ('rebusrallyt', 'Rallykå'), ('balen', 'Balkå'), ('cafegruppen', 'Cafegruppen'), ('forska', 'Forskå'), ('eventgruppen', 'Eventgruppen'), ('exka', 'Examenkå'), ('marknadsforingsgruppen', 'Marknadsföringsgruppen'), ('mer', 'MER'), ('utnarm', 'Utnarm'), ('polhacks', 'Polhackskå'), ('dka', 'Dkå'), ('karhusgruppen', 'Kårhusgruppen'), ('techna', 'Techna'), ('best', 'BEST'), ('teknatspex', 'Teknat Spex'), ('genius', 'Genius'), ('iaeste', 'IAESTE'), ('ibk', 'IBK'), ('igem', 'IGEM'), ('siv', 'SIV'), ('mfk', 'MFK'), ('gb', 'GB'), ('tmp', 'TMP'), ('valberedningen', 'Valberedningen'), ('board', 'Styrelsen'), ('utbex', 'Utb-ex'), ('utbn', 'Utb-n'), ('utbt', 'Utb-t'), ('soc', 'Soc'), ('int', 'Int'), ('na', 'NA'), ('plutnarm', 'PL Utnarm'), ('ordf', 'Ordförande'), ('viceordf', 'Vice Ordförande'), ('forvaltning', 'Förvaltning'), ('historiograf', 'Historiograf'), ('pelarmarskalk', 'Pelarmarskalk'), ('internrevisorer', 'Internrevisorer'), ('bas', 'BAS'), ('dv', 'DV'), ('e', 'E'), ('es', 'ES'), ('f', 'F'), ('h', 'H'), ('i', 'I'), ('it', 'IT'), ('k', 'K'), ('nvb', 'NVB (BÄR)'), ('nvf', 'NVF (FysKam)'), ('nvg', 'NVG (GRUS)'), ('nvk', 'NVK (IUPAK)'), ('nvl', 'NVL (LärNat)'), ('nvm', 'NVM (Moebius)'), ('q', 'Q'), ('sts', 'STS'), ('w', 'W'), ('x', 'X')], max_length=120),
        ),
    ]
