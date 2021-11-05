import h5py





data_file = h5py.read('/home/scott/Downloads/SC3_v3_NextGem_DI_Neurons_5K_SC3_v3_NextGem_DI_Neurons_5K_count_sample_molecule_info.h5' ,'r')
barcode_idx_set = set(f['/']['barcode_idx'])
barcode_idx = f['/']['barcode_idx']
gene_idx = f['/']['feature_idx']
counts = f['/']['count']
print(len(barcode_set),"barcodes found")