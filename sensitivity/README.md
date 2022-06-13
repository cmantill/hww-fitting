# Sensitivity study

Using softdrop mass to fit signal.

## Inputs

Use merged ROOT TTrees (`Events`) for inputs.
e.g.
```
IDIR = "/eos/user/c/cmantill/boostedhiggs/May7/merged/"
```

## Create datacards
Use `autodatacards.py` to create datacards and rootfiles with histograms of the softdrop mass.
This uses `histmaker` and `refs` to make a selection and assume a tagging efficiency in different processes.

Arguments:
```
- IDIR: Input directory with merged files
- ODIR: Output directory to store datacards (usually datacards/)
- TAG: Tag to save these datacards
- YEAR: 2016,2016APV,2017,2018?
- CHANNEL: (ele,mu or had)
- SHAPEFILE: Name of shapefile, default: shapehists.root
```

e.g.
```
python autodatacards.py  --idir /eos/user/c/cmantill/boostedhiggs/May7/merged/ -o datacards/ --tag May7_preSel -y 2017 -c ele
```

## Verify templates by plotting
One can plot the templates saved in `shapehists.root` for debugging using `plot_templates.py`
e.g.
```
python plot_templates.py -f datacards/May7_preSel_ele/hwwcard_2017_shapehists.root --year 2017 --tag May7_preSel_ele
```

## Get expected sensitivity for one datacard
Once the datacard is built, one can go inside the directory and run Combine commands:
e.g. to get the limits
```
combine -M AsymptoticLimits --run expected -d datacard.txt -t -1  -v 1 --expectSignal 1
```
e.g. to get the significance
```
combine -M Significance -d datacard.txt -t -1 --expectSignal 1
```

## To run full study:
To scan over different channels and years, use `run_study.py`.
```
python run_study.py --idir /eos/user/c/cmantill/boostedhiggs/May7/merged/  -o datacards/ --tag May7_preSel
```

