# Fishing for Smishing: Understanding SMS Phishing Infrastructure and Strategies by Mining Public User Reports

## Artifact Availability
As promised in our artifact availability (`Appendix B`), we provide our labeled smishing dataset (`final_dataset_output.csv`) along with the R code to produce the Fig. 2 and Fig. 3. 

## Directory Structure

```bash
├── code
│   ├── analysis.R
│   ├── count_lang_per_named_entity.py
│   ├── count_lang_per_scam.py
│   ├── count_lang.py
│   ├── count_lures_per_scam.py
│   ├── count_lures.py
│   ├── lang_per_named_entity.txt
│   ├── language_counts.txt
│   ├── lure_principle_counts.txt
│   ├── lure_scam_counts.txt
│   ├── named_entity_counts.txt
│   └── scam_type_lang_counts.txt
├── dataset
│   ├── final_dataset_output.csv
│   └── time_day.csv
├── LICENSE.txt
├── plots
│   ├── Figure 2.pdf
│   └── Figure 3.pdf
└── README.md
```

<a name="bibtex"></a>
## Citation

If you find our work or any of our materials useful, please cite our paper:

```
@inproceedings{10.1145/3730567.3764431,
author = {Agarwal, Sharad and Papasavva, Antonis and Suarez-Tangil, Guillermo and Vasek, Marie},
title = {Fishing for Smishing: Understanding SMS Phishing Infrastructure and Strategies by Mining Public User Reports},
year = {2025},
isbn = {9798400718601},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
url = {https://doi.org/10.1145/3730567.3764431},
doi = {10.1145/3730567.3764431},
booktitle = {Proceedings of the 2025 ACM on Internet Measurement Conference},
location = {Madison, WI, USA},
series = {IMC '25}
}
```

Shield: [![CC BY 4.0][cc-by-shield]][cc-by]

This work is licensed under a
[Creative Commons Attribution 4.0 International License][cc-by].

[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg