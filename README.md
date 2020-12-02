# Shipman

Console based shipment tracking tool. Written in python.

Relies upon the italian localization of GLS and Amazon websites.
Amazon tracking recognition is unreliable and could not work properly. 

Currently supports:
- *GLS*
- *Amazon* (partial, unreliable)
- *DHL*
- *TNT*
- *BRT*
- *Poste Italiane*
  
  (Note though that Poste Italiane server randomly requests a recaptcha verification so it could not work reliably)

## Usage

First install with pip

```shell
pip install git+https://github.com/paolo-projects/shipman.git#egg=shipman
```

Then run

```shell
shipman [-h] [-p {pretty,json,tab}] -s {gls,amazon,dhl,tnt,brt,posteit} tracking_number
```

- The optional argument `-p pretty|json|tab` modifies the way the output is formatted. 
Defaults to pretty if not specified
- The argument `-s {gls,amazon,dhl,tnt,brt,posteit}` selects which service the tracking number belongs to