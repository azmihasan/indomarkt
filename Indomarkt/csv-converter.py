import pandas as ps

data_path = "/Users/azmihasan/Library/CloudStorage/OneDrive-HochschulefürTechnikundWirtschaftBerlin/Indomarkt/Marken PrestaShop/manufacturer_2022-07-11_131835.csv"
data = ps.read_csv(data_path, sep=";")


save_path = "/Users/azmihasan/Library/CloudStorage/OneDrive-HochschulefürTechnikundWirtschaftBerlin/Indomarkt/Marken PrestaShop/manufacturer_2022-07-11_131835.xlsx"
data.to_excel(save_path)
