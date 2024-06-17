**Notebook Summary**
\
The CMAPSS datasets have simulated data from various different engines, which mimic the behavior from normal operation up until failure. There are 3 operational settings (OS1-3), 21 sensors and the time column (cycles). The unit column is simply the unit (engine) number. This notebook focuses on pre-processing, analyzing, modelling and predicting on the first CMAPSS dataset (FD001). The ultimate goal is to be able to predict how many cycles each engine will run before it experiences failure, which is known as Remaining Useful Life (RUL).

**Dataset: FD001**
* Train set engines: 100
* Test set engines: 100
* Operating condition: sea-level
* Fault mode: High Pressure Compressor (HPC) degradation
* Missing data: None

**Sensor Feature Descriptions**

| Name               | Description                    | Units   |
| ------------------ | ------------------------------ | ------- |
| fan_in_temp        | Total temp at fan inlet        | R       |
| lpc_out_temp       | Total temp at LPC outlet       | R       |
| hpc_out_temp       | Total temp at HPC outlet       | R       |
| lpt_out_temp       | Total temp at LPT outlet       | R       |
| fan_in_press       | Pressure at fan inlet          | psia    |
| bypass_press       | Total pressure in bypass duct  | psia    |
| hpc_out_press      | Total pressure at HPC outlet   | psia    |
| fan_speed          | Physical fan speed             | rpm     |
| core_speed         | Physical core speed            | rpm     |
| epr                | Engine pressure ratio (P50/P2) | N/A     |
| hpc_stat_press     | Static pressure at HPC outlet  | psia    |
| flow_press_ratio   | Ratio of fuel flow to Ps30     | pps/psi |
| corr_fan_speed     | Corrected fan speed            | rpm     |
| corr_core_speed    | Corrected core speed           | rpm     |
| bypass_ratio       | Bypass ratio                   | N/A     |
| burner_fuel_ratio  | Burner fuel-air ratio          | N/A     |
| bleed_enthalpy     | Bleed enthalpy                 | N/A     |
| dmd_fan_speed      | Demanded fan speed             | rpm     |
| dmd_corr_fan_speed | Demanded corrected fan speed   | rpm     |
| hpt_bleed          | HPT coolant bleed              | lbm/s   |
| lpt_bleed          | LPT coolant bleed              | lbm/s   |
