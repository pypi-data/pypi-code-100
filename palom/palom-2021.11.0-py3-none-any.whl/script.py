import pathlib
import logging
import matplotlib.pyplot as plt
from palom import reader
from palom import align
from palom import write_pyramid

logging.basicConfig(
    filename='abc.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# # create logger
# logger = logging.getLogger('simple_example')
# logger.setLevel(logging.DEBUG)

# # create console handler and set level to debug
# ch = logging.StreamHandler()
# ch.setLevel(logging.DEBUG)

# # create formatter
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# # add formatter to ch
# ch.setFormatter(formatter)

# # add ch to logger
# logger.addHandler(ch)



settings = {
    'svs_dir': r'Y:\sorger\data\OHSU\2019NOV-TNP_PILOT\TNP SARDANA images (mIHC)\75684\processed\raw',
    'ref_slide_pattern': '*HEM*',
    'out_dir': r'Y:\sorger\data\OHSU\2019NOV-TNP_PILOT\TNP SARDANA images (mIHC)\75684\processed\registration'
}

svs_paths = sorted(pathlib.Path(settings['svs_dir']).glob('*.svs'))
svs_paths.sort(key=lambda x: x.name.split('_')[4])

ref_slide = None
for svs in svs_paths:
    if svs.match(settings['ref_slide_pattern']):
        logging.info('Reference file found {}'.format(svs.name))
        ref_slide = svs
        svs_paths.remove(svs)
        break

ref_reader = reader.SvsReader(ref_slide)

aligners = []

for idx, p in enumerate(svs_paths[:2]):
    logging.info(f"Processing {p.name}")
    moving_reader = reader.SvsReader(p)

    aligner = align.ReaderAligner(ref_reader, moving_reader, pyramid_level=1)
    logging.info(f"Coarse aligning to {aligner.ref_reader.path.name}")
    aligner.coarse_register_affine()
    plt.suptitle(f"L: {aligner.ref_reader.path.name}\nR: {p.name}")
    plt.savefig(f"{idx+1:02d}-{p.name}.png")
    logging.info(f"Computing block-wise shifts")
    aligner.compute_shifts()
    aligner.constrain_shifts()

    aligners.append(aligner)



mosaics = [aligners[0].get_ref_mosaic(mode='hematoxylin')]
mosaics += [   
    a.get_aligned_mosaic(mode='intensity')
    for a in aligners
]


write_pyramid.write_pyramid(
    mosaics, r'D:\yc296\mosaic-full.ome.tif', pixel_size=0.5
)


channel_names = ', '.join(
    [
        '-'.join(p.name.split('_')[-2:][::-1]).replace('.svs', '') 
        for p in ([ref_slide] + svs_paths)
    ]
)