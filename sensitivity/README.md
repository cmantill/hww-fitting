# Sensitivity study

Using softdrop mass to fit signal

## Inputs

## Create datacards

```
python autodatacards.py  --idir /eos/user/c/cmantill/boostedhiggs/May7/merged/  -o datacards/May7_preSel -y 2017 -c ele
```

## Verify templates by plotting

```
python plot_templates.py -f datacards/May7_preSel_ele/hwwcard_2017_shapehists.root --year 2017 --tag May7_preSel_ele
```

## Get expected sensitivity for one datacard

```
combine -M AsymptoticLimits --run expected -d datacard.txt -t -1  -v 1 --expectSignal 1
combine -M Significance -d datacard.txt -t -1 --expectSignal 1
```

## To run full study:

```
python run_study.py --idir /eos/user/c/cmantill/boostedhiggs/May7/merged/  -o datacards/May7_preSel
```

