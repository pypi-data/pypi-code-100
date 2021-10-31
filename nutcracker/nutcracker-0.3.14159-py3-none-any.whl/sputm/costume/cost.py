#!/usr/bin/env python3
import io
import os
import struct
import itertools

import numpy as np
from nutcracker.sputm.room.pproom import get_rooms, read_room_settings

from nutcracker.sputm.tree import open_game_resource

UINT32LE = struct.Struct('<I')
UINT16LE = struct.Struct('<H')
SINT16LE = struct.Struct('<h')


from nutcracker.codex import bpp_cost
from nutcracker.graphics.image import convert_to_pil_image
from nutcracker.utils.funcutils import flatten

from ..preset import sputm



def read_cost_resource_2(cost, room_palette, version):

    with io.BytesIO(cost.data) as stream:
        size = 1
        if version == 6:
            size = UINT32LE.unpack(stream.read(UINT32LE.size))[0]
            header = stream.read(2)
            assert header == b'CO'

        num_anim = stream.read(1)[0]
        total_animations = num_anim + (1 if size > 0 else 0)

        format = stream.read(1)[0]
        palette_size = 32 if format & 1 else 16

        palette = list(itertools.chain.from_iterable([room_palette[3*x:3*x+3] for x in stream.read(palette_size)]))

        anim_cmd_offset = UINT16LE.unpack(stream.read(UINT16LE.size))[0]
        limbs_offsets = [UINT16LE.unpack(stream.read(UINT16LE.size))[0] for _ in range(16)]
        anim_offsets = [UINT16LE.unpack(stream.read(UINT16LE.size))[0] for _ in range(total_animations)]

        parsed_anims = set()
        animations = []
        for anim_off in anim_offsets:
            if anim_off > 0:
                if anim_off not in parsed_anims:
                    assert anim_off == stream.tell(), (anim_off, stream.tell())
                    
                    animation = {
                        'definitions': [],
                        'offset': anim_off
                    }
                    animation['limb_mask'] = UINT16LE.unpack(stream.read(UINT16LE.size))[0]
                    num_limbs = sum(int(x) for x in f"{animation['limb_mask']:016b}")

                    for i in range(num_limbs):
                        definition = {
                            'start': UINT16LE.unpack(stream.read(UINT16LE.size))[0]
                        }
                        if definition['start'] != 0xFFFF:
                            next_byte = stream.read(1)[0]
                            definition['no_loop'] = next_byte & 0x80
                            definition['end_offset'] = next_byte & 0x7F
                        animation['definitions'].append(definition)
                    animations.append(animation)
                    parsed_anims |= {anim_off}


        print(animations)
        yield 0, convert_to_pil_image(np.zeros((1, 1), dtype=np.uint8))
    #         //Segundo o site do SCUMMC, achar o tamanho do CMDArray e outro itens é somente olhando os indices, pois uma coisa começa onde a
    #         //outra termina. Segue o texto original abaixo:
    #         //
    #         //It seems the data is always properly ordered. That is, the first picture of the first limb comes right after the last limb table. 
    #         //The first limb table start right after the cmd array, and so on. Currently this seems to be the only way to determine how long the 
    #         //cmd array is, or how long the last limb table is. Clumsy but it works, however a simple decoder doesn’t need to compute these lengths :)

    #         //      anim cmds
    #         //        cmd: 8

    #         //Essa conta ta ficando 1 byte atrasado. Não sei se a sessão anterior termina com 00 e eu não estou pulando
    #         //ou se tem algum erro mesmo. Verificar se nos próximos costumes é sempre 00 ou 00 00...
    #         //por hora, vou comentar o código de start+length e calcular igual o site fala.

    #         //Tamanhos do CMD Array
    #         if (AnimCommandsOffset != (DebugGetCurrentRelativePosition(binaryReader))) Debugger.Break();

    #         int cmdArraySize = (int)(LimbsOffsets.First() - (DebugGetCurrentRelativePosition(binaryReader)));
    #         //cmdArraySize = 0;
    #         //foreach (Animation animation in Animations)
    #         //{
    #         //    foreach (AnimationDefinition animationDefinition in animation.AnimDefinitions)
    #         //    {
    #         //        if (!animationDefinition.Disabled)
    #         //        {
    #         //            int cmdArrayFinalPosition = animationDefinition.Start + animationDefinition.Length;
    #         //            if (cmdArrayFinalPosition > cmdArraySize)
    #         //            {
    #         //                cmdArraySize = cmdArrayFinalPosition;
    #         //            }
    #         //        }
    #         //    }
    #         //}

    #         Commands = new List<byte>();
    #         for (int i = 0; i < cmdArraySize; i++)
    #         {
    #             Commands.Add(binaryReader.ReadByte1());
    #         }


    #         Limbs = new List<Limb>();

    #         //Pega uma lista apenas com os limbs distintos, sem as repetições:
    #         //, e ignora o ultimo valor, sei lá porque, mas o ultimo valor parece apontar para o final da lista!
    #         List<ushort> differentLimbsOnly = LimbsOffsets.Distinct().ToList();
    #         for (int i = 0; i < differentLimbsOnly.Count - 1; i++)
    #         {
    #             Limb currentLimb = new Limb();
    #             currentLimb.OffSet = differentLimbsOnly[i];
    #             currentLimb.Size = (ushort)(differentLimbsOnly[i + 1] - differentLimbsOnly[i]);

    #             Limbs.Add(currentLimb);
    #         }
    #         //Para determinar o tamanho do ultimo limb, é preciso saber onde começa a primeira imagem do primeiro limb, 
    #         //pois ela vem, segundo o texto do scummc, logo apos a ultima tabela de limb. Então eu pego o offset da
    #         //primeira imagem do primeiro limb (dando peek no ushort, que será o primeiro valor lido) 
    #         //e subtraio o offset de inicio do ultimo limb, com isso eu descubro o tamanho.
    #         Limb lastLimb = new Limb();
    #         lastLimb.OffSet = differentLimbsOnly[differentLimbsOnly.Count - 1];

    #         //TESTE para tentar descobrir que porra ta acontecendo aqui
    #         ushort nextValue = binaryReader.PeekUint16();
    #         if (nextValue == 0)
    #         {
    #             //Debugger.Break();
    #         }
    #         else
    #         {
    #             lastLimb.Size = (ushort)(nextValue - lastLimb.OffSet);
    #         }

    #         //Eu to achando que se o size for 0, então na verdade esse limb não existe.
    #         //O negócio é que eu acho que pra determinar o tamanho do limb, o engine do scumm
    #         //desconta o offset do limb seguinte do limb atual, então o ultimo limb, se não
    #         //tiver tamanho, era porque seu offset só serviria para determinar o tamanho do limb
    #         //anterior. 
    #         //ACHO que talvez por isso, em algumas vezes o nextValue logo acima é 0,
    #         //porque por alguma razão o valor não era o do inicio da próxima imagem e dai foi nulado. Mas isso tudo pode ser besteira tb.
    #         if (lastLimb.Size > 0)
    #         {
    #             Limbs.Add(lastLimb);
    #         }


    #         foreach (Limb limb in Limbs)
    #         {
    #             if ((limb.Size % 2) != 0) Debugger.Break();
    #             if (limb.OffSet != (DebugGetCurrentRelativePosition(binaryReader))) Debugger.Break();

    #             //Como cada indice tem 2 bytes (ushort), então o total de entradas é o tamanho do limb dividido por 2
    #             for (int i = 0; i < (limb.Size / 2); i++)
    #             {
    #                 ushort currentImageOffset = binaryReader.ReadUint16();
    #                 limb.ImageOffsets.Add(currentImageOffset);
    #             }
    #         }

    #         Pictures = new List<CostumeImageData>();
    #         int picturesHeaderSize = 12;
    #         if ((Format & 0x7E) == 0x60)
    #         {
    #             //soh vai ter redir_limb e redir_pic se os bits 6 e 7 do format estiver ligados.
    #             picturesHeaderSize = 14;
    #         }

    #         //Primeiro vamos calcular o tamanho que tera os dados de cada imagem.
    #         //Para isso, precisamos pegar a imagem atual + 1, e descontar do offset dela
    #         //o offset da imagem atual. Com isso teremos o tamanho total da imagem.
    #         //Desse total, descontamos 14 (ou 12), que é o número de bytes do cabeçalho da imagem.
    #         CostumeImageData lastImageData = null;
    #         foreach (Limb limb in Limbs)
    #         {
    #             if (limb.ImageOffsets.Count > 0)
    #             {
    #                 if (lastImageData != null)
    #                 {
    #                     ushort firstWithImageOffSet = limb.ImageOffsets.Where(x => x > 0).First();
    #                     lastImageData.ImageDataSize = (ushort)((firstWithImageOffSet - lastImageData.ImageStartOffSet) - picturesHeaderSize);
    #                     Pictures.Add(lastImageData);
    #                 }

    #                 for (int i = 0; i < limb.ImageOffsets.Count - 1; i++)
    #                 {
    #                     if (limb.ImageOffsets[i] > 0)
    #                     {
    #                         //if (limb.ImageOffsets[i] != (DebugGetCurrentRelativePosition(binaryReader))) Debugger.Break();

    #                         ushort nextWithImageOffset = limb.ImageOffsets.Skip(i + 1).Where(x => x > 0).First();


    #                         CostumeImageData currentCostumeImageData = new CostumeImageData();
    #                         currentCostumeImageData.ImageStartOffSet = limb.ImageOffsets[i];
    #                         currentCostumeImageData.ImageDataSize = (ushort)((nextWithImageOffset - currentCostumeImageData.ImageStartOffSet) - picturesHeaderSize);

    #                         Pictures.Add(currentCostumeImageData);
    #                     }
    #                 }
    #                 lastImageData = new CostumeImageData();
    #                 ushort lastWithImageOffset = limb.ImageOffsets.Where(x => x > 0).Last();
    #                 lastImageData.ImageStartOffSet = lastWithImageOffset; //limb.ImageOffsets[limb.ImageOffsets.Count - 1];
    #             }
    #         }
    #         if (lastImageData != null)
    #         {
    #             uint sizeVerify = 0;

    #             switch (_gameInfo.ScummVersion)
    #             {
    #                 case 5:
    #                     sizeVerify = BlockSize - 2;
    #                     break;
    #                 case 6:
    #                     //pra determinar o tamanho da ultima imagem, vamos usar o parametro size(??) que foi o primeiro valor lido pelo costume.
    #                     //Talvez eu deva utilizar o blocksize, não sei... é que esse size não faz muito sentido, visto que o blocksize
    #                     //é justamente pra isso. Sei lá, tem alguma pegadinha aqui. Mas em alguns casos o SIZE é 0, dai tem que usar o blocksize mesmo (?)
    #                     sizeVerify = Size == 0 ? BlockSize - 8 : Size;
    #                     break;
    #                 default:
    #                     Debugger.Break(); //Não era pra cair aqui.
    #                     break;
    #             }
    #             lastImageData.ImageDataSize = (ushort)((sizeVerify - lastImageData.ImageStartOffSet) - picturesHeaderSize);
    #             Pictures.Add(lastImageData);
    #         }

    #         //Agora sim, finalmente, depois dessa volta MEDONHA, parece que conseguimos chegar de fato aos dados dos frames das
    #         //animações... espero que sim pelo menos.
    #         foreach (CostumeImageData picture in Pictures)
    #         {
    #             /*
    #             width            : 16le
    #             height           : 16le
    #             rel_x            : s16le
    #             rel_y            : s16le
    #             move_x           : s16le
    #             move_y           : s16le
    #             redir_limb       : 8 only present if((format & 0x7E) == 0x60)
    #             redir_pict       : 8 only present if((format & 0x7E) == 0x60)
    #             rle data
    #              */
    #             picture.Width = binaryReader.ReadUint16();
    #             picture.Height = binaryReader.ReadUint16();
    #             picture.RelX = binaryReader.ReadInt16();
    #             picture.RelY = binaryReader.ReadInt16();
    #             picture.MoveX = binaryReader.ReadInt16();
    #             picture.MoveY = binaryReader.ReadInt16();
    #             if (picturesHeaderSize == 14)
    #             {
    #                 //Mexendo, a impressão que parece é que só tem informações de REDIR_LIMB e REDIR_PICT quando
    #                 //o size == 0. Não sei porque, mas é isso que ta parecendo.
    #                 //Vou fazer mais uns testes.
    #                 picture.HasRedirInfo = true;
    #                 picture.RedirLimb = binaryReader.ReadByte1();
    #                 picture.RedirPict = binaryReader.ReadByte1();
    #             }
    #             picture.ImageData = binaryReader.ReadBytes(picture.ImageDataSize);
    #         }

    #         if (_gameInfo.ScummVersion == 6)
    #         {
    #             uint blockSizeWithoutHeader = (BlockSize - 8);
    #             if (blockSizeWithoutHeader == Size)
    #             {
    #                 //não faz nada
    #             }
    #             else if (blockSizeWithoutHeader == Size + 1)
    #             {
    #                 HasCloseByte = true;
    #                 CloseByte = binaryReader.ReadByte1();
    #             }
    #         }

    #         //TEM GATO NA TUBA!?!?
    #         if (binaryReader.Position - BlockOffSet != BlockSize) Debugger.Break();

    #     }


def read_cost_resource(cost, room_palette, version):
    with io.BytesIO(cost.data) as stream:
        size = 1
        if version == 6:
            size = UINT32LE.unpack(stream.read(UINT32LE.size))[0]
            header = stream.read(2)
            assert header == b'CO'
        num_anim = stream.read(1)[0] + (1 if size > 0 else 0)
        assert num_anim > 0
        flags = stream.read(1)[0]
        num_colors = 32 if flags % 2 else 16
        palette = list(itertools.chain.from_iterable([room_palette[3*x:3*x+3] for x in stream.read(num_colors)]))
        anim_cmds_offset = UINT16LE.unpack(stream.read(UINT16LE.size))[0]
        limbs_offsets = [UINT16LE.unpack(stream.read(UINT16LE.size))[0] for _ in range(16)]
        anim_offsets = [UINT16LE.unpack(stream.read(UINT16LE.size))[0] for _ in range(num_anim)]
        print(anim_offsets)

        parsed_offs = set()

        glimb_mask = 0

        for off in anim_offsets:
            if off == 0:
                continue
            if off in parsed_offs:
                continue
            assert stream.tell() == off, (stream.tell(), off)
            parsed_offs |= {off}
            limb_mask = UINT16LE.unpack(stream.read(UINT16LE.size))[0]
            # print('LIMB MASK', f'{limb_mask:016b}')
            glimb_mask |= limb_mask
            num_limbs = sum(int(x) for x in f'{limb_mask:016b}')
            for limb in range(num_limbs):
                # print('LIMB', limb)
                start = UINT16LE.unpack(stream.read(UINT16LE.size))[0]
                # print('START', start)
                if start != 0xFFFF:
                    next_byte = stream.read(1)[0]
                    no_loop = next_byte & 0x80
                    end_offset = next_byte & 0x7F
                    # print('START', start, 'NOLOOP', no_loop, 'END', end_offset)

        # print('GLIMB MASK', f'{glimb_mask:016b}')
        assert glimb_mask != 0, glimb_mask
        assert stream.tell() == anim_cmds_offset, (stream.tell(), anim_cmds_offset)
        cmds = stream.read(limbs_offsets[0] - stream.tell())

        cpic_offs = []

        diff_limbs = sorted(set(limbs_offsets))
        if len(diff_limbs) > 1:
            for limb_idx, off in enumerate(diff_limbs[:-1]):
                assert stream.tell() == off, (stream.tell(), off)
                num_pics = (diff_limbs[limb_idx + 1] - off) // 2
                pic_offs = [UINT16LE.unpack(stream.read(UINT16LE.size))[0] for _ in range(num_pics)]
                cpic_offs += pic_offs
        else:
            assert stream.tell() == diff_limbs[0], (stream.tell(), diff_limbs[0])
            cpic_offs = [UINT16LE.unpack(stream.read(UINT16LE.size))[0]]
            while stream.tell() < cpic_offs[0]:
                cpic_offs.append(UINT16LE.unpack(stream.read(UINT16LE.size))[0])

        flag_skip = None
        for off in cpic_offs:
            if off == 0:
                continue
            if stream.tell() + 1 == off:
                pad = stream.read(1)
                # assert pad == b'\0', (stream.tell(), off, pad)
            assert stream.tell() == off, (stream.tell(), off)
            width = UINT16LE.unpack(stream.read(UINT16LE.size))[0]
            height = UINT16LE.unpack(stream.read(UINT16LE.size))[0]
            rel_x = SINT16LE.unpack(stream.read(SINT16LE.size))[0]
            rel_y = SINT16LE.unpack(stream.read(SINT16LE.size))[0]
            move_x = SINT16LE.unpack(stream.read(SINT16LE.size))[0]
            move_y = SINT16LE.unpack(stream.read(SINT16LE.size))[0]
            redir_limb, redir_pict = 0, 0
            if flags & 0x7E == 0x60:
                redir_limb, redir_pict = stream.read(2)
            print(width, height, rel_x, rel_y, move_x, move_y, redir_limb, redir_pict)


            if flag_skip is None:
                flag_skip = redir_pict

            if flag_skip == redir_pict:
                im = convert_to_pil_image(
                    bpp_cost.decode1(width, height, num_colors, stream),
                    size=(width, height)
                )
                im.putpalette(palette)
                yield off, im


        print(stream.tell(), size, header, palette, anim_cmds_offset, limbs_offsets, anim_offsets)
        rest = stream.read()
        assert rest in {b'', b'\0'}, (stream.tell() - len(rest), rest)


        # exit(1)


if __name__ == '__main__':
    import argparse
    import glob
    import os

    from nutcracker.utils.fileio import read_file

    parser = argparse.ArgumentParser(description='read smush file')
    parser.add_argument('files', nargs='+', help='files to read from')
    args = parser.parse_args()

    files = sorted(set(flatten(glob.iglob(r) for r in args.files)))
    print(files)
    for filename in files:

        print(filename)

        gameres = open_game_resource(filename)
        basename = gameres.basename

        root = gameres.read_resources(
            # schema=narrow_schema(
            #     SCHEMA, {'LECF', 'LFLF', 'RMDA', 'ROOM', 'PALS'}
            # )
        )

        os.makedirs(f'COST_out/{basename}', exist_ok=True)

        for t in root:

            for lflf in get_rooms(t):
                print(lflf, lflf.attribs["path"])
                _, palette, _, _ = read_room_settings(lflf)

                for cost in sputm.findall('COST', lflf):
                    print(cost, cost.attribs["path"], gameres.game.version)

                    for off, im in read_cost_resource(cost, palette, gameres.game.version):
                        im.save(f'COST_out/{basename}/{os.path.basename(lflf.attribs["path"])}_{os.path.basename(cost.attribs["path"])}_{off:08X}.png')

        # for idx, im in enumerate(read_akos_resource(resource)):
        #     im.save(f'COST_out/{os.path.basename(filename)}_aframe_{idx}.png')
