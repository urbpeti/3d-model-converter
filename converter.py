import argparse
from pathlib import Path
from lib.modelparser import Parser, ObjParsingStrategy
from lib.modelwriter import ModelWriter, STLWritingStrategy

if __name__ == "__main__":
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('-i', '--input',  help='input file path',
                             type=str, default='test.obj')
    args_parser.add_argument('-o', '--output', help='output file path',
                             type=str, default='test.stl')
    args = args_parser.parse_args()

    parser = Parser(ObjParsingStrategy())
    writer = ModelWriter(STLWritingStrategy())

    model = parser.parse(args.input)
    print('Parser done')
    writer.write(args.output, model)
    print("Writer done")
