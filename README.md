# I2C Frame Decoder

Ce projet Python permet de **décoder dynamiquement** une ou plusieurs trames I2C binaires à partir d'une chaîne de caractères. Il peut détecter plusieurs trames dans une même ligne grâce aux indices des caractères `S` (start condition) et retourne une représentation lisible.

---

## Fonctionnalités

- Détection automatique des débuts de trames (`S`)
- Décodage :
  - Adresse esclave + bit R/W
  - Bits d'acquittement (`A` ou `N`)
  - Données codées sur 8 bits suivies d’un acquittement
- Gestion des erreurs
- Supporte plusieurs trames concaténées
- Auto-correction si la ligne ne commence pas par `S`

---

##  Exemple de trame décodée

```bash
    [S] 0x41 W A 0x10 A 0x10 A[S] 0x41 R A 0x01 A 0x02 A 0xA7 A 0x07 A 0x31 A 0x0A A 0x00 A 0x00 A 0x00 A 0x00 A 0x0A A 0x00 A 0x00 A 0x00 A 0x00 A 0x0A A 0x00 A 0x00 A 0x00 A 0x00 A 0x1A A 0x00 A 0x00 A 0x00 A 0x00 A[S] 0x20 W A 0x00 A 0x00 A 0x00 A 0x00 N 0x41 N
```

### Entrée :
```bash 
    S1000001WA00010000A00010000A1S1000001RA00000001A00000010A10100111A00000111A00110001A00001010A00000000A00000000A00000000A00000000A00001010A00000000A00000000A00000000A00000000A00001010A00000000A00000000A00000000A00000000A00011010A00000000A00000000A00000000A00000000A00001S0100000WA00000000A00000000A00000000A00000000N01000001N1101s
```