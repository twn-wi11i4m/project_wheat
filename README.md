# Project Wheat

python3.8

## constant in ```constant.py``` 

- farming area size $A$ [```FAAMING_AREA```]
    - unit: acre

- Cost $C$ [```COST```](including risk management)
    - all in  unit: $/acre
    - The Operational cost $\text{OC}$ [```OPERATIONAL_COST```]
        - Seed & Treatment [```SEED_TREATMENT```]
        - Fertilizer [```FERTILIZER```]
        - Pesticide [```PESTICIDE```]
        - Fuel [```FUEL```]
        - Machinery Operation \& Lease [```MACHINERY_OPERATION_LEASE```]
        - Labour Hired [```LABOUR_HIRED```]
        - Drying \& Other Costs [```DRYING_OTHER_COSTS```]
        - Insurance premium [```INSURANCE_PREMIUM```]
        - Land Taxes [```LAND_TAXES```]
        - Storage Costs [```STORAGE_COSTS```]
        - Interest on Operation [```INTEREST_ON_OPERATION```]
    - The Fixed cost $\text{FC}$ [```FIXED_COST```]
        - Land Costs [```LAND_COSTS```]
        - Machinery Costs [```MACHINERY_COSTS```]
- The total cost $TC$ [```TOTAL_COST```]


## Insurance payoff
- The payoff of insurance: $\max{\{Y_\text{guarantee} - Y_T, 0\}}\times \text{spring insured price}$
- The total payoff of insurance $\text{R}_\text{insurance} = \max{\{Y_\text{guarantee} - Y_T, 0\}}\times \text{spring insured price}\times A$
- The detail of insurance please refer to ```insurance.py```


## Some unknown variable:
- The Final Yield $Y_T$ [```Y_T```]
    - unit: Bushel/acre
- The Spot price $S_T$ [```S_T```]
    - unit: Bushel/acre
- The future price (depends on expired date $d$) $P_{t, d}$
- The Revenue $\text{R} = Y_T\times S_T \times A+ \text{R}_\text{insurance} +\text{R}_\text{Finanical}$
- The net-profit $\text{NP} = R -TC$

## formulation
We assume the the wealth at time $t$ is $W_t$ and define $W_T$ is the final wealth at the end of period.
$$W_T = W_0+\text{NP}=W_0+\left(Y_T\times S_T \times A\right)+\text{R}_\text{insurance} + \text{R}_\text{Financial}-TC$$

## Project Approach
### Approach 1
The farmer only sell the crop at spot price, the final wealth will be
$$W_T = W_0 + \left(Y_T\times A\times S_T\right) - {TC}_\text{excluding insurance}$$

$$\Rightarrow\Delta W:=W_T-W_0=\left(Y_T\times A\times S_T\right) - {TC}_\text{exculding insurance}$$


### Approach 2
The farmer only sell the crop at spot price and purchase the corp insurance, and the final wealth will be
$$
W_T = W_0+(Y_T\times A\times S_T)+\text{R}_\text{insurance}-TC
$$

$$
\Rightarrow \Delta W=(Y_T\times A\times S_T)+\text{R}_\text{insurance}-TC
$$

### Approach 3
The farmer only sell the crop at spot price, purchase the corp insurance, and hedge with the corp future. 
$$
W_T = W_0+\left(Y_T\times A\times S_T\right)+\text{R}_\text{insurance} + \text{R}_\text{Financial}-TC
$$

$$
\Rightarrow \Delta W =\left(Y_T\times A\times S_T\right)+\text{R}_\text{insurance} + \text{R}_\text{Financial}-TC
$$
* Here, we assume the farmer allocate all the wealth in financial. The farmer will trade ```WC2 COMDTY``` only.


### Approach 3.1
The farmer only sell the crop at spot price, purchase the corp insurance, and hedge with the corp future with smart allocation
$$
W_T = W_0+\left(Y_T\times A\times S_T\right)+\text{R}_\text{insurance} + \text{R}_\text{Financial}'-TC
$$

$$
\Rightarrow \Delta W =\left(Y_T\times A\times S_T\right)+\text{R}_\text{insurance} + \text{R}_\text{Financial}'-TC
$$
* Here, we assume the farmer allocate some of the wealth in financial.

**Data source:**

spot price of wheat: [https://economicdashboard.alberta.ca/GrainPrices](https://economicdashboard.alberta.ca/GrainPrices)

- the spot price



