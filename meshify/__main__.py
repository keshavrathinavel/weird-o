import argparse

from meshify.mesh import mesh_image, un_mesh_image

parser = argparse.ArgumentParser(description="Mesh and Unmesh CLI Tool")
subparsers = parser.add_subparsers(dest='command', required=True, help="Available commands")

# Mesh subcommand
mesh_parser = subparsers.add_parser('mesh', help="Convert image to mesh")
mesh_parser.add_argument('-i', '--input', required=True, help="Input file (e.g., input_file.png)")
mesh_parser.add_argument('-o', '--output', required=True, help="Output file (e.g., output_file.stl)")

# Unmesh subcommand
unmesh_parser = subparsers.add_parser('unmesh', help="Convert mesh to image")
unmesh_parser.add_argument('-i', '--input', required=True, help="Input file (e.g., input_file.stl)")
unmesh_parser.add_argument('-o', '--output', required=True, help="Output file (e.g., output_file.png)")
unmesh_parser.add_argument('-v', '--validate', required=False, help="Validate against an image file")

args = parser.parse_args()

if __name__ == "__main__":
    if args.command == 'mesh':
        mesh_image(args.input, args.output)
    elif args.command == 'unmesh':
        un_mesh_image(args.input, args.output, args.validate)
    else:
        parser.print_help()
