# Climate Policy Breaks

This repository lays the foundation for the method proposed by Stechemesser et al. (2024), Koch et al. (2022), and Pretis (2022).

The method is titled "Detecting unknown treatment assignemnt and timing as breaks in panel models.". 

The main purpose is to use difference-in-difference models and machine learning approaches to detect breaks in time-series. 

## Methodology

...

## Todo

### Data 

- [x] download the test data for the method development
- [ ] compile HEUS (Japan) monthly data for experiments (using behavioural change as structural breaks) 

### Methods

- [ ] use `getspanel` in R to implement structural break identification
- [ ] or connect R with Python to use `getspanel` 

### Codes
- 
- [ ] init the repo with R codes (if available in *Science's* publication)
- [ ] detect structural breaks in households emission based on HEUS datasets

## References

1. Stechemesser, A., Koch, N., Mark, E., Dilger, E., Klösel, P., Menicacci, L., ... & Wenzel, A. (2024). Climate policies that achieved major emission reductions: Global evidence from two decades. Science, 385(6711), 884-892.
2. Koch, N., Naumann, L., Pretis, F., Ritter, N., & Schwarz, M. (2022). Attributing agnostically detected large reductions in road CO2 emissions to policy mixes. Nature Energy, 7(9), 844-853.
3. Pretis, F. (2022). Does a carbon tax reduce CO2 emissions? Evidence from British Columbia. Environmental and Resource Economics, 83(1), 115-144.
