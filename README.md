# Covid-Brazil-Scraping
This code scrapes daily data from the Brazilian Civil Registry Transparency Portal.

<img src="images/sample-plot-ptrc.png" title="Github Logo">



## Brazilian Transparency Portal of Civil Registry

 The [Brazilian Transparency Portal of Civil Registry](https://transparencia.registrocivil.org.br/especial-covid) offers data on deaths registered due to COVID-19 (confirmed or suspected) and respiratory diseases, such as severe acute respiratory syndrome (SARS), pneumonia, and respiratory failure. The civil registry data website is based on death certificates sent by the registry offices countrywide for deaths that take place in hospitals, residences, public roads, etc [1].



## Instructions

In order to setup the execution, the following set of instructions are required:

1. Fill the required browser headers in the `headers.txt` file. This information can be acquired through your browser's web inspector.
2. Choose the brazilian cities you want to scrape data from by filling the dictionary in the `CitySelect.txt` file.
3. Run the `scrape-respiratory-daily.py` file.
4. The data will be saved in the `data` repository in a directory named after the date the web scraping was executed. The file will be in csv format.



The following steps are optional:

1. By default, the script will scrape data since Januray 1st 2020 until the present date, this can be changed by editing the `start-date` and `end-date` variables on the `scrape-respiratory-daily.py` file.



## License

MIT License



## References
1. Veiga e Silva, L., de Andrade Abi Harb, M. D. P., Teixeira Barbosa dos Santos, A. M., de Mattos Teixeira, C. A., Macedo Gomes, V. H., Silva Cardoso, E. H., Silva da Silva, M., Lankalapalli Vijaykumar, N., Venâncio Carvalho, S., Ponce de Leon Ferreira de Carvalho, A., & Lisboa Frances, C. R. (2020). An analysis of COVID-19 mortality underreporting based on data available from official Brazilian government internet portals (Preprint). Journal of Medical Internet Research, 22, 1–14. https://doi.org/10.2196/21413.
2. Especial COVID-19. Portal da Transparência do Registro Civil. 2020. URL: https://transparencia.registrocivil.org.br/especial-covid. 





