from csv import reader
from math import log2,ceil

def open_csv(filename):
    csv = reader(open(filename))
    return [row for row in csv]

def extract_row_data(rows,limits):
    return rows[limits[0]-1:limits[1]]

def extract_colum_data(rows,first_indx, second_indx):
    return [row[first_indx:second_indx] for row in rows]

def extract_dir_content(rows,dir_range,content_range):
    data = {}
    for row in rows:
        rom_dir = "".join(row[dir_range[0] : dir_range[1] if len(dir_range) == 2 else len(row)])
        rom_content = "".join(row[content_range[0]:content_range[1] if len(content_range) == 2 else len(row)])
        data[rom_dir] = rom_content
    return data

def create_mif_file(rom,width,depth,output_name):
    template = open("mif_template.mif")
    mif = ""
    for line in template:
        mif += line
    mif = mif.replace("{WIDTH}",str(width))
    mif = mif.replace("{DEPTH}",str(depth))
    data_str = ""
    data_format = "\t {rom_dir}  :   {data};\n"
    dir_length = int(log2(depth) + 1)
    for rom_dir,data in rom.items():
        data_str += data_format.format(rom_dir=rom_dir.zfill(dir_length)  ,data=str(data))
    print(len(rom), depth)
    if len(rom) < depth:
        default = "".zfill(width)
        rem_0 = str(bin(len(rom))).replace("0b","").zfill(dir_length)
        rem_1 = str(bin(depth - 1)).replace("0b","").zfill(dir_length)
        if rem_0 == rem_1:
            data_str += data_format.format(rom_dir=rem_0  ,data=default)
        else:
            data_str += "\t[{ini}..{end}]  :   {default};\n".format(ini=rem_0,end=rem_1,default=default)
    mif = mif.replace("{data}",str(data_str))
    output = open(output_name + ".mif","w")
    output.write(mif)

def create_rom_vhd(rom):
    data_format = '\t internal_mem({index}) <= "{liga}"  & {salida};\n'
    data_str = ""
    for rom_dir,data in rom.items():
        data_str += data_format.format(index=int(str(rom_dir),2), liga=data[:3], salida=data[3:len(data)])
    vhd_file = open("vhd_format.txt","w")
    vhd_file.write(data_str)


def main():
    # Modificable data ##############################
    # Rango de columnas donde se encuentran los datos, asi como aparece en el excel
    row_range = (4,11)
    # Rango donde se encuentra la direccion, 
    # Se inicia contando desde 0. y el segundo numero es el primero + el numero de columnas.
    #Si no se pone se entiende que va desde n hasta el fin.
    dir_range = (0,3)
    data_range = (3,)
    width = 9
    depth = 64
    # Archivo de entrada
    filename = "P4.csv"
    # Nombre del archivo salida sin extension
    output_name = "rom_content_2" 
    ###############################################
    rows = open_csv(filename)
    data = extract_row_data(rows,row_range)
    rom = extract_dir_content(data,dir_range,data_range)
    # Se puede calcular el valor depth
    # Utilizando un valor potencia de 2
    depth_calc = 2 ** ceil(log2(len(rom)))
    depth = depth_calc
    # O simplemente con la longitud de nuestos valores
    # depth_calc = len(rom)
    ###################################################
    # Igual se puede calcular el parametro width
    width = len(list(rom.values())[0])
    rom_sorted = sorted(rom.items(),key=lambda x: int(x[0],2))
    rom_sorted = {rom_s[0]: rom_s[1] for rom_s in rom_sorted }
    create_mif_file(rom_sorted,width,depth,output_name)
    #create_rom_vhd(rom_sorted)

if __name__ == "__main__":
    main()


